import asyncio
import contextlib
from io import StringIO
import gradio as gr
from inference import main

def predict():
    buffer = StringIO()
    with contextlib.redirect_stdout(buffer):
        asyncio.run(main())
    return buffer.getvalue()

with gr.Blocks() as demo:
    gr.Markdown("# Healthcare Triage OpenEnv")
    run_btn = gr.Button("Run All Tasks")
    output = gr.Textbox(lines=25, label="Agent Output")
    run_btn.click(fn=predict, outputs=output, api_name="/predict")

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)