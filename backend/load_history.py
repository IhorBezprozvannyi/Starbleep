import pandas as pd
import sqlite3
import requests
from bs4 import BeautifulSoup
import io
import time

BASE_URL = "https://atmos.nmsu.edu/PDS/data/PDS4/Mars2020/mars2020_meda/data_derived_env/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_links(url):
    """Fetches all links from a directory page."""
    try:
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [a['href'] for a in soup.find_all('a') if a['href'].endswith('/') and 'Parent' not in a.text]
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return []

def get_ps_csv_url(folder_url):
    """Finds the correct PS CSV file in a folder regardless of version number."""
    try:
        response = requests.get(folder_url, headers=HEADERS)
        soup = BeautifulSoup(response.text, 'html.parser')
        for a in soup.find_all('a'):
            href = a['href']
            # Looks for files matching the PS pattern
            if href.startswith("WE__") and "DER_PS" in href and href.endswith(".CSV"):
                return folder_url + href
        return None
    except Exception:
        return None

def fetch_all():
    conn = sqlite3.connect("perseverance.db")
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS meda_ps_data 
                      (sclk, lmst, ltst, pressure, pressure_uncertainty, transducer, sol)''')
    
    # Get existing sols to skip them
    cursor.execute("SELECT DISTINCT sol FROM meda_ps_data")
    existing_sols = {row[0] for row in cursor.fetchall()}
    
    buckets = get_links(BASE_URL)
    
    for bucket in buckets:
        print(f"Entering bucket: {bucket}")
        sol_folders = get_links(BASE_URL + bucket)
        
        for sol_folder in sol_folders:
            # Extract sol number from folder name
            try:
                sol_id = int(sol_folder.replace('/', '').split('_')[1])
            except (ValueError, IndexError):
                continue
                
            if sol_id in existing_sols:
                continue 
            
            # Dynamically find the CSV
            csv_url = get_ps_csv_url(BASE_URL + bucket + sol_folder)
            
            if csv_url:
                try:
                    resp = requests.get(csv_url, headers=HEADERS)
                    if resp.status_code == 200:
                        df = pd.read_csv(io.StringIO(resp.text))
                        df['sol'] = sol_id
                        df.columns = [c.lower() for c in df.columns]
                        
                        df.to_sql('meda_ps_data', conn, if_exists='append', index=False)
                        print(f"  --> Saved Sol {sol_id} from {csv_url.split('/')[-1]}")
                    else:
                        print(f"  --> Failed to download {csv_url}")
                except Exception as e:
                    print(f"  --> Error downloading {sol_id}: {e}")
            else:
                print(f"  --> No PS file found for Sol {sol_id}")
            
            time.sleep(0.2) # Polite delay
            
    conn.close()
    print("Done! Database is up to date.")

if __name__ == "__main__":
    fetch_all()