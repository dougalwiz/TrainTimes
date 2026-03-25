import requests
import streamlit as st # Added for secrets

# National Rail REST API endpoint
API_URL = "https://api1.raildata.org.uk/1010-live-departure-board-dep1_2/LDBWS/api/20220120/GetDepBoardWithDetails"

# Get the key from Streamlit Secrets
API_KEY = st.secrets["API_KEY"] 

# Station CRS codes
STATIONS = {
    "Guildford": "GLD",
    "London Waterloo": "WAT"
}

def get_departures(from_station, to_station):
    if not API_KEY:
        return "NO_API_KEY"

    headers = {
        "x-apikey": API_KEY,
        "User-Agent": "TrainDepartureBoardApp/1.0"
    }
    
    url = f"{API_URL}/{STATIONS[from_station]}"
    params = {
        "filterCrs": STATIONS[to_station],
        "filterType": "to" 
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() 
        data = response.json()

        train_services = []
        if data and data.get("trainServices"):
            for service in data["trainServices"]:
                sta = "N/A"
                eta = "N/A"
                if service.get("subsequentCallingPoints"):
                    for calling_point_list in service["subsequentCallingPoints"]:
                        for calling_point in calling_point_list.get("callingPoint", []):
                            if calling_point.get("crs") == STATIONS[to_station]:
                                sta = calling_point.get("st", "N/A")
                                eta = calling_point.get("et", "N/A")
                                break
                
                train_services.append({
                    "std": service.get("std", "N/A"),
                    "etd": service.get("etd", "N/A"),
                    "sta": sta,
                    "eta": eta,
                    "platform": service.get("platform", "N/A"),
                })
        return train_services[:5]
    except Exception as e:
        return []
