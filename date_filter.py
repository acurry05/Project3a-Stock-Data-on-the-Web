from datetime import datetime

API_KEY = "KST2CQHMXDNNVQAX"

def filter_data_by_date(json_data, start_date, end_date):
    

    
    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    except ValueError:
        print("Error: Dates must be in YYYY-MM-DD format")
        return None

    if end_date < start_date:
        print("Error: End date must be after start date")
        return None

    # Determine which time series key is present
    time_series_key = None
    if "Time Series (Daily)" in json_data:
        time_series_key = "Time Series (Daily)"
    elif "Weekly Time Series" in json_data:
        time_series_key = "Weekly Time Series"
    elif "Monthly Time Series" in json_data:
        time_series_key = "Monthly Time Series"

    if time_series_key is None:
        print("Error: Time series data not found")
        return None

    # Filter the data
    time_series_data = json_data[time_series_key]
    data_filtered = {}

    for date_string in time_series_data:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
        if start_date <= date_obj <= end_date:
            data_filtered[date_string] = time_series_data[date_string]

    if len(data_filtered) == 0:
        print("Error: No data found in the specified date range")
        return None

    # Include Meta Data if exists
    result = {}
    if "Meta Data" in json_data:
        result["Meta Data"] = json_data["Meta Data"]
    result[time_series_key] = data_filtered

    return result


def print_data_filtered(data_filtered):
    """Prints filtered stock data nicely."""
    if data_filtered is None:
        print("No data to print")
        return

    time_series_key = next((k for k in data_filtered if "Time Series" in k), None)
    if time_series_key is None:
        print("Error: No time series data in filtered data")
        return

    time_series = data_filtered[time_series_key]
    dates = sorted(time_series.keys())

    print(f"\nFiltered Stock Data ({time_series_key}):\n")
    for date in dates:
        print(f"{date}: {time_series[date]}")

    print(f"\nTotal data points: {len(dates)}")
