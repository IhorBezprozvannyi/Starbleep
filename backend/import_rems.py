import sqlite3

def import_rems_data(file_content, rover_id=2):
    conn = sqlite3.connect('starbleep.db')
    cursor = conn.cursor()
    
    lines = file_content.splitlines()
    for line in lines:
        parts = line.split(',')
        
        # We need at least 38 columns to reach the pressure reading
        if len(parts) > 37:
            pressure = parts[37].strip()
            # If it's a valid number, save it
            if pressure != "UNK" and pressure != "NULL":
                sol = parts[0].strip() # Assuming column 0 is the ID/Sol-related SCLK
                # Your SQL insertion here
                # cursor.execute("INSERT INTO meda_ps_data (sol, pressure, rover_id) VALUES (?, ?, ?)", 
                #                (sol, pressure, rover_id))
    
    conn.commit()
    conn.close()
    print("Import complete!")