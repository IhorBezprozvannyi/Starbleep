import sqlite3
import os

# Use the same path as your main.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "starbleep.db")

def setup_missions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            launch_year INTEGER,
            mission_type TEXT,
            status TEXT,
            celestial_body TEXT
        )
    """)
    
    # The full list of missions
    missions_to_add = [
        ("Perseverance", 2020, "Rover", "Active", "Mars"),
        ("Curiosity", 2011, "Rover", "Active", "Mars"),
        ("Spirit", 2003, "Rover", "Inactive", "Mars"),
        ("Opportunity", 2003, "Rover", "Inactive", "Mars"),
        ("Lunar Reconnaissance Orbiter", 2009, "Orbiter", "Active", "Moon"),
        ("Apollo 11", 1969, "Lander", "Inactive", "Moon")
    ]
    
    # Insert them
    cursor.executemany("""
        INSERT OR IGNORE INTO missions (name, launch_year, mission_type, status, celestial_body) 
        VALUES (?, ?, ?, ?, ?)
    """, missions_to_add)
    
    conn.commit()
    conn.close()
    print("Database updated with mission fleet!")

if __name__ == "__main__":
    setup_missions()