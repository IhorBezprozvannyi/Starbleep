
import kagglehub
import os

# 1. This downloads the dataset structure to your cache
path = kagglehub.dataset_download("nikitamanaenkov/meda-mars-weather-and-atmosphere-sensor-data")

# 2. This FORCE PRINTS every single file name in that 6GB folder
print("\n--- SCANNING DATASET FILES ---")
file_count = 0
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".csv"):
            print(f"FILE FOUND: {file}")
            file_count += 1

print(f"\nTotal CSV files found: {file_count}")


import requests

url = "https://atmos.nmsu.edu/PDS/data/mslrem_1001/DATA/SOL_00001_00089/SOL00001/RME_397535244RMD00010000000_______P9.TAB"
response = requests.get(url)
lines = response.text.splitlines()

print("Scanning for lines with numeric pressure readings...")

for i, line in enumerate(lines):
    # Does this line have a number that looks like a pressure (between 600 and 800)?
    # We look for a pattern like 700.XX
    if "70" in line or "71" in line or "72" in line:
        print(f"Found potential data on line {i}: {line[:60]}...")
        # If we found at least 3, stop so we don't spam the terminal
        if i > 20: 
            break