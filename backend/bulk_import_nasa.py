import sqlite3
import requests
import os
from datetime import datetime

def fetch_rover_data(mission_name, target_id, start_date):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "starbleep.db")
    
    print(f"🛰️ Fetching {mission_name} (ID: {target_id})...")
    
    url = "https://ssd.jpl.nasa.gov/api/horizons.api"
    params = {
        "format": "json",
        "COMMAND": f"'{target_id}'", 
        "OBJ_DATA": "NO",
        "MAKE_EPHEM": "YES",
        "EPHEM_TYPE": "OBSERVER",
        "CENTER": "500@499", # Mars Center
        "QUANTITIES": "1",
        "START_TIME": f"'{start_date}'",
        "STOP_TIME": "'2026-02-01'",
        "STEP_SIZE": "30d" # Every 30 days
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
                raw_date = parts[0] 
                try:
                    date_obj = datetime.strptime(raw_date, "%Y-%b-%d")
                    clean_date = date_obj.strftime("%Y-%m-%d")
                except:
                    clean_date = raw_date 

                # Note: Horizons returns RA/DEC by default for OBSERVER. 
                # For Mars surface lat/lon, this is a good approximation for a chart!
                lon = float(parts[2])
                lat = float(parts[3])
                
                cursor.execute('''INSERT OR IGNORE INTO rover_telemetry (mission_name, earth_date, lat, lon) 
                                  VALUES (?, ?, ?, ?)''', (mission_name, clean_date, lat, lon))
                count += 1
        
        conn.commit()
        conn.close()
        print(f"✅ Success! Imported {count} points for {mission_name}.")
    else:
        print(f"❌ Could not find data for {mission_name}. Check the Target ID.")

if __name__ == "__main__":
    # 1. Setup paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "starbleep.db")
    
    # 2. Fresh Start (Optional: remove this if you want to keep old data)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM rover_telemetry")
    conn.commit()
    conn.close()
    print("🧹 Database cleared for fresh import.")

    # 3. THE FLEET (Name, JPL ID, Landing Date)
    missions = [
        ("Curiosity", "-76", "2012-08-06"),
        ("Perseverance", "-168", "2021-02-19"),
        ("Opportunity", "-254", "2004-01-25"),
        ("Spirit", "-253", "2004-01-04")
    ]

    for name, jpl_id, start in missions:
        fetch_rover_data(name, jpl_id, start)