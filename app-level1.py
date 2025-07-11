import gradio as gr
from fastapi import FastAPI

# FastAPI app
app = FastAPI()

# Placeholder for the UI
PLACEHOLDER = "Type your question and press Run Agent."

# Clear functions
def reset():
    return None, PLACEHOLDER, PLACEHOLDER
def clear_response():
    return PLACEHOLDER

# Gradio UI
with gr.Blocks() as interface:
    gr.Markdown("# Agentic Case")
    with gr.Tab("Instructions"):
        pass
    with gr.Tab("Agent"):   
        pdf_file = gr.File(label="Upload PDF File", file_types=[".pdf"])
        question = gr.Textbox(label="Question", placeholder=PLACEHOLDER, interactive=True)
        run_button = gr.Button("Run Agent")
        with gr.Row():
            reset_button = gr.Button("Reset")
            clear_response_button = gr.Button("Clear Response")
        response = gr.Textbox(label="Response", placeholder=PLACEHOLDER, interactive=False)

    reset_button.click(fn=reset, outputs=[pdf_file, question, response])
    clear_response_button.click(fn=clear_response, outputs=response)

app = gr.mount_gradio_app(app, interface, path="/app")