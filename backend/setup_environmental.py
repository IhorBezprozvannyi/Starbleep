import sqlite3

def setup_env():
    conn = sqlite3.connect('starbleep.db')
    cursor = conn.cursor()
    
    # This table handles ANY rover on ANY body
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS environmental_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,          -- 'Perseverance', 'Curiosity', 'LRO'
            body TEXT,            -- 'Mars', 'Moon'
            sol INTEGER,          -- Martian Sol or Lunar Cycle
            ls REAL,              -- Solar Longitude (Season) - CRITICAL for analysis
            timestamp_utc TEXT,
            pressure REAL,        -- Pascals
            temp_air REAL,        -- Celsius
            temp_ground REAL,     -- Celsius
            humidity REAL,
            UNIQUE(source, sol, timestamp_utc)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("🚀 Universal Environmental Table Ready!")

if __name__ == "__main__":
    setup_env()