import gradio as gr
import matplotlib.pyplot as plt
import pandas as pd
import string

from alpha_vantage.timeseries import TimeSeries
from datetime import datetime


def clean_ticker(ticker):
    """
    Cleans a stock ticker symbol by removing all non-alphabetic characters
    and converting to uppercase.
    Args:
        ticker (str): Raw ticker symbol, may contain invalid characters.
    Returns:
        str: Cleaned ticker containing only uppercase letters (A-Z).
    """
    return ''.join(filter(lambda c: c in string.ascii_uppercase, ticker.upper()))


def get_stock_data(ts, symbol, start_date, end_date):
    """
    Fetches and processes daily adjusted or basic stock data for a given ticker and date range.
    Args:
        ts (TimeSeries): Alpha Vantage TimeSeries API client.
        symbol (str): Stock ticker symbol (e.g. 'NVDA').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
    Returns:
        tuple: (pd.Series, str) – cumulative percentage gain series and error message (empty if
                                  successful). Returns (None, error_message) on failure.
    """
    # Ensure date format is correct
    start_date = str(start_date)[ : 10]
    end_date = str(end_date)[ : 10]

    symbol = clean_ticker(symbol)

    if not symbol:
        return None, "⚠️ Invalid ticker symbols. Please use Latin letters only."

    message = ""

    try:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_dt = datetime.strptime(end_date, "%Y-%m-%d").date()
        today = datetime.today().date()

        if start_dt > today or end_dt > today:
            message = "⚠️ Dates must not be in the future. Please select a valid range."

            return None, message

    except ValueError:
        message = "⚠️ Invalid date format. Please use YYYY-MM-DD."

        return None, message

    try:
        data, _ = ts.get_daily_adjusted(symbol = symbol, outputsize = 'full')
        column = '5. adjusted close'
        print(f"✅ Using adjusted data for {symbol}")
    except ValueError:
        data, _ = ts.get_daily(symbol = symbol, outputsize = 'compact')
        column = '4. close'
        print(f"⚠️ Premium endpoint not available for {symbol}. Using basic daily data.")

    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    data = (data[start_date:end_date][column]
            .pct_change()
            .fillna(0)
            .add(1)
            .cumprod()
            .sub(1)
            .mul(100))

    return data, ""


def fetch_and_plot_stocks(api_key, ticker1, ticker2, start_date, end_date):
    """
    Fetches and plots cumulative percentage gain for two stock tickers over a specified date range.
    Args:
        api_key (str): Alpha Vantage API key.
        ticker1 (str): First stock ticker (e.g. 'AMD').
        ticker2 (str): Second stock ticker (e.g. 'INTC').
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
    Returns:
        tuple: (matplotlib.pyplot, str) – plot object and empty string if successful,
               (None, error_message) if data fetch or validation fails.
    """
    if not api_key.strip():
        return None, "⚠️ Please enter a valid API key."

    ts = TimeSeries(key = api_key, output_format = 'pandas')

    data1, msg1 = get_stock_data(ts, ticker1, start_date, end_date)
    data2, msg2 = get_stock_data(ts, ticker2, start_date, end_date)

    if data1 is None or data2 is None or data1.empty or data2.empty:
        message = msg1 or msg2 or "⚠️ No data returned. Check ticker symbols or date range."

        return None, message

    plt.figure(figsize=(20, 13))
    plt.plot(data1.index, data1, label=f'{ticker1.upper()} YTD Gain', color='blue')
    plt.plot(data2.index, data2, label=f'{ticker2.upper()} YTD Gain', color='red')
    plt.title(f'YTD Stock Gains of {ticker1.upper()} and {ticker2.upper()}')
    plt.xlabel('Date')
    plt.ylabel('Percentage Gain (%)')
    plt.legend()
    plt.grid(True)
    plt.savefig("ytd_stock_gains.png", dpi=300)

    return plt, ""


demo = gr.Interface(
                    fn = fetch_and_plot_stocks,
                    inputs = [
                            gr.Textbox(label = "Alpha Vantage API Key",
                                       placeholder = "Paste your API key here",
                                       info = "Your key stays local and is never shared."),
                            gr.Textbox(label = "Ticker 1", placeholder = "e.g. META",
                                       info = "Enter stock symbol (e.g. AAPL, TSLA, NVDA)"),
                            gr.Textbox(label = "Ticker 2", placeholder = "e.g. NVDA",
                                       info = "Enter stock symbol (e.g. MSFT, AMZN, GOOG)"),
                            gr.Textbox(label = "Start Date (YYYY-MM-DD)",
                                       placeholder = "e.g. 2025-01-01"),
                            gr.Textbox(label = "End Date (YYYY-MM-DD)",
                                       placeholder = "e.g. 2025-10-29")
                            ],
                    outputs = [
                                gr.Plot(label = "YTD Gain Plot"),
                                gr.Textbox(label = "Message", interactive = False)
                               ],
                    title = "YTD Stock Gain Comparison",
                    description = ("Compare year-to-date stock gains between two companies. "
                                "Dates must be in YYYY-MM-DD format and not in the future. "
                                "Please visit 'https://www.alphavantage.co/support/#api-key' to "
                                "get your free API key. "
                                "To stop the app, press Ctrl+C in the terminal!")
                    )

demo.launch()
