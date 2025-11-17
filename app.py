from flask import Flask, render_template, request
from request import makeRequest
import pygal
import lxml.etree
import csv

app = Flask(__name__)


symbols = []
with open('stocks.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        symbols.append(row[0])

intervals = ["TIME_SERIES_INTRADAY", "TIME_SERIES_DAILY", "TIME_SERIES_WEEKLY", "TIME_SERIES_MONTHLY"]

@app.route('/', methods=['GET', 'POST'])
def index():
    chart_svg = None
    error_msg = None

    if request.method == 'POST':
        symbol = request.form['symbol']
        chart_type = request.form['chart_type']
        time_choice = int(request.form['time_choice'])
        interval = request.form.get('interval') or None
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        try:
            stock_data = makeRequest(intervals[time_choice - 1], symbol, 'demo', start_date, end_date)

            if not stock_data:
                error_msg = "No data returned. Try different dates or stock."
            else:
                key = [k for k in stock_data.keys() if "Time Series" in k][0]
                dates = sorted(stock_data[key].keys())
                open_values, high_values, low_values, close_values = [], [], [], []

                for date in dates:
                    open_values.append(float(stock_data[key][date]['1. open']))
                    high_values.append(float(stock_data[key][date]['2. high']))
                    low_values.append(float(stock_data[key][date]['3. low']))
                    close_values.append(float(stock_data[key][date]['4. close']))

                chart = pygal.Bar() if chart_type == 'bar' else pygal.Line()
                chart.title = f"Data for {symbol}"
                chart.x_labels = dates
                chart.add('Open', open_values)
                chart.add('High', high_values)
                chart.add('Low', low_values)
                chart.add('Close', close_values)

                svg_data = chart.render()
                chart_svg = lxml.etree.tostring(lxml.etree.fromstring(svg_data)).decode()

        except Exception as e:
            error_msg = f"Error: {str(e)}"

    return render_template('index.html', symbols=symbols, chart_svg=chart_svg, error_msg=error_msg)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
