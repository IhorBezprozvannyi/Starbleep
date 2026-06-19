import sqlite3
conn = sqlite3.connect("starbleep.db")
cursor = conn.cursor()

# Get all unique missions
cursor.execute("SELECT DISTINCT mission_name FROM rover_telemetry")
missions = [row[0] for row in cursor.fetchall()]

for mission in missions:
    # Fetch all data for this rover in order
    cursor.execute("SELECT id, lat, lon FROM rover_telemetry WHERE mission_name = ? ORDER BY sol ASC", (mission,))
    data = cursor.fetchall()
    
    dist = 0
    prev_lat, prev_lon = None, None
    for row in data:
        row_id, lat, lon = row
        if prev_lat is not None:
            # Simple Pythagorean distance
            dist += ((lat - prev_lat)**2 + (lon - prev_lon)**2)**0.5
        
        # Update the database with distance in KM (assuming meters / 1000)
        cursor.execute("UPDATE rover_telemetry SET total_distance_km = ? WHERE id = ?", (round(dist / 1000, 3), row_id))
        prev_lat, prev_lon = lat, lon

conn.commit()
conn.close()
print("All null values have been filled!")