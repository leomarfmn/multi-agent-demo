from utils import run_ocr, upload_to_qdrant, similarity_search
from templates import TEMPLATE_STANDALONE_QUESTION, TEMPLATE_QUESTION_WITH_RAG
from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import os

def process_question(pdf_file, question):
    
    # Perform OCR
    records = run_ocr(pdf_file)

    # Upload to Qdrant
    qdrant_collection = upload_to_qdrant(records)

    # Run similarity search
    vector_similarity_results = similarity_search(question, qdrant_collection)

    # Run question on LLM
    llm_answer = ask_llm(question, vector_similarity_results)

    return llm_answer


def ask_llm(question, vector_similarity_results):
    try:
        # Define LLM output type and RAG context
        llm = get_llm()
        output_parser = JsonOutputParser()
        context = [{"page_number": result['page'], "text": result['text']} for result in vector_similarity_results]

        # The first chain ensures the question is standalone
        standalone_prompt = PromptTemplate(
            input_variables=["question"],
            template=TEMPLATE_STANDALONE_QUESTION
        )
        standalone_chain = standalone_prompt | llm | output_parser
        standalone_json = standalone_chain.invoke({"question": question})

        # The second chain answers the question using the context and the standalone question
        rag_prompt = PromptTemplate(
            input_variables=["standalone_question", "context"],
            template=TEMPLATE_QUESTION_WITH_RAG
        )

        rag_chain = rag_prompt | llm | output_parser
        rag_json = rag_chain.invoke({
            "standalone_question": standalone_json["standalone_question"],
            "context": context
        })

        # Combine the results into a final JSON object
        final_json = {
            "initial_question": question,
            "formatted_question": standalone_json["standalone_question"],
            "reasoning_for_formatted_question": standalone_json["reasoning"],
            "answer": rag_json["answer"],
            "page_references": rag_json.get("page references", "No references found.") if rag_json.get('page references', "").strip() != "" else "No references found.",
        }
        return final_json

    except Exception as e:
        print(f"Error asking LLM: {e}")
        raise HTTPException(status_code=500, detail="LLM query failed")


def get_llm():
    return ChatOpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.1-8b-instant",
        temperature=0.7,
    )
