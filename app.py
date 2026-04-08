import asyncio
import gradio as gr
from io import StringIO
import contextlib
from inference import main

def run_all_tasks():
    buffer = StringIO()
    try:
        with contextlib.redirect_stdout(buffer):
            asyncio.run(main())
    except Exception as e:
        print(f"[ERROR] {e}")
    return buffer.getvalue()

with gr.Blocks(title="Healthcare Triage OpenEnv") as demo:
    gr.Markdown("# 🏥 Healthcare Triage OpenEnv")
    gr.Markdown("Run the complete inference pipeline below.")

    run_btn = gr.Button("🚀 Run All Tasks", variant="primary")
    output = gr.Textbox(
        label="Agent Output",
        lines=25,
        max_lines=30,
        placeholder="Click the button to run inference..."
    )

    run_btn.click(
        fn=run_all_tasks,
        outputs=output,
        api_name="predict"
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)