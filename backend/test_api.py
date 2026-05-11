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

