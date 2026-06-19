import pandas as pd
import sqlite3
import io
import requests

# The NASA PDS URL
BASE_URL = "https://pds-geosciences.wustl.edu/mer/mer1_mer2-m-pancam-5-atmos-opacity-v1/merao_1xxx/data/"

def fetch_and_ingest(filename):
    print(f"Streaming {filename}...")
    
    response = requests.get(BASE_URL + filename)
    if response.status_code != 200:
        print(f"Error {response.status_code}: Could not reach {filename}")
        return

    # Process content: Skip 8 lines of metadata comments
    content = response.text
    data = "\n".join(content.splitlines()[8:])
    
    df = pd.read_csv(io.StringIO(data))
    df.columns = df.columns.str.strip()
    
    # Filter valid data (TAU > 0)
    df = df[df['TAU'] > 0]
    
    # Add metadata columns
    df['ROVER'] = 'Opportunity' if filename.startswith('1') else 'Spirit'
    df['FILTER'] = 'Left_440nm' if '440' in filename else 'Right_880nm'
    
    # Store in database
    conn = sqlite3.connect("mer_data.db")
    df.to_sql('atmospheric_opacity', conn, if_exists='append', index=False)
    conn.close()
    
    print(f"Success: Added {len(df)} rows.")

# List the files you want to include
files_to_process = [
    "1tau440_5106_20181207a.tab", 
    "1tau880_5106_20181207a.tab",
    "2tau440_2209_20110214a.tab", 
    "2tau880_2209_20110214a.tab"
]

for f in files_to_process:
    fetch_and_ingest(f)

print("\nIngestion Complete! Data is ready in 'mer_data.db'.")