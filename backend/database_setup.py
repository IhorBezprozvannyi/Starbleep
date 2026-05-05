import sqlite3

conn = sqlite3.connect('starbleep.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS mission_details")
# Create tables
cursor.execute('CREATE TABLE IF NOT EXISTS mission_details (id INTEGER PRIMARY KEY, name TEXT UNIQUE, celestial_body TEXT, mission_type TEXT, status TEXT, launch_year INTEGER)')
cursor.execute('CREATE TABLE IF NOT EXISTS rover_images (id INTEGER PRIMARY KEY, rover_name TEXT, earth_date TEXT, sol INTEGER, img_url TEXT UNIQUE, camera TEXT)')

# Expanded List: 10 Mars + 10 Moon
missions = [
    # --- MARS (10) ---
    ('Curiosity', 'Mars', 'Rover', 'Active', 2011),
    ('Perseverance', 'Mars', 'Rover', 'Active', 2020),
    ('Opportunity', 'Mars', 'Rover', 'Inactive', 2003),
    ('Spirit', 'Mars', 'Rover', 'Inactive', 2003),
    ('Sojourner', 'Mars', 'Rover', 'Inactive', 1996),
    ('Phoenix', 'Mars', 'Lander', 'Inactive', 2007),
    ('InSight', 'Mars', 'Lander', 'Inactive', 2018),
    ('Viking 1', 'Mars', 'Lander', 'Inactive', 1975),
    ('Viking 2', 'Mars', 'Lander', 'Inactive', 1975),
    ('Zhurong', 'Mars', 'Rover', 'Inactive', 2020),
    
    # --- MOON (10) ---
    ('LRO', 'Moon', 'Orbiter', 'Active', 2009),
    ('Apollo 11', 'Moon', 'Lander', 'Inactive', 1969),
    ('Apollo 12', 'Moon', 'Lander', 'Inactive', 1969),
    ('Apollo 14', 'Moon', 'Lander', 'Inactive', 1971),
    ('Apollo 15', 'Moon', 'Rover', 'Inactive', 1971),
    ('Apollo 16', 'Moon', 'Rover', 'Inactive', 1972),
    ('Apollo 17', 'Moon', 'Rover', 'Inactive', 1972),
    ('Yutu-2', 'Moon', 'Rover', 'Active', 2018),
    ('Chandrayaan-3', 'Moon', 'Lander/Rover', 'Inactive', 2023),
    ('Luna 25', 'Moon', 'Lander', 'Inactive', 2023)
]

cursor.executemany('INSERT OR IGNORE INTO mission_details (name, celestial_body, mission_type, status, launch_year) VALUES (?, ?, ?, ?, ?)', missions)

conn.commit()
conn.close()
print("!!!!!!! Database updated with 20 missions (10 Mars, 10 Moon)!!!!!!!!")