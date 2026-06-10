import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "starbleep.db")

def upgrade():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Adding the new columns to your existing table
    columns = [
        "sol INTEGER",
        "total_distance_km REAL",
        "photos_taken INTEGER",
        "event_log TEXT"
    ]
    
    for col in columns:
        try:
            cursor.execute(f"ALTER TABLE rover_telemetry ADD COLUMN {col}")
            print(f"✅ Added column: {col}")
        except sqlite3.OperationalError:
            print(f"⚠️ Column {col.split()[0]} already exists.")
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    upgrade()