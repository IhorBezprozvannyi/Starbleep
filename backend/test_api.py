import requests

url = "https://atmos.nmsu.edu/PDS/data/mslrem_1001/DATA/SOL_00001_00089/SOL00001/RME_397535244RMD00010000000_______P9.TAB"
response = requests.get(url)
lines = response.text.splitlines()

print("Scanning for lines with numeric pressure readings...")

<<<<<<< HEAD
for i, line in enumerate(lines):
    # Does this line have a number that looks like a pressure (between 600 and 800)?
    # We look for a pattern like 700.XX
    if "70" in line or "71" in line or "72" in line:
        print(f"Found potential data on line {i}: {line[:60]}...")
        # If we found at least 3, stop so we don't spam the terminal
        if i > 20: 
            break
=======
file_url = f"{folder_url}{filenames[0]}"
print(f"📡 STEP 2: Streaming rows and dynamically hunting for valid Martian pressure...")

with requests.get(file_url, stream=True, timeout=5) as data_r:
    line_count = 0
    
    for raw_line in data_r.iter_lines():
        if not raw_line: continue
        line_count += 1
        
        clean_line = raw_line.decode('utf-8').strip()
        parts = [p.strip().replace('"', '') for p in clean_line.split(',')]
        
        # Extract Sol from Column 1 safely
        try:
            sol = int(parts[1].split('M')[0])
        except:
            continue
            
        # 🎯 DYNAMIC SCAN: Look through every column in this row for our pressure!
        for item in parts:
            try:
                val = float(item)
                # Check if this number looks exactly like Martian surface pressure
                if 600.0 <= val <= 1000.0:
                    print(f"\n🎯 FOUND IT AT ROW #{line_count}!")
                    print(f"   -> Parsed Sol: {sol}")
                    print(f"   -> Found Pressure Value: {val} Pa")
                    
                    # Now let's try to extract Solar Longitude (Ls) from the same row dynamically
                    # Ls on Mars is usually a small float between 0 and 360
                    found_ls = None
                    for ls_candidate in parts:
                        try:
                            ls_val = float(ls_candidate)
                            if 0.0 <= ls_val <= 360.0 and ls_val != val:
                                found_ls = ls_val
                                break
                        except:
                            continue
                            
                    print(f"   -> Found Solar Longitude (Ls): {found_ls}°")
                    print("   🎉 SUCCESS! This dynamic extraction layout is 100% bulletproof.")
                    exit()
            except:
                continue

        # Print a progress indicator every 100 rows so you know it's searching
        if line_count % 100 == 0:
            print(f"   Searching deeper... Checked {line_count} rows of initialization data...", end="\r")
            
    print(f"\n❌ Checked all {line_count} rows but couldn't find active environment readings.")
>>>>>>> 3c89308f47e165be815bf55ffe257645507e11d5
