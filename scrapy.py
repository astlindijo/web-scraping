import requests
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
# IBM Lab @astlin_dijo

def make_graph(stock_data, revenue_data, stock):
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    
    axes[0].plot(pd.to_datetime(stock_data_specific.Date), stock_data_specific.Close.astype("float"), label="Share Price", color="blue")
    axes[0].set_ylabel("Price ($US)")
    axes[0].set_title(f"{stock} - Historical Share Price")

    
    axes[1].plot(pd.to_datetime(revenue_data_specific.Date), revenue_data_specific.Revenue.astype("float"), label="Revenue", color="green")
    axes[1].set_ylabel("Revenue ($US Millions)")
    axes[1].set_xlabel("Date")
    axes[1].set_title(f"{stock} - Historical Revenue")

    plt.tight_layout()
    plt.show()

tesla=yf.Ticker("TSLA")
tesla_data=tesla.history(period="max")
tesla_data.reset_index(inplace=True)
print(tesla_data.head())


url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data=requests.get(url).text
beautiful_soup=BeautifulSoup(html_data,"html.parser")

tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
tables = beautiful_soup.find_all("table")
target_table = None

for table in tables:
    if "Tesla Quarterly Revenue" in table.text:
        target_table = table
        break

if target_table is not None:
    rows = target_table.find("tbody").find_all("tr")

    for row in rows:
        cols = row.find_all("td")

        if len(cols) == 2:
            date = cols[0].text.strip()
            revenue = cols[1].text.strip()

            
            tesla_revenue = pd.concat(
                [tesla_revenue, pd.DataFrame([[date, revenue]], columns=["Date", "Revenue"])],
                ignore_index=True
            )

tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"",regex=True)
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
print(tesla_revenue.head())

GameStop=yf.Ticker("GME")
gme_data=GameStop.history(period="max")
gme_data.reset_index(inplace=True)
print(gme_data.head())

url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2=requests.get(url).text
soup=BeautifulSoup(html_data_2,"html.parser")

gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
tables = soup.find_all("table")
target_table = None

for table in tables:
    if "GameStop Quarterly Revenue" in table.text:
        target_table = table
        break

if target_table is not None:
    rows = target_table.find("tbody").find_all("tr")

    for row in rows:
        cols = row.find_all("td")

        if len(cols) == 2:
            date = cols[0].text.strip()
            revenue = cols[1].text.strip()

            
            gme_revenue = pd.concat(
                [gme_revenue, pd.DataFrame([[date, revenue]], columns=["Date", "Revenue"])],
                ignore_index=True
            )

gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"",regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]

make_graph(tesla_data, tesla_revenue, "Tesla")
make_graph(gme_data, gme_revenue, "GameStop")


