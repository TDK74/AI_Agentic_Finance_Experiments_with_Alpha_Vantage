# Agentic Finance Experiments with Alpha Vantage

Inspired by the short course "AI Agentic Design Patterns with AutoGen" on DeepLearning.AI:  
<https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/>

This repository contains Python scripts that explore stock data using the Alpha Vantage API.  
The code was written as part of my personal practice and experimentation, based on ideas from the course.

## Related Repositories
My practice repo for the AutoGen course contains raw Python code extracted from the course notebooks:  
<>

## What's Inside
- `fetch_basic_daily_stock_data.py` – plots YTD gains for NVDA and SLYG using basic daily data
- `fetch_ytd_stock_data_with_alpha_vantage.py` – attempts to use adjusted daily data (premium endpoint)

## Notes
- The API key is not included. Please replace `"YOUR_API_KEY"` with your own key.
- Some endpoints require premium access and may raise errors with demo keys.
- Pylance may report type issues, but the code runs and produces correct output.
