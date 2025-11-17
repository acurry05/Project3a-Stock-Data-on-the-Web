import requests
from date_filter import filter_data_by_date, print_data_filtered

def makeRequest(func : str,  symbol : str, apikey : str, start_date : str, end_date : str):
    '''Func: TIME_SERIES_MONTHLY, TIME_SERIES_INTRADAY, TIME_SERIES_DAILY, TIME_SERIES_WEEKLY
    Symbol: Stock Symbol
    Apikey: String from site
    Start_date & End_date: yyyy-mm-dd'''
    #get url
    url = 'https://www.alphavantage.co/query?function=' + func + '&symbol=' + symbol + '&apikey=' + apikey

    #make a request to that url to get the json
    r = requests.get(url)

    #use .json() on the request. This changes it to a dictionary that python can use.
    data = r.json()

    filterered_data = filter_data_by_date(data, start_date, end_date)

    return filterered_data


# To test the function (If you try to test daily further then 100 days ago it wont let you and will come back with a error)
# Pretty sure this is because we have the free tier so it has limits on it
'''
if __name__ == "__main__":
    API_KEY = "KST2CQHMXDNNVQAX"
    symbol = "IBM"
    func = "TIME_SERIES_DAILY"
    start_date = "2025-09-01"
    end_date = "2025-09-04"

    filtered_data = makeRequest(func, symbol, API_KEY, start_date, end_date)

    print_data_filtered(filtered_data)
'''
