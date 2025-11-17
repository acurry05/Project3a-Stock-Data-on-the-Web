import pygal        #Graphing module
import lxml         #lets pygal be displayed in browser
import requests     #lets you make http requests to query api 
from datetime import datetime
from request import makeRequest
from flask import Flask, Response


def valid_date(prompt: str):
    while True:
        s = input(prompt)
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            print("Use YYYY-MM-DD")

def userinput():
    symbol = input("Enter the stock symbol you are looking for: ")

    chart_type = input("\nEnter the chart type (Bar = 1, Line = 2): ")
    while chart_type not in ['1','2']:
        chart_type = input("\nInvalid choice, enter 1 or 2.")

    print("\nSelect the time series of the chart you want to generate:")
    print("----------------------------------------------------------")
    print("1. Intraday")
    print("2. Daily")
    print("3. Weekly")
    print("4. Monthly")

    time_choice = input("\nEnter time series option (1-4): ")
    while time_choice not in ['1', '2', '3', '4']:
        time_choice = input("Invalid choice, enter 1-4: ")

    interval = None
    if time_choice == '1':
        print("\nInterval options: 1, 5, 15, 30, 60")
        interval = input("Enter interval: ")
        while interval not in ['1', '5', '15', '30', '60']:
            interval = input("Enter interval: ")

    start_date = valid_date("\nEnter the start date (YYYY-MM-DD) ")
    end_date = valid_date("\nEnter the end date (YYYY-MM-DD): ")
    while end_date < start_date:
        end_date = valid_date("Ender the end date (YYYY-MM-DD): ")

    return {
        "symbol": symbol,
        "chart_type": "bar" if chart_type == '1' else "line",
        "time_choice": time_choice,
        "interval": interval,
        "start_date": start_date,
        "end_date": end_date
    }

getInput = userinput()
intervals = ["TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY"]

stock_data = makeRequest(intervals[int(getInput["time_choice"])-1], getInput["symbol"], 'demo', getInput['start_date'], getInput['end_date'])
print(stock_data)
key = list(stock_data.keys())[1]
dates = stock_data[key].keys()
open_values = []
high_values = []
low_values = []
close_values = []
for date in dates:
    open_values.append(float(stock_data[key][date]['1. open']))
    high_values.append(float(stock_data[key][date]['2. high']))
    low_values.append(float(stock_data[key][date]['3. low']))
    close_values.append(float(stock_data[key][date]['4. close']))

# ------------------- Flask app ------------------------------------
app = Flask(__name__)

@app.route('/')
def chart():
    if getInput["chart_type"] == "bar":
        chart = pygal.Bar()
        
    else:
        chart = pygal.Line()
    chart.title = "Data for " + getInput["symbol"]
    chart.x_labels = dates
    chart.add('Open', open_values)
    chart.add('High', high_values)
    chart.add('Low', low_values)
    chart.add('Close', close_values)
    # Render to SVG and parse with lxml
    svg_data = chart.render()
    svg_tree = lxml.etree.fromstring(svg_data)

    # Return SVG as HTTP response
    return Response(lxml.etree.tostring(svg_tree), mimetype='image/svg+xml')

if __name__ == '__main__':
    app.run(port=5000, debug=False, use_reloader=False)
