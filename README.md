# AI Agentic Finance Experiments with Alpha Vantage

Inspired by the short course "AI Agentic Design Patterns with AutoGen" on the DeepLearning.AI platform, available for free.  
For more details, visit:  
<https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/>

This repository contains Python scripts that explore stock data using the Alpha Vantage API.  
The code was written as part of my personal practice and experimentation, based on ideas from the course.  
In the final two lessons, some API calls did not work as expected (likely due to demo key limitations), so I generated my own Alpha Vantage key to continue exploring the concepts independently.

## Related Repositories
My practice repo for the AutoGen course contains raw Python code extracted from the course notebooks:  
<https://github.com/TDK74/SC_AI_Agentic_Design_Patterns_with_AutoGen>

## What's Inside
- `fetch_basic_daily_stock_data.py` – plots YTD gains for NVDA and SLYG using basic daily data from Alpha Vantage.
- `fetch_ytd_stock_data_with_alpha_vantage.py` – attempts to use adjusted daily data (premium endpoint); may fail with demo API key.
- `install_alpha_vantage.py` - checks for and installs the alpha_vantage package if missing; and prints a link to get a free API key.
- `install_stock_libraries.py` - checks for and installs yfinance and matplotlib if missing; useful for quick setup.
- `plot_ytd_stock_gains.py` - fetches NVDA and IBM data using yfinance (no API key needed), calculates YTD gains using formulas, and plots them.
- `test_fetch_stock_data.py` - tests if yfinance can fetch data for a given ticker; useful for verifying API access and data availability.

## Notes
- The API key is not included. Please replace `"YOUR_API_KEY"` with your own key.
- Some endpoints require premium access and may raise errors with demo keys.
- Pylance may report type issues, but the code runs and produces correct output.
