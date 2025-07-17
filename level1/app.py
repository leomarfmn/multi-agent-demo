import gradio as gr
from fastapi import FastAPI
from utils_llm import process_question
from templates import ANSWER_TEMPLATE

# FastAPI app
app = FastAPI()

# Placeholder for the UI
PLACEHOLDER = "Type your question and press Run Agent."

# Button functions
def reset():
    return None, PLACEHOLDER, PLACEHOLDER
def clear_response():
    return PLACEHOLDER
def gradio_process_question(pdf_file, question):
    if pdf_file is None or question.strip() == "":
        return "Please upload a PDF file and enter a question."
    else:
        response = process_question(pdf_file, question)
        answer = ANSWER_TEMPLATE.format(answer=response['answer'], page_references=response['page_references'])
        return answer

# Gradio UI
with gr.Blocks() as interface:
    gr.Markdown("# Agentic Case")
    with gr.Tab("Agent"):   
        pdf_file = gr.File(label="Upload PDF File", file_types=[".pdf"], type='filepath')
        question = gr.Textbox(label="Question", placeholder=PLACEHOLDER, interactive=True)
        run_button = gr.Button("Run Agent")
        with gr.Row():
            reset_button = gr.Button("Reset")
            clear_response_button = gr.Button("Clear Response")
        response = gr.Textbox(label="Response", placeholder=PLACEHOLDER, interactive=False)
    with gr.Tab("Instructions"):
        pass

    run_button.click(fn=gradio_process_question, inputs=[pdf_file, question], outputs=response)
    reset_button.click(fn=reset, outputs=[pdf_file, question, response])
    clear_response_button.click(fn=clear_response, outputs=response)

app = gr.mount_gradio_app(app, interface, path="/app")