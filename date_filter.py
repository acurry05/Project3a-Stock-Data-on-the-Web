from datetime import datetime

API_KEY = "KST2CQHMXDNNVQAX"

def filter_data_by_date(json_data, start_date, end_date):
    # Checking if the dates are correctly inputted in the right order
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
    except:
        print("Error: Date should be in YYYY-MM-DD")
    end = end_date
    begin = start_date
    # Making sure the end date is after the start date.
    if end < begin:
        print("Error: End date must be after start date")
        return
    
    time_series_key = None

    #Checking for the correct time series key from the data
    if "Time Series (Daily)" in json_data:
        time_series_key = "Time Series (Daily)"
    elif "Weekly Time Series" in json_data:
        time_series_key = "Weekly Time Series"
    elif "Monthly Time Series" in json_data:
        time_series_key = "Monthly Time Series"

    #Error message if no time series data is found.
    if time_series_key == None:
        print("Error: Time series data could not be found")
        return None
    
    # Getting the time series data
    time_series_data = json_data[time_series_key]

    # storing the time series data
    data_filtered = {}

    #Looping through the dates in the data
    for date_string in time_series_data:
        date = datetime.strptime(date_string, "%Y-%m-%d").date()

        #Checking if the date is in the correct range and then adding the date to the data
        if begin <= date <= end:
            data_filtered[date_string] = time_series_data[date_string]

        #Check if any data was actually found
    if len(data_filtered) == 0:
        print("Error: No data was found in the date range")
        return None
        
    result = {}

    if "Meta Data" in json_data:
        result["Meta Data"] = json_data["Meta Data"]

    result[time_series_key] = data_filtered
    
    return result

def print_data_filtered(data_filtered):
    time_series_key = None
    
    # Checking which key has the time series data.
    if "Time Series (Daily)" in data_filtered:
        time_series_key = "Time Series (Daily)"
    elif "Weekly Time Series" in data_filtered:
        time_series_key = "Weekly Time Series"
    elif "Monthly Time Series" in data_filtered:
        time_series_key = "Monthly Time Series"

    if time_series_key == None:
        print("Error: No time series data found in filtered data")
        return
    
    time_series = data_filtered[time_series_key]

    print("\n")
    print(f"Filtered Stock Data {time_series_key}")
    print("\n")

    #Sorting the dates so theyre in order
    dates = sorted(time_series.keys())

    # Printing each date and its dta
    for date in dates:
        print(f"{date}: {time_series[date]}")

    print(f"\nData points: {len(dates)}")