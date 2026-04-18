#puts initial data into databse file starbleep.db

import sqlite3

def seed_rover_dashboard():
    conn = sqlite3.connect('starbleep.db')
    cursor = conn.cursor()

    # Create the specialized table for this UI
    cursor.execute('DROP TABLE IF EXISTS rover_telemetry')
    cursor.execute('''CREATE TABLE rover_telemetry (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   mission_id INTEGER,
                   sol INTEGER,
                   earth_date TEXT,
                   lat REAL,
                   lon REAL,
                   point_type TEXT, -- 'landing', 'failure', 'current', or 'path'
                   total_distance REAL,
                   photos_count INTEGER,
                   failure_note TEXT)''')

    # Seed data for Perseverance based on your image
    # (mission_id, sol, date, lat, lon, type, dist, photos, failure)
    percy_data = [
        (1, 0, '2021-02-18', 18.444, 77.450, 'landing', 0.0, 142, None),
        (1, 15, '2021-03-05', 18.445, 77.451, 'failure', 0.5, 210, 'Wheel slip detected'),
        (1, 30, '2021-03-20', 18.447, 77.453, 'failure', 1.2, 450, 'Sensor recalibration'),
        (1, 50, '2021-04-10', 18.450, 77.456, 'current', 2.8, 890, None)
    ]

    cursor.executemany('''INSERT INTO rover_telemetry 
        (mission_id, sol, earth_date, lat, lon, point_type, total_distance, photos_count, failure_note) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', percy_data)

    conn.commit()
    conn.close()
    print("Dashboard data is ready!")

seed_rover_dashboard()