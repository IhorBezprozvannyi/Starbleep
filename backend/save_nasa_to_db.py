import sqlite3
import requests

def fetch_and_save():
    # --- PART A: FETCH THE DATA ---
    print("🛰️ Fetching from NASA...")
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
        start = result.find("$$SOE") + 5
        end = result.find("$$EOE")
        raw_line = result[start:end].strip().split('\n')[0]
        parts = raw_line.split()
        
        # Here are our variables
        nasa_date = parts[0]
        nasa_lat = float(parts[2])
        nasa_lon = float(parts[3])

        # --- PART B: SAVE TO DATABASE ---
        print("💾 Saving to starbleep.db...")
        conn = sqlite3.connect('starbleep.db')
        cursor = conn.cursor()

        # 1. Create the table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS rover_telemetry (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            mission_name TEXT,
                            earth_date TEXT,
                            lat REAL,
                            lon REAL)''')

        # 2. Insert the data
        cursor.execute('''INSERT INTO rover_telemetry (mission_name, earth_date, lat, lon) 
                          VALUES (?, ?, ?, ?)''', 
                       ('Curiosity', nasa_date, nasa_lat, nasa_lon))

        conn.commit()
        conn.close()
        print(f"✅ Success! Saved Curiosity data for {nasa_date} to the database.")
    else:
        print("❌ Failed to fetch data from NASA.")

if __name__ == "__main__":
    fetch_and_save()