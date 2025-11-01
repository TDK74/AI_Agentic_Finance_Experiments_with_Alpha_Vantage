# AI Agentic Finance Experiments with Alpha Vantage

Personal practice inspired by the short course "AI Agentic Design Patterns with AutoGen" on the DeepLearning.AI platform, available for free.  
For more details, visit:  
<https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/>

It contains Python scripts that explore stock data using the Alpha Vantage API, written as part of my personal experimentation and learning. In the final two lessons of the course, some API calls did not work as expected (likely due to API key limitations), so I registered my own key from Alpha Vantage (not the same API as in the course) to continue exploring the concepts independently.

## Related Repositories
`Short Course: AI Agentic Design Patterns with AutoGen` <https://github.com/TDK74/SC_AI_Agentic_Design_Patterns_with_AutoGen> - raw Python code extracted from the AutoGen course notebooks.

## What's Inside this repository
- `fetch_basic_daily_stock_data.py` – plots YTD gains for NVDA and SLYG using basic daily data from Alpha Vantage.
- `fetch_ytd_stock_data_with_alpha_vantage.py` – attempts to use adjusted daily data (premium endpoint); may fail with demo API key.
- `fetch_ytd_stock_data_with_AV_enhanced.py` – attempts to use adjusted daily data (premium endpoint) then switch to basic daily data if fails.
- `install_alpha_vantage.py` - checks for and installs the 'alpha_vantage' if missing; and prints a link to get a free API key.
- `install_stock_libraries.py` - checks for and installs 'yfinance' and 'matplotlib' if missing; useful for quick setup.
- `plot_ytd_stock_gains.py` - fetches NVDA and IBM data using 'yfinance' (no API key needed), calculates YTD gains using formulas, and plots them.
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
- All scripts are intended for educational and experimental use.

## Illustrative graphics:
<img width="50%" height="500" alt="NVDA_SLYG" src="https://github.com/user-attachments/assets/cd443501-4d9f-457e-bebc-49fd502d1430"/>
<img width="50%" height="500" alt="NVDA_IBM" src="https://github.com/user-attachments/assets/f386438c-a9db-4ec4-8247-94d05528abae"/>
<img width="50%" height="500" alt="NVDA_AMD" src="https://github.com/user-attachments/assets/0db8eb0a-e448-4b4f-830d-cff0041a5262"/>
