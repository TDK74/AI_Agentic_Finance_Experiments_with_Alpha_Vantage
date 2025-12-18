import gradio as gr
import yfinance as yf
import matplotlib.pyplot as plt
import string

from datetime import datetime


def clean_ticker(ticker):
    """
    Removes non-alphabetic characters from a ticker symbol and returns uppercase letters only.
    Args:
        ticker (str): Raw ticker symbol.
    Returns:
        str: Cleaned ticker (only A-Z).
    """
    return ''.join(filter(lambda c: c in string.ascii_uppercase, ticker.upper()))


def plot_ytd(ticker1, ticker2, start_date, end_date):
    """
    Compares YTD stock gains for two tickers and returns a plot or error message.
    Args:
        ticker1 (str): First ticker (e.g. AAPL).
        ticker2 (str): Second ticker (e.g. MSFT).
        start_date (str): Start date (YYYY-MM-DD).
        end_date (str): End date (YYYY-MM-DD).
    Returns:
        tuple: (plot, message) – plot if successful, None and error message otherwise.
    """
    # Ensure date format is correct
    start_date = str(start_date)[ : 10]
    end_date = str(end_date)[ : 10]

    ticker1 = clean_ticker(ticker1)
    ticker2 = clean_ticker(ticker2)

    if not ticker1 or not ticker2:
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


    # Fetch stock data
    data1 = yf.download(ticker1, start = start_date, end = end_date)
    data2 = yf.download(ticker2, start = start_date, end = end_date)

    if data1.empty or data2.empty:
        message = "⚠️ No data returned. Check ticker symbols or date range."

        return None, message


    # Calculate the YTD gains
    gain1 = ((data1['Close'] - data1['Close'].iloc[0]) / data1['Close'].iloc[0]) * 100
    gain2 = ((data2['Close'] - data2['Close'].iloc[0]) / data2['Close'].iloc[0]) * 100

    # Create a plot
    plt.figure(figsize = (20, 13))
    plt.plot(gain1.index, gain1, label = f'{ticker1} YTD Gain', color = 'blue')
    plt.plot(gain2.index, gain2, label = f'{ticker2} YTD Gain', color = 'red')
    plt.title(f'YTD Stock Gains of {ticker1} and {ticker2}')
    plt.xlabel('Date')
    plt.ylabel('Percentage Gain (%)')
    plt.legend()
    plt.grid(True)

    # Save the plot as PNG
    plt.savefig("ytd_gain_plot.png", dpi = 300)

    return plt, ""


demo = gr.Interface(
                    fn = plot_ytd,
                    inputs = [
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
                                "To stop the app, press Ctrl+C in the terminal!")
                    )

demo.launch()
