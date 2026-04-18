import sqlite3
import os

# Use the same path as your main project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "starbleep.db")

def setup_mission_metadata():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create the table for the filters
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mission_details (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            target TEXT,
            naif_id TEXT,
            type TEXT,
            status TEXT,
            launch_year INTEGER,
            description TEXT
        )
    """)

    # 2. Insert the data for Ihor's filters
    missions = [
        ('Curiosity', 'Mars', 'MSL', 'Rover', 'Active', 2011, 'Exploring Gale Crater to study habitability.'),
        ('Perseverance', 'Mars', 'M2020', 'Rover', 'Active', 2020, 'Seeking signs of ancient life in Jezero Crater.'),
        ('Opportunity', 'Mars', 'MER-B', 'Rover', 'Inactive', 2003, 'Completed a 15-year mission in 2018.'),
        ('InSight', 'Mars', 'INSIGHT', 'Lander', 'Inactive', 2018, 'Studied the "inner space" of Mars.')
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO mission_details 
        (name, target, naif_id, type, status, launch_year, description) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, missions)

    conn.commit()
    conn.close()
    print("✅ Mission Metadata is ready!")

if __name__ == "__main__":
    setup_mission_metadata()