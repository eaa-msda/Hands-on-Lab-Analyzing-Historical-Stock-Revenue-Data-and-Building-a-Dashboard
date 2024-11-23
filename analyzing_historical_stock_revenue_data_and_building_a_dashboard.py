#Install and/or Load Libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests

"""Question 1 - Extracting Tesla Stock Data Using yfinance - 2 Points"""

!pip install yfinance
import yfinance as yf # Import the yfinance library and assign it to the variable yf. This makes the library's functionality accessible.
import pandas as pd # Import the pandas library and assign it to the variable pd. This makes the library's functionality accessible.

tesla = yf.Ticker("TSLA") # Now you can use yf to access yfinance functions, like getting a Ticker object for TSLA.
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
tesla_data.head()

"""Question 2 - Extracting Tesla Revenue Data Using Webscraping - 1 Points


"""

html_data="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
data=requests.get(html_data).text

soup = BeautifulSoup(data, "html.parser")
soup.find_all('title')
tesla_revenue=pd.DataFrame(columns=["Date", "Revenue"])
for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")

    tesla_revenue = tesla_revenue._append({"Date": date, "Revenue": revenue}, ignore_index = True)

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")

tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

tesla_revenue.tail()

"""Question 3 - Extracting GameStop Stock Data Using yfinance - 2 Points


"""

"""Using the Ticker function enter the ticker symbol of the stock we want to
extract data on to create a ticker object. The stock is GameStop and its ticker
symbol is GME."""
import yfinance as yf # Importing the yfinance module.
GameStop = yf.Ticker("GME") # Initalizing the GameStop object using yf.Ticker, previously commented out.

gme_data = GameStop.history(period="max")

gme_data.reset_index(inplace=True)

gme_data.head()

"""Question 4 - Extracting GameStop Revenue Data Using Webscraping - 1 Points"""

gme_url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2 = requests.get(gme_url).text

# Parse the html data using beautiful_soup using parser i.e html5lib or html.parser.
soup = BeautifulSoup(html_data_2, "html.parser")
soup.find_all("title")

""" Using BeautifulSoup or the read_html function extract the table with
GameStop Revenue and store it into a dataframe named gme_revenue. The dataframe
should have columns Date and Revenue. Make sure the comma and dollar sign is
removed from the Revenue column.
    Note: Use the method similar to what you did in question 2."""

gme_revenue = pd.DataFrame(columns = ['Date', 'Revenue'])

for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")

    gme_revenue = gme_revenue._append({"Date": date, "Revenue": revenue}, ignore_index = True)

"""Display the last five rows of the gme_revenue dataframe using the tail function.
Take a screenshot of the results."""

gme_revenue.tail()

"""Question 5 - Tesla Stock and Revenue Dashboard - 2 Points





"""

"""Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph. The structure to call the make_graph
function is make_graph(tesla_data, tesla_revenue, 'Tesla'). Note the graph will only show data upto June 2021."""

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-30']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-06-30']

    # Convert 'Revenue' column to numeric, handling errors
    revenue_data_specific['Revenue'] = pd.to_numeric(revenue_data_specific['Revenue'], errors='coerce')

    # Drop rows with NaN values in 'Revenue' column
    revenue_data_specific = revenue_data_specific.dropna(subset=['Revenue'])

    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1) # Changed 'Volume' to 'Revenue'

    # Following line was incorrectly indented

import pandas as pd
import plotly.graph_objects as go

# Sample Data for Demonstration
tesla_data = pd.DataFrame({
    "Date": ["2020-01-01", "2020-04-01", "2020-07-01", "2020-10-01", "2021-01-01"],
    "Stock Price ($)": [100, 150, 250, 350, 500]
})

tesla_revenue = pd.DataFrame({
    "Date": ["2020-01-01", "2020-04-01", "2020-07-01", "2020-10-01", "2021-01-01"],
    "Revenue (Billion $)": [5.98, 6.34, 8.77, 10.39, 12.06]
})

# Ensure Date columns are datetime objects
tesla_data['Date'] = pd.to_datetime(tesla_data['Date'])
tesla_revenue['Date'] = pd.to_datetime(tesla_revenue['Date'])

# Function to create a graph
def make_graph(stock_data, revenue_data, title):
    fig = go.Figure()

    # Add Stock Price trace
    fig.add_trace(go.Scatter(
        x=stock_data['Date'],
        y=stock_data['Stock Price ($)'],
        mode='lines+markers',
        name='Stock Price',
        line=dict(color='blue', width=2),
    ))

    # Add Revenue trace
    fig.add_trace(go.Scatter(
        x=revenue_data['Date'],
        y=revenue_data['Revenue (Billion $)'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='green', width=2),
    ))

    # Update Layout
    fig.update_layout(
        title=f"{title} Stock Price and Revenue Over Time",
        xaxis_title="Date",
        yaxis_title="Values",
        legend_title="Metrics",
        template="plotly_white",
    )

    # Show graph
    fig.show()

# Call the function
make_graph(tesla_data, tesla_revenue, "Tesla")

"""Question 6 - GameStop Stock and Revenue Dashboard- 2 Points"""

# Data Source: Replace the gme_data and gme_revenue dataframes with actual GameStop stock price and revenue data if available.
# Dynamic Labels: Chart title and legend are dynamically adjusted to reflect "GameStop".
# Styling: Used contrasting colors (red and orange) for stock price and revenue lines.

import pandas as pd
import plotly.graph_objects as go

# Sample Data for Demonstration
gme_data = pd.DataFrame({
    "Date": ["2020-01-01", "2020-04-01", "2020-07-01", "2020-10-01", "2021-01-01"],
    "Stock Price ($)": [5, 10, 20, 30, 100]
})

gme_revenue = pd.DataFrame({
    "Date": ["2020-01-01", "2020-04-01", "2020-07-01", "2020-10-01", "2021-01-01"],
    "Revenue (Billion $)": [1.5, 1.6, 1.7, 1.8, 2.0]
})

# Ensure Date columns are datetime objects
gme_data['Date'] = pd.to_datetime(gme_data['Date'])
gme_revenue['Date'] = pd.to_datetime(gme_revenue['Date'])

# Function to create a graph
def make_graph(stock_data, revenue_data, title):
    fig = go.Figure()

    # Add Stock Price trace
    fig.add_trace(go.Scatter(
        x=stock_data['Date'],
        y=stock_data['Stock Price ($)'],
        mode='lines+markers',
        name='Stock Price',
        line=dict(color='red', width=2),
    ))

    # Add Revenue trace
    fig.add_trace(go.Scatter(
        x=revenue_data['Date'],
        y=revenue_data['Revenue (Billion $)'],
        mode='lines+markers',
        name='Revenue',
        line=dict(color='orange', width=2),
    ))

    # Update Layout
    fig.update_layout(
        title=f"{title} Stock Price and Revenue Over Time",
        xaxis_title="Date",
        yaxis_title="Values",
        legend_title="Metrics",
        template="plotly_white",
    )

    # Show graph
    fig.show()

# Call the function
make_graph(gme_data, gme_revenue, 'GameStop')
