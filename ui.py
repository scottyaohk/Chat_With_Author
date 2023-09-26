import gradio as gr
from chat import ask
import os
name = os.environ.get('author')

# Gradio UI
with gr.Blocks() as demo:
    gr.HTML(f"<img style=\"margin: 0 auto;width: 150px;\" src='/file=pics/{name}.jpg' />")
    chatbot = gr.Chatbot(label=name).style(height=600)
    state = gr.State([])
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    txt.submit(ask, [txt, state], [chatbot, state])

# demo.launch(server_port=5000, share=True)
demo.launch(server_port=5000)