import datetime
import gradio as gr
import json
import os
import requests

from autogen.coding import LocalCommandLineCodeExecutor
from autogen import ConversableAgent, AssistantAgent


# ----------------------------------------------------------------------
# Ollama Client Class
# ----------------------------------------------------------------------
class OllamaLLM:
    """Custom client for Ollama."""

    def __init__(self, model = "mistral:7b", host = "http://localhost:11434"):
        """Initialize the Ollama LLM client with model and host.
        Args:
            model (str): The Ollama model to use (default: "mistral:7b").
            host (str): The Ollama server host URL (default: "http://localhost:11434").
        """
        self.model = model
        self.host = host.rstrip("/")

    def complete(self, prompt):
        """Send a prompt to the Ollama API and return the generated response.
        Args:
            prompt (str): The input prompt for the LLM.
        Returns:
            str: The generated text response from the LLM.
        """
        responce = requests.post(f"{self.host}/api/generate",
                                 json = {"model" : self.model,
                                         "prompt" : prompt,
                                         "stream" : False}
                                )
        responce.raise_for_status()

        return responce.json()["response"]


# ----------------------------------------------------------------------
# Global variables and LAZY CLIENT ACCESS (The fix for serialization)
# ----------------------------------------------------------------------
_OLLAMA_CLIENT = None

def get_ollama_client():
    """
    Returns the single instance of OllamaLLM, creating it if necessary.
    This prevents the client object from being captured in Gradio's serialization
    closure during setup.
    """
    global _OLLAMA_CLIENT

    if _OLLAMA_CLIENT is None:
        # Initialize the client only when it's first needed.
        _OLLAMA_CLIENT = OllamaLLM(model = "mistral:7b")

    return _OLLAMA_CLIENT


# --- Configs --- #
config_writer = {"model" : "ollama"}
config_executor = None

# ------------------------------------------------------------------------------------------
# Unless you have a real OPENAI_API_KEY use this mimic key -> $env:OPENAI_API_KEY="ollama"
# in the terminal before running the file in order to avoid this ERROR:
# Error: The api_key client option must be set either by passing api_key to the client or by
# setting the OPENAI_API_KEY environment variable
# ------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------
# Helper Functions (for Predefined Task)
# ----------------------------------------------------------------------
def get_stock_prices(stock_symbols, start_date, end_date):
    """Get the stock prices..."""
    import yfinance


    stock_data = yfinance.download(stock_symbols, start = start_date, end = end_date)

    return stock_data.get("Close")


def plot_stock_prices(stock_prices, filename):
    """Plot the stock prices..."""
    import matplotlib.pyplot as plt


    plt.figure(figsize = (10, 5))

    for column in stock_prices.columns:
        plt.plot(stock_prices.index, stock_prices[column], label = column)

    plt.title("Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.savefig(filename)

# ----------------------------------------------------------------------
# Core Agent Setup Functions
# ----------------------------------------------------------------------
def setup_agents(executor_functions = None):
    """Sets up Autogen agents with the Ollama client."""
    # 1. Access the client lazily and globally
    ollama_client = get_ollama_client()

    # 2. Executor
    executor = LocalCommandLineCodeExecutor(
                                            timeout = 60,
                                            work_dir = "coding",
                                            functions = (executor_functions
                                                          if executor_functions else []),
                                            )

    # 3. Writer Config (needs the client object)
    writer_llm_config = config_writer.copy()
    writer_llm_config["client"] = ollama_client

    # 4. Agent Definitions
    code_executor_agent = ConversableAgent(
                                            name = "code_executor_agent",
                                            llm_config = False,
                                            code_execution_config = {"executor" : executor},
                                            human_input_mode = "ALWAYS",
                                            default_auto_reply = ("Please continue. If everything "
                                                                    "is done, reply 'TERMINATE'."),
                                            )

    # Determine system message for writer
    temp_writer = AssistantAgent(name = "temp", llm_config = writer_llm_config)
    writer_system_message = temp_writer.system_message

    if executor_functions:
        writer_system_message += executor.format_functions_for_prompt()

    del temp_writer

    code_writer_agent = ConversableAgent(
                                        name = "code_writer_agent",
                                        system_message = writer_system_message,
                                        llm_config = writer_llm_config,
                                        code_execution_config = False,
                                        human_input_mode = "NEVER",
                                        )

    return code_executor_agent, code_writer_agent

# ----------------------------------------------------------------------
# Gradio Handler Functions
# ----------------------------------------------------------------------
def _run_task_logic(predefined = False):
    """Common logic for running both task types."""
    # 1. Setup Agents (Accesses client globally via get_ollama_client())
    if predefined:
        functions = [get_stock_prices, plot_stock_prices]
        img_filename = "stock_prices_YTD_plot.png"
        message_type = "Download the stock prices YTD"

    else:
        functions = None
        img_filename = "ytd_stock_gains.png"
        message_type = "Create a plot showing stock gain YTD"

    code_executor_agent, code_writer_agent = setup_agents(executor_functions = functions)

    # 2. Initiate Chat
    today = datetime.datetime.now().date()
    message = (f"Today is {today}. {message_type} for NVDA and AMD. "
               f"Make sure the code is in markdown code block and save the figure "
               f"to a file {img_filename}.")

    try:
        chat_result = code_executor_agent.initiate_chat(code_writer_agent, message = message, )

        # 3. Formatting the entire dialogue for display in Gradio
        conversation_log = []

        for msg in chat_result.chat_history:
            sender = msg["name"] if "name" in msg else "Unknown"
            content = msg.get("content", "[No content]") or msg.get("function_call", "[No content]")

            conversation_log.append(f"🤖 {sender}:\n{content.strip()}\n" + ("-" * 20))

        output_text = "\n".join(conversation_log)

        # 4. Check for Image result
        img_path = os.path.join("coding", img_filename)

        if os.path.exists(img_path):
            output_text += "\n✅ Plot created successfully."

            return output_text, img_path

        else:
            output_text += "\n⚠️ No result image found."

            return output_text, None

    except Exception as e:
        return f"❌ Error during task execution: {e}", None


def run_agentic_ai_task_no_functions():
    """Run agentic task without predefined functions."""
    return _run_task_logic(predefined = False)


def run_agentic_ai_task_predefined():
    """Run agentic task with predefined functions (stock prices)."""
    return _run_task_logic(predefined = True)


def reply_to_agents_placeholder(user_message):
    """Placeholder for the disabled reply function."""
    return ("The 'Send Reply' function is inactive because agents are recreated each time Run "
            "Agentic AI Task is launched to avoid problems with Gradio's JSON serialization."), None


# ----------------------------------------------------------------------
# Main Execution Block
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        # NOTE: get_ollama_client() will be called by the handlers when Gradio has already started.
        with gr.Blocks() as demo:
            with gr.Row():
                btn_run_1 = gr.Button("Run Agentic AI Task (No functions)")
                btn_run_2 = gr.Button("Run Agentic AI Task (Predefined functions)")
                btn_reply = gr.Button("Send reply (Disabled)")

            user_input = gr.Textbox(label = "Your reply to agents", placeholder = "Type here...",
                                     interactive = False)
            out_text = gr.Textbox(label = "Agentic AI message field", lines = 14,
                                  interactive = False)
            out_image = gr.Image(label = "YTD Gain Plot")

            # Binds buttons inside Gradio Context.
            btn_run_1.click(fn = run_agentic_ai_task_no_functions, inputs = None,
                            outputs = [out_text, out_image])
            btn_run_2.click(fn = run_agentic_ai_task_predefined, inputs = None,
                            outputs = [out_text, out_image])
            btn_reply.click(fn = reply_to_agents_placeholder, inputs = user_input,
                            outputs = [out_text, out_image])

            demo.launch()

    except KeyboardInterrupt:
        print("Gradio app stopped.")

    except Exception as e:
        # Displays the error at startup, if any.
        print(f"An error occurred during startup: {e}")
