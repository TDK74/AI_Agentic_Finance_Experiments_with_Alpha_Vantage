import datetime
import gradio as gr
import os
import requests

from autogen.coding import LocalCommandLineCodeExecutor
from autogen import ConversableAgent, AssistantAgent


class OllamaLLM:
    def __init__(self, model = "mistral:7b", host = "http://localhost:11434"):
        self.model = model
        self.host = host.rstrip("/")

    def complete(self, prompt):
        responce = requests.post(f"{self.host}/api/generate",
                                 json = {"model" : self.model,
                                         "prompt" : prompt,
                                         "stream" : False}
                                )
        responce.raise_for_status()

        return responce.json()["response"]


OLLAMA_CLIENT = None

# --- Configs --- #
config_writer = {"model" : "ollama"}
config_executor = None
code_executor_agent = None

# ------------------------------------------------------------------------------------------ #
# Unless you have a real OPENAI_API_KEY use this mimic key -> $env:OPENAI_API_KEY="ollama" 
# in the terminal before running the file in order to avoid this ERROR:
# Error: The api_key client option must be set either by passing api_key to the client or by 
# setting the OPENAI_API_KEY environment variable
# ------------------------------------------------------------------------------------------ #

# --- Conversation history --- #
conversation_log = []

def run_agentic_ai_task(llm_config_writer = config_writer,
                        llm_config_executor = config_executor):
    global code_executor_agent
    global code_writer_agent

    try:
        ## ------------------------------------------------------##
        executor = LocalCommandLineCodeExecutor(
                                                timeout = 60,
                                                work_dir = "coding",
                                                )

        ## ------------------------------------------------------##
        code_executor_agent = ConversableAgent(
                                            name = "code_executor_agent",
                                            llm_config = False,
                                            code_execution_config = {"executor" : executor},
                                            human_input_mode = "ALWAYS",
                                            default_auto_reply = ("Please continue. If everything "
                                                                    "is done, reply 'TERMINATE'."),
                                            )

        ## ------------------------------------------------------##
        writer_llm_config = llm_config_writer.copy()
        writer_llm_config["client"] = OLLAMA_CLIENT

        code_writer_agent = AssistantAgent(
                                            name = "code_writer_agent",
                                            llm_config = writer_llm_config,
                                            code_execution_config = False,
                                            human_input_mode = "NEVER",
                                            )

        ## ------------------------------------------------------##
        code_writer_agent_system_message = code_writer_agent.system_message

        ## ------------------------------------------------------##
        print(code_writer_agent_system_message)

        ## ------------------------------------------------------##
        today = datetime.datetime.now().date()

        message = (f"Today is {today}. "
                    "Create a plot showing stock gain YTD for NVDA and AMD. "
                    "Make sure the code is in markdown code block and save the figure "
                    "to a file ytd_stock_gains.png.""")

        ## ------------------------------------------------------##
        chat_result = code_executor_agent.initiate_chat(code_writer_agent, message = message, )
        print("Agent state:", code_executor_agent._state)

        conversation_log.append(f"👤 User: {message}")
        conversation_log.append(f"🤖 Agent: {chat_result}")

        ## ------------------------------------------------------##
        img_path = os.path.join("coding", "ytd_stock_gains.png")

        if os.path.exists(img_path):
            conversation_log.append("✅ Plot created successfully.")

            return "\n".join(conversation_log), img_path

        else:
            conversation_log.append("⚠️ No result image found.")

            return "\n".join(conversation_log), None

    except Exception as e:
        return f"Error: {e}", None


def run_agentic_ai_task_predefined(llm_config_writer = config_writer,
                                   llm_config_executor = config_executor):
    global code_executor_agent
    global code_writer_agent

    try:
        ## ------------------------------------------------------##
        # define helper functions
        def get_stock_prices(stock_symbols, start_date, end_date):
            """Get the stock prices for the given stock symbols between
            the start and end dates.
            Args:
                stock_symbols (str or list): The stock symbols to get the
                prices for.
                start_date (str): The start date in the format 'YYYY-MM-DD'.
                end_date (str): The end date in the format 'YYYY-MM-DD'.
            Returns:
                pandas.DataFrame: The stock prices for the given stock
                symbols indexed by date, with one column per stock symbol.
            """
            import yfinance


            stock_data = yfinance.download(stock_symbols, start = start_date, end = end_date)

            return stock_data.get("Close")


        ## ------------------------------------------------------##
        def plot_stock_prices(stock_prices, filename):
            """Plot the stock prices for the given stock symbols.
            Args:
                stock_prices (pandas.DataFrame): The stock prices for the
                given stock symbols.
            """
            import matplotlib.pyplot as plt


            plt.figure(figsize = (10, 5))

            for column in stock_prices.columns:
                plt.plot(stock_prices.index, stock_prices[column], label = column)

            plt.title("Stock Prices")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.grid(True)
            plt.savefig(filename)


        ## ------------------------------------------------------##
        executor = LocalCommandLineCodeExecutor(
                                                timeout = 60,
                                                work_dir = "coding",
                                                functions = [get_stock_prices, plot_stock_prices],
                                                )

        ## ------------------------------------------------------##
        code_writer_agent_system_message = AssistantAgent(name = "temp",
                                                    llm_config = llm_config_writer).system_message
        code_writer_agent_system_message += executor.format_functions_for_prompt()

        print(code_writer_agent_system_message)

        ## ------------------------------------------------------##
        writer_llm_config = llm_config_writer.copy()
        writer_llm_config["client"] = OLLAMA_CLIENT

        code_writer_agent = ConversableAgent(
                                            name = "code_writer_agent",
                                            system_message = code_writer_agent_system_message,
                                            llm_config = writer_llm_config,
                                            code_execution_config = False,
                                            human_input_mode = "NEVER",
                                            )

        ## ------------------------------------------------------##
        code_executor_agent = ConversableAgent(
                                            name = "code_executor_agent",
                                            llm_config = llm_config_executor,
                                            code_execution_config = {"executor": executor},
                                            human_input_mode = "ALWAYS",
                                            default_auto_reply = ("Please continue. If everything "
                                                                    "is done, reply 'TERMINATE'."),
                                            )

        ## ------------------------------------------------------##
        today = datetime.datetime.now().date()

        message = (f"Today is {today}. "
                    "Download the stock prices YTD for NVDA and AMD and create "
                    "a plot. Make sure the code is in markdown code block and "
                    "save the figure to a file stock_prices_YTD_plot.png.""")

        chat_result = code_executor_agent.initiate_chat(code_writer_agent, message = message, )

        conversation_log.append(f"👤 User: {message}")
        conversation_log.append(f"🤖 Agent: {chat_result}")

        ## ------------------------------------------------------##
        img_path = os.path.join("coding", "stock_prices_YTD_plot.png")

        if os.path.exists(img_path):
            conversation_log.append("✅ Plot created successfully.")

            return "\n".join(conversation_log), img_path

        else:
            conversation_log.append("⚠️ No result image found.")

            return "\n".join(conversation_log), None

    except Exception as e:
        return f"Error: {e}", None


# --- Reply handler --- #
def reply_to_agents(user_message):
    global code_executor_agent
    global code_writer_agent

    try:
        if code_executor_agent is None or code_writer_agent is None:
             conversation_log.append("❌ Error: Run an Agentic AI Task first.")

             return "\n".join(conversation_log), None

        code_executor_agent.send(message = user_message,
                                 recipient = code_writer_agent,
                                 request_reply = True)
        conversation_log.append(f"👤 User: {user_message}")
        conversation_log.append(f"✅ Reply sent.")

        return "\n".join(conversation_log), None

    except Exception as e:
        conversation_log.append(f"❌ Error sending reply: {e}")
        return "\n".join(conversation_log), None


# --- Gradio interface ---
with gr.Blocks() as demo:
    with gr.Row():
        btn_run_1 = gr.Button("Run Agentic AI Task")
        btn_run_2 = gr.Button("Run Agentic AI Task with Predefined Functions")
        btn_reply = gr.Button("Send reply")

    user_input = gr.Textbox(label = "Your reply to agents", placeholder = "Type here...",
                            interactive = True)
    out_text = gr.Textbox(label = "Agentic AI message field", lines = 14, interactive = False)
    out_image = gr.Image(label = "YTD Gain Plot")

    # note: handlers must return (text, image) where image is a path or PIL
    btn_run_1.click(fn = run_agentic_ai_task, inputs = None, outputs = [out_text, out_image])
    btn_run_2.click(fn = run_agentic_ai_task_predefined, inputs = None,
                    outputs = [out_text, out_image])
    btn_reply.click(fn = reply_to_agents, inputs = user_input, outputs = [out_text, out_image])


if __name__ == "__main__":
    try:
        OLLAMA_CLIENT = OllamaLLM(model = "mistral:7b") # (model = "llama3.1:8b")
        demo.launch()

    except KeyboardInterrupt:
        print("Gradio app stopped.")
