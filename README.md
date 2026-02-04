# AI Agentic Finance Experiments with Alpha Vantage

Personal practice inspired by the short course "AI Agentic Design Patterns with AutoGen" on the DeepLearning.AI platform, available for free, while the certificate and graded assessments require a paid subscription.  
For more details, visit:  
<https://learn.deeplearning.ai/courses/ai-agentic-design-patterns-with-autogen/information>

It contains Python scripts that explore stock data using the Alpha Vantage API, written as part of my personal experimentation and learning. In the final two lessons of the course, some API calls did not work as expected (likely due to API key limitations), so I registered my own key from Alpha Vantage (not the same API as in the course) to continue exploring the concepts independently.

In addition, this repository is also influenced by the short course "Building Generative AI Applications with Gradio" on the DeepLearning.AI platform.  
You can explore the course here:  
<https://www.deeplearning.ai/short-courses/building-generative-ai-applications-with-gradio/>

## Related Repositories
`Short Course: AI Agentic Design Patterns with AutoGen`:  
  <https://github.com/TDK74/SC_AI_Agentic_Design_Patterns_with_AutoGen> - raw Python code extracted from the AutoGen course notebooks.  
`Short Course: Building Generative AI Applications with Gradio`:  
  <https://github.com/TDK74/SC_Building_Generative_AI_Applications_with_Gradio> – raw Python code extracted from the Gradio course notebooks.  
`SLMs on laptop`:  
  <https://github.com/TDK74/SLMs_on_laptop> - personal experiments with SLMs, using Ollama on my laptop.

## What's Inside this repository
- `Autogen_Coding_and_Financial_Analysis_v1.py` – **FAIL**: Attempts to integrate AutoGen multi-agent system (code writer and executor) with **Ollama** LLM client and **Gradio** interface for financial analysis. **Agents successfully communicate and generate code in the terminal**, but the Gradio interface fails upon launch due to the persistent error: **Error: Object of type OllamaLLM is not JSON serializable**.
- `Autogen_Coding_and_Financial_Analysis_v2.py` – **FAIL**: Attempts to integrate AutoGen multi-agent system (code writer and executor) with **Ollama** LLM client and **Gradio** interface for financial analysis. **Agents successfully communicate and generate code in the terminal**, but the Gradio interface fails upon launch due to the persistent error: **Error: Object of type OllamaLLM is not JSON serializable**.
- `fetch_basic_daily_stock_data.py` – plots YTD gains for NVDA and SLYG using basic daily data from Alpha Vantage.
- `fetch_ytd_stock_data_with_alpha_vantage.py` – attempts to use adjusted daily data (premium endpoint); may fail with demo API key.
- `fetch_ytd_stock_data_with_AV_enhanced.py` – attempts to use adjusted daily data (premium endpoint) then switch to basic daily data if fails.
- `gradio_plot_ytd_stock.py` - fetches financial data using 'yfinance' (no API key needed), calculates year-to-date (YTD) gains using formulas, plots them, and visualises the results using Gradio.
- `gradio_ytd_stock_data_with_AV.py` - attempts to use adjusted daily data (premium endpoint) then switch to basic daily data if fails, and visualises the results using Gradio.
- `gradio_ollama_control_panel.py` – Gradio control panel for managing Ollama models; supports refresh, start/stop actions, and status feedback.
- `gradio_ollama_model_check.py` – Gradio interface for selecting and starting Ollama models; includes validation, feedback messages, and dropdown integration for user-friendly control.
- `install_alpha_vantage.py` - checks for and installs the 'alpha_vantage' if missing; and prints a link to get a free API key.
- `install_stock_libraries.py` - checks for and installs 'yfinance' and 'matplotlib' if missing; useful for quick setup.
- `ollama_manager.py` – utility functions to check for available Ollama models and trigger model startup via local API; used as backend logic for Gradio interface.
- `plot_ytd_stock_gains.py` - fetches NVDA and IBM data using 'yfinance' (no API key needed), calculates YTD gains using formulas, and plots them.
- `test_autogen_ollama_minimal.py` – Gradio smoke-test for AutoGen agents with Ollama models; validates agent setup and chat initiation.
- `test_fetch_stock_data.py` - tests if 'yfinance' can fetch data for a given ticker; useful for verifying API access and data availability.

## Setup Environment
* Operating System: Windows 10 Pro x64
* Software: Python 3.11 (virtual env)
* Virtual Environment, created with `uv` ( https://github.com/astral-sh/uv )

For detailed instructions on setting up a virtual environment with `uv` see **_uv_env_setup.txt_**, **_requirements_finance_env.txt_** and **_requirements_finance_freeze.txt_**.

## Notes
- The API key is not included. Please replace `"YOUR_API_KEY"` with your own key.
- Some endpoints require premium access and may raise errors with demo API keys.
- Pylance may report type issues, but the code runs and produces correct output.
- To stop the Gradio app, press `Ctrl+C` in the terminal after closing the browser tab.
- All scripts are intended for educational and experimental use.

## Illustrative graphics:
<img width="50%" height="500" alt="NVDA_SLYG" src="https://github.com/user-attachments/assets/cd443501-4d9f-457e-bebc-49fd502d1430"/>
<img width="50%" height="500" alt="NVDA_IBM" src="https://github.com/user-attachments/assets/f386438c-a9db-4ec4-8247-94d05528abae"/>
<img width="50%" height="500" alt="NVDA_AMD" src="https://github.com/user-attachments/assets/0db8eb0a-e448-4b4f-830d-cff0041a5262"/>

## Video demo
Link to my illustrative Youtube video:  
<https://youtu.be/cRRTTT09hAM>
