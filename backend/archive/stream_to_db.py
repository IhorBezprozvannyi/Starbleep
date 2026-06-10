import sqlite3
import ijson
import os

#dont delete but keep it archived

DB_PATH = "starbleep.db"
JSON_PATH = "per_ps.json"

def stream_import():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear out the bad data from the previous run
    print("🧹 Clearing old Perseverance data...")
    cursor.execute("DELETE FROM environmental_data WHERE source='Perseverance'")
    
    print("🚀 Starting Corrected Stream Import...")

    with open(JSON_PATH, 'rb') as f:
        parser = ijson.items(f, 'item')
        
        batch = []
        total_readings = 0
        
        for entry in parser:
            # 1. Clean the Sol string: "sol_0001" -> 1
            raw_sol = entry.get('sol', '0')
            sol_int = int(raw_sol.replace('sol_', ''))
            
            # 2. Get the list of readings inside "data"
            readings = entry.get('data', [])
            
            for r in readings:
                # 3. Grab the actual PRESSURE and LMST (timestamp)
                pressure = r.get('PRESSURE')
                timestamp = r.get('LMST')
                
                # Only add if we have a valid pressure reading
                if pressure is not None:
                    val = (
                        'Perseverance',
                        'Mars',
                        sol_int,
                        None,       # Ls (we'll add this when we scrape curiosity)
                        timestamp,
                        float(pressure),
                        None,       # Temp Air
                        None        # Temp Ground
                    )
                    batch.append(val)
                    total_readings += 1

                # Batch commit every 5000 readings for speed
                if len(batch) >= 5000:
                    cursor.executemany('''
                        INSERT INTO environmental_data 
                        (source, body, sol, ls, timestamp_utc, pressure, temp_air, temp_ground)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', batch)
                    conn.commit()
                    print(f"✅ Imported {total_readings} readings...")
                    batch = []

        # Final batch
        if batch:
            cursor.executemany('''
                INSERT INTO environmental_data 
                (source, body, sol, ls, timestamp_utc, pressure, temp_air, temp_ground)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', batch)
            conn.commit()

    conn.close()
    print(f"🎉 SUCCESS! Total Martian pressure readings saved: {total_readings}")

if __name__ == "__main__":
    stream_import()