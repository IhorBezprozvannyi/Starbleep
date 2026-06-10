import pandas as pd
import ftplib
import io
import json
import time
import os


#archive
# Connection settings for Perseverance (MEDA)
FTP_HOST = "atmos.nmsu.edu"

def start_vacuum():
    print("Connecting to Mars PDS...")
    try:
        # Increase timeout to 60 seconds
        ftp = ftplib.FTP(FTP_HOST, timeout=60) 
        ftp.login()
        # Enable Passive Mode (CRITICAL for modern routers)
        ftp.set_pasv(True) 
        return ftp
    except Exception as e:
        print(f"Connection failed: {e}")
        return None

def extract_sol_data(ftp, sol_folder):
    """Goes inside a Sol folder and pulls Pressure data."""
    ftp.cwd(sol_folder)
    files = ftp.nlst()
    
    ps_file = [f for f in files if 'DER_PS' in f and f.endswith('.CSV')]
    
    sol_results = {"sol": sol_folder, "data": []}
    
    if ps_file:
        print(f"  Found Pressure data: {ps_file[0]}")
        r = io.BytesIO()
        ftp.retrbinary(f"RETR {ps_file[0]}", r.write)
        r.seek(0)
        
        df = pd.read_csv(r, usecols=['LMST', 'PRESSURE'])
        # Thin data: 1 reading per minute
        thinned_df = df.iloc[::60] 
        sol_results["data"] = thinned_df.to_dict(orient='records')

    ftp.cwd("..") 
    return sol_results

def main():
    all_data = []
    done_sols = []

    # 1. Load what we already have to resume correctly
    if os.path.exists("per_ps.json"):
        try:
            with open("per_ps.json", "r") as f:
                all_data = json.load(f)
                done_sols = [item['sol'] for item in all_data]
                print(f"Resuming: Already have {len(done_sols)} Sols.")
        except json.JSONDecodeError:
            pass

    ftp = start_vacuum()
    if not ftp: return

    # ALL BLOCKS available for MEDA Derived Environmental Data
    ALL_BLOCKS = [
"/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_0180_0299/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_0300_0419/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_0420_0539/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_0540_0659/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_0660_0779/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_0780_0899/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_0900_1019/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_1020_1139/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_1140_1259/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_1260_1379/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_1380_1499/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_1500_1619/",
    "/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/sol_1620_1739/"
    ]
    

    try:
        for block in ALL_BLOCKS:
            print(f"\n--- Entering Block: {block.split('/')[-2]} ---")
            
            # Keep trying to enter the block until successful
            connected = False
            while not connected:
                try:
                    ftp.cwd(block)
                    connected = True
                except Exception:
                    print("Connection lost. Reconnecting in 10 seconds...")
                    time.sleep(10)
                    ftp = start_vacuum()
            
            sol_folders = sorted([f for f in ftp.nlst() if f.startswith('sol_')])
            
            for sol in sol_folders:
                if sol in done_sols:
                    continue 
                
                print(f"New Data -> {sol}")
                try:
                    result = extract_sol_data(ftp, sol)
                    if result["data"]:
                        all_data.append(result)
                    
                    with open("per_ps.json", "w") as f:
                        json.dump(all_data, f, indent=4)
                    
                    time.sleep(2.0) # Slightly longer pause for stability
                except Exception as e:
                    print(f"Error on {sol}: {e}. Retrying connection...")
                    time.sleep(5)
                    ftp = start_vacuum()
                    ftp.cwd(block)

    # Inside your main() function, where it retries the connection:
                    if ftp is None:
                        print("Connection still down. Waiting 30 seconds before trying again...")
                        time.sleep(30)
                    continue  # This skips the rest of the loop and tries start_vacuum() again
                    
        print("\nMISSION COMPLETE: All available blocks processed!")
        print(f"Total Sols now in database: {len(all_data)}")

    finally:
        if ftp: 
            ftp.quit()
            print("NASA connection closed.")
    
if __name__ == "__main__":
    main()