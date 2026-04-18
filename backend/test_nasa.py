import requests

#it works!
  
def fetch_and_clean_data():
    print("🛰️ Fetching data...")
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    params = {
        "format": "json",
        "COMMAND": "'-76'", # Curiosity
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "OBSERVER",
        "CENTER": "'500@499'",
        "QUANTITIES": "'19'",
        "START_TIME": "'2025-10-01'", 
        "STOP_TIME": "'2025-10-02'",
        "STEP_SIZE": "'1d'"
    }

    response = requests.get(url, params=params)
    result = response.json().get("result", "")
    
    if "$$SOE" in result:
        # 1. Find the data line
        start = result.find("$$SOE") + 5
        end = result.find("$$EOE")
        raw_line = result[start:end].strip().split('\n')[0] # Get the first day
        
        # 2. Split the line into pieces
        parts = raw_line.split()
        
        # 3. Pick the numbers (Date is parts[0], Time is parts[1], Lat is parts[2], Lon is parts[3])
        date = parts[0]
        lat = parts[2]
        lon = parts[3]
        
        print(f"\nDATA FOR DATABASE:")
        print(f"Date: {date}")
        print(f"Latitude: {lat}")
        print(f"Longitude: {lon}")
    else:
        print("Error cleaning data.")

if __name__ == "__main__":
    fetch_and_clean_data()