import sqlite3
import requests
import os
from datetime import datetime

def fetch_rover_data(mission_name, target_id, start_date):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "starbleep.db")
    
    print(f"🛰️ Fetching {mission_name}...")
    
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    params = {
        "format": "json",
        "COMMAND": f"'{target_id}'", 
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "OBSERVER",
        "CENTER": "500@499", 
        "QUANTITIES": "1",
        "START_TIME": f"'{start_date}'",
        "STOP_TIME": "'2026-02-01'",
        "STEP_SIZE": "30d"
    }

    response = requests.get(url, params=params)
    result = response.json().get("result", "")

    if "$$SOE" in result:
        start = result.find("$$SOE") + 5
        end = result.find("$$EOE")
        data_lines = result[start:end].strip().split('\n')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        count = 0
        for line in data_lines:
            parts = line.split()
            if len(parts) >= 4:
                # --- DATE FIX START ---
                raw_date = parts[0] # e.g., "2019-Jul-31"
                try:
                    # Convert "2019-Jul-31" to "2019-07-31"
                    date_obj = datetime.strptime(raw_date, "%Y-%b-%d")
                    clean_date = date_obj.strftime("%Y-%m-%d")
                except:
                    clean_date = raw_date # Fallback
                # --- DATE FIX END ---

                lat = float(parts[3])
                lon = float(parts[2])
                
                cursor.execute('''INSERT OR IGNORE INTO rover_telemetry (mission_name, earth_date, lat, lon) 
                                  VALUES (?, ?, ?, ?)''', (mission_name, clean_date, lat, lon))
                count += 1
        
        conn.commit()
        conn.close()
        print(f"✅ Success! Imported {count} points for {mission_name}.")

if __name__ == "__main__":
    # Clear the table first so we start fresh
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "starbleep.db")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM rover_telemetry")
    conn.commit()
    conn.close()
    print("🧹 Database cleared for fresh import.")

    # Fetch Curiosity (approx 160+ points)
    fetch_rover_data("Curiosity", "-76", "2012-08-06")
    
    # Fetch Perseverance (approx 61 points)
    fetch_rover_data("Perseverance", "-168", "2021-02-19")