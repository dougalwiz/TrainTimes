import requests
import config

# National Rail REST API endpoint
API_URL = "https://api1.raildata.org.uk/1010-live-departure-board-dep1_2/LDBWS/api/20220120/GetDepBoardWithDetails"

# Station CRS codes
STATIONS = {
    "Guildford": "GLD",
    "London Waterloo": "WAT"
}

def get_departures(from_station, to_station):
    """
    Get departure information for a given route using the REST API.
    """
    if not config.API_KEY or config.API_KEY == "YOUR_API_KEY":
        return "NO_API_KEY"

    # FIX 1: Added a custom User-Agent to prevent the API from blocking the request
    headers = {
        "x-apikey": config.API_KEY,
        "User-Agent": "TrainDepartureBoardApp/1.0"
    }
    
    url = f"{API_URL}/{STATIONS[from_station]}"
    
    # FIX 2: Added 'filterType' because 'filterCrs' usually requires it
    params = {
        "filterCrs": STATIONS[to_station],
        "filterType": "to" 
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        train_services = []
        if data and data.get("trainServices"):
            for service in data["trainServices"]:
                # The new API response structure is different
                sta = "N/A"
                eta = "N/A"
                if service.get("subsequentCallingPoints"):
                    for calling_point_list in service["subsequentCallingPoints"]:
                        for calling_point in calling_point_list.get("callingPoint", []):
                            if calling_point.get("crs") == STATIONS[to_station]:
                                sta = calling_point.get("st", "N/A")
                                eta = calling_point.get("et", "N/A")
                                break
                        if sta != "N/A":
                            break
                
                train_services.append({
                    "std": service.get("std", "N/A"),
                    "etd": service.get("etd", "N/A"),
                    "sta": sta,
                    "eta": eta,
                    "platform": service.get("platform", "N/A"),
                })
        return train_services[:5]

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print(f"Error calling National Rail API: {e}")
            return "INVALID_API_KEY"
        else:
            # This will now print the exact status code (e.g., 400 or 403) if it fails again
            print(f"HTTP Error: {e.response.status_code} - {e}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error calling National Rail API: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []