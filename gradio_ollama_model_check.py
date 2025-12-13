import gradio as gr
import re

from ollama_manager import start_model, model_exists, list_model_names


available_models = list_model_names()


def clean_model_name(name):
    """
    Cleans a model name by removing special characters.
    Args:
        name (str): Raw model name string.
    Returns:
        str: Cleaned model name with only alphanumeric characters, dots, and colons.
    """
    return re.sub(r'[^a-zA-Z0-9\.:]', '', name.strip())


def start_ollama_model(model_name):
    """
    Starts the specified Ollama model after cleaning the name.
    Args:
        model_name (str): Model name from dropdown or input.
    Returns:
        str: Status message indicating success or error.
    """
    model_name = clean_model_name(model_name)

    if not model_name:
        return "⚠️ Invalid model name. Please enter a valid Ollama model name."

    if not model_exists(model_name):
        return f"⚠️ Model '{model_name}' not found in Ollama. Please check the name."

    try:
        start_model(model_name)
        return f"✅ Model '{model_name}' started successfully!"

    except Exception as e:
        return f"❌ Failed to start model '{model_name}': {e}"


with gr.Blocks() as demo:
    input = gr.Dropdown(choices = available_models, label = "Choose Ollama model",
                        info = "Select a model available in your Ollama setup")
    btn_start = gr.Button("Start Ollama model")
    out = gr.Textbox(label = "Message", interactive = False)
    btn_start.click(start_ollama_model, inputs = input, outputs = out)

demo.launch()
