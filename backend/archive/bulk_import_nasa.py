import sqlite3
import requests
import os
from datetime import datetime
import time

#archive for now!

# --- HELPER FUNCTIONS ---

def get_sol(mission_name, earth_date_str):
    landing_dates = {
        "Curiosity": "2012-08-06",
        "Perseverance": "2021-02-18",
        "Spirit": "2004-01-04",
        "Opportunity": "2004-01-25"
    }
    fmt = "%Y-%m-%d"
    try:
        landed = datetime.strptime(landing_dates[mission_name], fmt)
        current = datetime.strptime(earth_date_str, fmt)
        return int((current - landed).days / 1.02749)
    except:
        return 0


# --- MAIN IMPORT ENGINE ---

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

    try:
        response = requests.get(url, params=params)
        result = response.json().get("result", "")
    except:
        print("❌ Failed to reach JPL Horizons")
        return

    if "$$SOE" in result:
        start_idx = result.find("$$SOE") + 5
        end_idx = result.find("$$EOE")
        data_lines = result[start_idx:end_idx].strip().split('\n')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        count = 0 
        for line in data_lines:
            parts = line.strip().split()
            if len(parts) > 5:
                raw_date = parts[0] 
                try:
                    date_obj = datetime.strptime(raw_date, "%Y-%b-%d")
                    clean_date = date_obj.strftime("%Y-%m-%d")
                except:
                    continue 

                sol_value = get_sol(mission_name, clean_date)
                
                try:
                    lon = float(parts[-2])
                    lat = float(parts[-1])
                except:
                    continue
                
                cursor.execute('''
                    INSERT OR REPLACE INTO rover_telemetry 
                    (mission_name, earth_date, lat, lon, sol, photos_taken, event_log) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (mission_name, clean_date, lat, lon, sol_value, "Normal Operations"))
                count += 1 
                time.sleep(0.5)  # This waits half a second before the next request
        
        conn.commit()
        conn.close()
        print(f"✅ Success! Imported {count} points for {mission_name}.")

if __name__ == "__main__":
    missions = [
        ("Curiosity", "-76", "2012-08-06"),
        ("Perseverance", "-168", "2021-02-19"),
        ("Opportunity", "-254", "2004-01-25"),
        ("Spirit", "-253", "2004-01-04")
    ]

    for name, jpl_id, start in missions:
        fetch_rover_data(name, jpl_id, start)