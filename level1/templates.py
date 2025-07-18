TEMPLATE_STANDALONE_QUESTION = """
You are an expert at analyzing questions and making sure the questions are clear and concise. Given a question, return the same question if it is clear, or return a reformulated version of the question if it is not clear. Your job is to ensure we are passing a standalone question to an LLM. Below you will find some examples.

Examples (input > output):
1. Soccer > What can you tell me about soccer?
2. France capital > What is the capital of France?
3. How do I cook pasta? > How do I cook pasta?

You should return a JSON object with the following structure:
{{
  "question": "soccer",
  "standalone_question": "What can you tell me about soccer?",
  "reasoning": "The original question was simply 'soccer?', which is not clear enough. The reformulated question provides more context and asks for specific information."
}}

No introductory text, no call to action at the end, nothing but the JSON object.

Question: {question}
"""


TEMPLATE_QUESTION_WITH_RAG = """
You are an expert assistant. Given a standalone question and relevant context, answer the question using only the provided context. If the context does not contain the answer, say "Not found in context."

Return a JSON object:
{{
  "answer": "...",
  "page references": "..."
}}

Standalone question: {standalone_question}
Context: {context}
"""


ANSWER_TEMPLATE = """
Here is the answer to your question using the provided context:
{answer}

These are the pages that were referenced to answer your question:
{page_references}
"""


INSTRUCTIONS = """
## About the Project

This demo is Level 1 of a multi-level demo on AI agents. Each level introduces new capabilities and increasing complexity.  
**Level 1** focuses on document question answering using OCR and Retrieval-Augmented Generation (RAG).  
- You can upload a PDF file.
- The system extracts text using OCR, stores it in a vector database (Qdrant), and an LLM (large language model) answers your question using context from the document (using RAG).
- Higher levels will add support for images, audio, chat memory, and agent orchestration.

## How to Use

1. **Upload a PDF file** using the provided file upload box.
2. **Type your question** about the document in the question box.
3. Click **Run Agent** to get an answer based on the document’s content.
4. Use **Reset** to clear all inputs, or **Clear Response** to clear only the answer box.

**What to Expect:**  
- The system will read your PDF, extract its text, and search for relevant information.
- Answers are generated using only the document’s content.
- Page references are provided so you know where the answer was found.
- If the answer is not found in the document, it will say "Not found in context."

**Connect with me:**  
[LinkedIn](https://www.linkedin.com/in/leomar-fonseca/)  
[GitHub](https://github.com/leomarfmn)
"""

PLACEHOLDER = "Type your question and press Run Agent."