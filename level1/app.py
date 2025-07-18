import gradio as gr
from fastapi import FastAPI, UploadFile, File, Form, Depends

# Custom imports
from utils import CUSTOM_CSS, verify_developer_token
from utils_llm import process_question
from templates import ANSWER_TEMPLATE, INSTRUCTIONS, PLACEHOLDER

# FastAPI app
app = FastAPI()

# POST endpoint
@app.post("/multi-agent-demo-level1")
def process_question_endpoint(
    file: UploadFile = File(None),
    question: str = Form(None),
    api_key_header: str = Depends(verify_developer_token)
):
    return process_question(file, question)

# Button functions
def reset():
    return None, PLACEHOLDER, PLACEHOLDER, None
def clear_response():
    return PLACEHOLDER, None
def gradio_process_question(pdf_file, question):
    if pdf_file is None or question.strip() == "":
        return "Please upload a PDF file and enter a question.", None
    else:
        json_response = process_question(pdf_file, question)
        formatted_answer = ANSWER_TEMPLATE.format(answer=json_response['answer'], page_references=json_response['page_references'])
        return formatted_answer, json_response

# Gradio UI
with gr.Blocks(css=CUSTOM_CSS) as interface:
    gr.Markdown("# Multi-Agent Demo - Level 1: OCR and RAG")
    with gr.Tab("Instructions"):
        gr.Markdown(INSTRUCTIONS)
    with gr.Tab("Agent"):
        pdf_file = gr.File(label="Upload PDF File", file_types=[".pdf"], type='filepath')
        question = gr.Textbox(label="Question", placeholder=PLACEHOLDER, interactive=True)
        run_button = gr.Button("Run Agent")
        with gr.Row():
            reset_button = gr.Button("Reset")
            clear_response_button = gr.Button("Clear Response")
        response = gr.Markdown(label="Response", value=PLACEHOLDER, elem_classes="answer-box")
        json_response = gr.JSON(label="Full JSON Response", visible=True)

    run_button.click(fn=gradio_process_question, inputs=[pdf_file, question], outputs=[response, json_response])
    reset_button.click(fn=reset, outputs=[pdf_file, question, response, json_response])
    clear_response_button.click(fn=clear_response, outputs=[response, json_response])

app = gr.mount_gradio_app(app, interface, path="/app")