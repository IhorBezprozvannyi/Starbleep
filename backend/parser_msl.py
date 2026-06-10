import requests

def get_sol_folder_prefix(sol):
    ranges = [1, 90, 180, 270, 360, 450, 584, 708, 805, 939, 1063, 1160, 1294, 1418, 1515, 
              1649, 1773, 1870, 2004, 2128, 2225, 2359, 2483, 2580, 2714, 2838, 2935, 
              3069, 3193, 3290, 3424, 3548, 3645, 3779, 3903, 4000, 4134, 4258, 4355, 4489, 4613]
    for i in range(len(ranges)-1):
        if ranges[i] <= sol < ranges[i+1]:
            return f"SOL_{ranges[i]:05d}_{ranges[i+1]-1:05d}"
    return "SOL_4613_9999"

def get_data_for_sol(sol_num):
    folder_prefix = get_sol_folder_prefix(sol_num)
    target_sol = f"SOL{sol_num:05d}"
    dir_url = f"https://atmos.nmsu.edu/PDS/data/mslrem_1001/DATA/{folder_prefix}/{target_sol}/"
    
    try:
        listing = requests.get(dir_url, timeout=10).text
        filename = next((line.split('"')[1] for line in listing.split() if "RMD" in line and ".TAB" in line), None)
        if not filename: return []

        data_resp = requests.get(f"{dir_url}{filename}", timeout=10)
        rows = []
        for line in data_resp.text.splitlines():
            cols = [c.strip().replace('"', '') for c in line.split(',')]
            if len(cols) < 5: continue # Skip empty/header rows

            # Intelligent categorization
            p, t, w = None, None, None
            for val in cols:
                try:
                    num = float(val)
                    if 500 < num < 1000: p = num      # Pressure
                    elif -130 < num < 30: t = num     # Temperature
                    elif 0 <= num < 50: w = num       # Wind Speed
                except: continue
            
            if p: # Only add row if we at least found a valid pressure
                rows.append({
                    "sclk": cols[0],
                    "lmst": cols[1],
                    "ltst": cols[2],
                    "pressure": p,
                    "air_temp": t,
                    "wind_speed": w
                })
        return rows
    except: return []