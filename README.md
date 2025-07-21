# Multi-Agent Demo: LLMs & Agents

This repository was designed to demonstrate how Large Language Models (LLMs) and AI Agents can be applied to real-world tasks, with a focus on practical document understanding and multi-modal capabilities. The project is structured in **three levels**, each introducing new features and increasing complexity.

---

## The levels

- **Level 1** demonstrates how to answer questions about documents using OCR, vector search, and LLMs. We take a PDF file where text can't be selected, run through a pipeline that uploads the content of the file to a vector DB (Qdrant) and use that as context to answer questions (RAG).
- **Level 2** add image and audio understanding, plus multi-agent orchestration (coming)
- **Level 3** introduce chat memory and observability for production-grade agent workflows (coming)

Each level is self-contained, so one can run and experiment with them independently.

---

## Project Roadmap

### Level 1: Document Q&A with OCR and RAG

**What it does:**

- Lets one upload a PDF (even scanned/non-selectable).
- Uses OCR to extract text from each page.
- Splits text into chunks and stores them as embeddings in a vector database (Qdrant).
- Uses a Retrieval-Augmented Generation (RAG) pipeline:
  - Finds relevant chunks for your question.
  - Reformulates unclear questions for the LLM - turns malformulated questions into standalone questions.
  - Answers using only the document context, with page references.
- The same outcome can also be achieved by running an API POST request, without using the user interface.

**Tech Stack:**

- UI: Gradio
- API: FastAPI
- OCR: pytesseract
- Embeddings: sentence-transformers
- Vector DB: Qdrant
- LLM: Groq API (Llama-3.1-8b-instant)
- Orchestration: LangChain

**How to Run Level 1:**

1. **Recommendations:**
   After forking the repo, create a virtual environment and install requirements, to avoid possible conflicts.

2. **API-KEYS**
   The keys to GROQ and QDRANT were omitted to this repository via a .env file, so new users should replicate this set up inside the level1 folder.

3. **Run the app:**
   uvicorn app:app --host=0.0.0.0 --port=8080

   Or use Docker:
   docker build --rm -t multi-agent-demo-level1 .
   docker run --name multi-agent-demo-level1-container --rm -p 8080:8080 multi-agent-demo-level1

4. **Open the Gradio UI:**  
   The address will depend on how the server was started.

---

## About the Author

- [LinkedIn](https://www.linkedin.com/in/leomar-fonseca/)
- [GitHub](https://github.com/leomarfmn)

---
