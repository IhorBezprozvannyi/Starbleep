import sqlite3
import time
from parser_msl import get_data_for_sol

def run_import():
    conn = sqlite3.connect("curiosity.db") 
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meda_ps_data (
            sol INTEGER, sclk TEXT, lmst TEXT, ltst TEXT, 
            pressure REAL, wind_speed REAL, air_temp REAL, rover_id INTEGER
        )
    """)
    
    # Get already processed sols to avoid re-downloading
    cursor.execute("SELECT DISTINCT sol FROM meda_ps_data")
    already_done = {row[0] for row in cursor.fetchall()}
    
    for sol_num in range(1, 4710):
        if sol_num in already_done: continue
            
        print(f"Processing Sol {sol_num}...", end='\r')
        data = get_data_for_sol(sol_num)
        
        if data:
            cursor.executemany("""
                INSERT INTO meda_ps_data (sol, sclk, lmst, ltst, pressure, wind_speed, air_temp, rover_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, 2)
            """, [(sol_num, r['sclk'], r['lmst'], r['ltst'], r['pressure'], r['wind_speed'], r['air_temp']) for r in data])
            conn.commit()
            print(f"\n--> Saved {len(data)} rows for Sol {sol_num}")
            time.sleep(0.5) # Polite delay
        
    conn.close()
    print("\nImport Complete!")

if __name__ == "__main__":
    run_import()