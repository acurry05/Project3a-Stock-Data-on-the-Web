import requests
# Example url: https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo

#defines what function, which stock and the apikey
function = 'TIME_SERIES_MONTHLY'
symbol = 'IBM'
apikey = 'demo'

#put above info into a url
url = 'https://www.alphavantage.co/query?function=' + function + '&symbol=' + symbol + '&apikey=' + apikey

#make a request to that url to get the json
r = requests.get(url)

#use .json() on the request. This changes it to a dictionary that python can use.
data = r.json()

#define dates to filter
begin_date = "2024-01-01"
end_date = "2025-01-01"

#API is set up with "Meta Data" as one key and in the case of monthly time series the other key is "Monthly Time Series".
#Worth noting that the second dictionary key will change depending on what the user wants to access.

for date in data["Monthly Time Series"]:
    #filter via date
    if begin_date < date < end_date:
        print(date + ":" + str(data["Monthly Time Series"][date]))

#print(data)