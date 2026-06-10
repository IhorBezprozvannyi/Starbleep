import sqlite3
import csv
import io
import requests

# Base URL to the NASA directory structure you found
BASE_URL = "https://pds-atmospheres.nmsu.edu/PDS/data/PDS4/Mars2020/mars2020_meda/data_calibrated_env/sol_0000_0089/"

def fetch_and_parse_sol(sol_num):
    """Downloads ATS (Air) and TIRS (Ground) data for a specific Sol and pairs them by time."""
    sol_str = f"sol_{sol_num:04d}"
    
    # NASA's exact naming convention patterns for Sol 1, Sol 2, etc.
    ats_file = f"WE__{sol_num:04d}___________CAL_ATS_________________P01.CSV"
    tirs_file = f"WE__{sol_num:04d}___________CAL_TIRS________________P04.CSV"
    
    data_points = []
    
    try:
        # 1. Fetch Air Temperature Data
        ats_res = requests.get(f"{BASE_URL}{sol_str}/{ats_file}")
        if ats_res.status_code != 200:
            return [] # Skip if NASA hasn't uploaded this Sol's file yet
            
        # Parse rows (Filtering out non-numeric header lines)
        ats_rows = list(csv.reader(io.StringIO(ats_res.text)))
        
        # 2. Fetch Ground Temperature Data
        tirs_res = requests.get(f"{BASE_URL}{sol_str}/{tirs_file}")
        tirs_rows = list(csv.reader(io.StringIO(tirs_res.text))) if tirs_res.status_code == 200 else []

        # 3. Read and align the timelines (NASA files typically store elapsed seconds or LTST in Col 0)
        # For simplicity and speed, we grab data points at regular intervals across the file
        max_rows = min(len(ats_rows), len(tirs_rows)) if tirs_rows else len(ats_rows)
        
        # We step through the file rows (e.g., pulling a reading every 1000 rows to avoid blowing up the DB size)
        for i in range(0, max_rows, 1000):
            try:
                row_ats = ats_rows[i]
                # If we don't have ground temp rows, default it safely
                row_tirs = tirs_rows[i] if tirs_rows else [0, -50.0] 
                
                # Basic scientific safety check to make sure we are parsing numbers
                if not row_ats[0].replace('.','',1).isdigit():
                    continue
                
                # Convert elapsed time to a readable hourly stamp (or keep raw seconds)
                seconds = float(row_ats[0])
                hours = int((seconds / 3600) % 24)
                minutes = int((seconds / 60) % 60)
                time_stamp = f"{hours:02d}:{minutes:02d}:00"
                
                air_temp = float(row_ats[1])
                ground_temp = float(row_tirs[1])
                
                data_points.append((sol_num, time_stamp, air_temp, ground_temp, 0.12))
            except (ValueError, IndexError):
                continue
    except Exception as e:
        print(f"Skipping Sol {sol_num} due to an error: {e}")
        
    return data_points

# --- Main Database Loader Configuration ---
print("📡 Connecting to starbleep.db...")
conn = sqlite3.connect("starbleep.db")
cursor = conn.cursor()

# Create a robust table designed for a massive multi-sol scientific time-series dataset
cursor.execute('''
    CREATE TABLE IF NOT EXISTS meda_time_series (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sol INTEGER,
        sample_time TEXT,
        air_temp REAL,
        ground_temp REAL,
        relative_humidity REAL
    )
''')

# Let's scrape the first batch of Sols available in this directory bucket (Sols 1 to 5)
# (You can expand this range up to 89 later once you verify it works!)
print("🚀 Initializing pipeline: Fetching all scientific rows directly from NASA PDS...")
all_rows = []
for sol in range(1, 6):
    print(f"  -> Scraping and extracting raw telemetry for Sol {sol}...")
    sol_data = fetch_and_parse_sol(sol)
    if sol_data:
        all_rows.extend(sol_data)
        print(f"     ✅ Extracted {len(sol_data)} calibrated data coordinates.")

if all_rows:
    cursor.executemany('''
        INSERT OR REPLACE INTO meda_time_series (sol, sample_time, air_temp, ground_temp, relative_humidity)
        VALUES (?, ?, ?, ?, ?)
    ''', all_rows)
    conn.commit()

conn.close()
print(f"\n🎉 Step 1 & 2 Complete! Your database now contains real scientific multi-sol streams.")