import sqlite3
import requests
import re
import sys

#archive

DB_PATH = "/Volumes/Expansion Drive/starbleep_backend/backend/starbleep.db"
BASE_URL = "https://pds-atmospheres.nmsu.edu/PDS/data/mslrem_1001/DATA/"

def get_nasa_range_folder(sol):
    if 1 <= sol <= 89: return "SOL_00001_00089"
    if 90 <= sol <= 179: return "SOL_00090_00179"
    if 180 <= sol <= 269: return "SOL_00180_00269"
    if 270 <= sol <= 359: return "SOL_00270_00359"
    if 360 <= sol <= 449: return "SOL_00360_00449"
    if 450 <= sol <= 583: return "SOL_00450_00583"
    if 584 <= sol <= 707: return "SOL_00584_00707"
    if 708 <= sol <= 804: return "SOL_00708_00804"
    if 805 <= sol <= 938: return "SOL_00805_00938"
    if 939 <= sol <= 1062: return "SOL_00939_01062"
    if 1063 <= sol <= 1159: return "SOL_01063_01159"
    if 1160 <= sol <= 1293: return "SOL_01160_01293"
    if 1294 <= sol <= 1417: return "SOL_01294_01417"
    if 1418 <= sol <= 1514: return "SOL_01418_01514"
    if 1515 <= sol <= 1648: return "SOL_01515_01648"
    if 1649 <= sol <= 1772: return "SOL_01649_01772"
    if 1773 <= sol <= 1869: return "SOL_01773_01869"
    if 1870 <= sol <= 2003: return "SOL_01870_02003"
    if 2004 <= sol <= 2127: return "SOL_02004_02127"
    if 2128 <= sol <= 2224: return "SOL_02128_02224"
    if 2225 <= sol <= 2358: return "SOL_02225_02358"
    if 2359 <= sol <= 2482: return "SOL_02359_02482"
    if 2483 <= sol <= 2579: return "SOL_02483_02579"
    if 2580 <= sol <= 2713: return "SOL_02580_02713"
    if 2714 <= sol <= 2837: return "SOL_02714_02837"
    if 2838 <= sol <= 2934: return "SOL_02838_02934"
    if 2935 <= sol <= 3068: return "SOL_02935_03068"
    if 3069 <= sol <= 3192: return "SOL_03069_03192"
    if 3193 <= sol <= 3289: return "SOL_03193_03289"
    if 3290 <= sol <= 3423: return "SOL_03290_03423"
    if 3424 <= sol <= 3547: return "SOL_03424_03547"
    if 3548 <= sol <= 3644: return "SOL_03548_03644"
    if 3645 <= sol <= 3778: return "SOL_03645_03778"
    if 3779 <= sol <= 3902: return "SOL_03779_03902"
    if 3903 <= sol <= 3999: return "SOL_03903_03999"
    if 4000 <= sol <= 4133: return "SOL_04000_04133"
    if 4134 <= sol <= 4257: return "SOL_04134_04257"
    if 4258 <= sol <= 4354: return "SOL_04258_04354"
    if 4355 <= sol <= 4488: return "SOL_04355_04488"
    if 4489 <= sol <= 4612: return "SOL_04489_04612"
    if 4613 <= sol <= 4709: return "SOL_04613_04709"  # Fixed typo
    return None

def run_curiosity_ultimate_pipeline():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Clear out any old bad runs with 0.0 Ls entries so we can rewrite them cleanly
    cursor.execute("DELETE FROM environmental_data WHERE source='Curiosity' AND ls=0.0")
    conn.commit()
    
    # 2. Map existing inventory to avoid repeating work
    cursor.execute("SELECT DISTINCT sol FROM environmental_data WHERE source='Curiosity'")
    finished_sols = {row[0] for row in cursor.fetchall()}
    print(f"📊 Current database inventory: {len(finished_sols)} clean Sols.")

    new_saved_count = 0
    target_new_limit = 4000
    session = requests.Session()

    print("🚀 Starting Vocal Martian Pipeline...\n")

    for sol_num in range(1, 4710):
        if new_saved_count >= target_new_limit:
            print(f"\n🎯 Batch limit reached! Added {new_saved_count} Sols this run.")
            break
            
        if sol_num in finished_sols:
            print(f"ℹ️ Skipping Sol {sol_num} (Already exists in SQLite)")
            continue

        range_folder = get_nasa_range_folder(sol_num)
        if not range_folder: continue

        sol_padded = f"SOL{str(sol_num).zfill(5)}"
        folder_url = f"{BASE_URL}{range_folder}/{sol_padded}/"
        
        print(f"📡 Requesting index for Sol {sol_num}...", end="\r")
        sys.stdout.flush()

        try:
            r = session.get(folder_url, timeout=4)
            if r.status_code != 200:
                print(f"❌ Sol {sol_num} -> NASA directory returned HTTP {r.status_code}")
                continue
            
            filenames = re.findall(r'href="([^"]*(?:RMD|RNV)[^"]*\.TAB)"', r.text, re.IGNORECASE)
            if not filenames:
                print(f"❌ Sol {sol_num} -> Found folder, but no RMD or RNV data file inside.")
                continue
                
            file_url = f"{folder_url}{filenames[0]}"
            print(f"⚡ Streaming data for Sol {sol_num}...", end="\r")
            sys.stdout.flush()
            
            with session.get(file_url, stream=True, timeout=6) as data_r:
                if data_r.status_code not in [200, 206]:
                    print(f"❌ Sol {sol_num} -> Failed to stream target data file.")
                    continue
                
                found_valid_row = False
                for raw_line in data_r.iter_lines():
                    if not raw_line: continue
                    
                    clean_line = raw_line.decode('utf-8').strip()
                    parts = [p.strip().replace('"', '') for p in clean_line.split(',')]
                    
                    if len(parts) >= 30:
                        found_pressure = None
                        ls = None
                        
                        # Dynamic Matrix Scanning Loop
                        for item in parts:
                            if "UNK" in item or "NULL" in item or not item:
                                continue
                            try:
                                val = float(item)
                                
                                # 1. Check if it fits the strict atmospheric pressure window
                                if 600.0 <= val <= 1000.0 and found_pressure is None:
                                    found_pressure = val
                                    continue
                                
                                # 2. Check if it fits the orbital solar longitude window
                                # (We skip clean integers like 1.0 or 2.0 to avoid mixing up status flags)
                                if 0.0 <= val <= 360.0 and ls is None and "." in item:
                                    # Secondary protection: avoid grabbing temperature values
                                    if found_pressure and abs(val - found_pressure) < 10.0:
                                        continue
                                    ls = val
                            except:
                                continue
                        
                        ts = parts[1] if (len(parts) > 1 and "UNK" not in parts[1]) else None
                        
                        # Commit data if any viable tracking metric is pulled
                        if ls is not None or found_pressure is not None:
                            cursor.execute("""
                                INSERT OR IGNORE INTO environmental_data 
                                (source, body, sol, ls, timestamp_utc, pressure, temp_air, temp_ground, humidity) 
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """, ('Curiosity', 'Mars', sol_num, ls, ts, found_pressure, None, None, None))
                            conn.commit()
                            
                            pressure_display = f"{found_pressure} Pa" if found_pressure else "NaN"
                            ls_display = f"{ls}°" if ls is not None else "NaN"
                            print(f"✅ SAVED -> Sol {sol_num} | Pressure: {pressure_display} | Ls: {ls_display}")
                            
                            found_valid_row = True
                            new_saved_count += 1
                            break
                            
                if not found_valid_row:
                    print(f"⚠️ Sol {sol_num} -> Checked file, but data arrays were entirely blank.")
                    
        except Exception as e:
            error_msg = str(e) if str(e) else "Empty file contents / initialization line skipped"
            print(f"💥 Sol {sol_num} -> {error_msg}")
            continue

    conn.close()
    print(f"\n🎉 ALL DONE! Mission Successful.")

if __name__ == "__main__":
    run_curiosity_ultimate_pipeline()
#python3 "/Volumes/Expansion Drive/starbleep_backend/backend/msl_pipeline.py"