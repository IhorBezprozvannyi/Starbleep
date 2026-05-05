import sqlite3
import os

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "starbleep.db")

def update_metadata():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ONLY your four rovers
    # Format: (Name, Target, NAIF_ID, Type, Status, Launch_Year, Description)
    rover_fleet = [
        ('Curiosity', 'Mars', '-76', 'Rover', 'Active', 2011, 
         'Exploring Gale Crater to determine if Mars was ever habitable for microbial life.'),
        
        ('Perseverance', 'Mars', '-168', 'Rover', 'Active', 2020, 
         'Searching for signs of ancient life and collecting rock samples in Jezero Crater.'),
        
        ('Opportunity', 'Mars', '-254', 'Rover', 'Inactive', 2003, 
         'The marathon rover that proved Mars once had liquid water; lasted 15 years.'),
        
        ('Spirit', 'Mars', '-253', 'Rover', 'Inactive', 2003, 
         'Explored Gusev Crater and discovered evidence of ancient hydrothermal activity.')
    ]

    # This clears any old mission info and puts in the fresh 4
    cursor.execute("DELETE FROM mission_details")
    
    cursor.executemany("""
        INSERT INTO mission_details 
        (name, target, naif_id, type, status, launch_year, description) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rover_fleet)

    conn.commit()
    conn.close()
    print("✅ Metadata Sync Complete: Curiosity, Perseverance, Spirit, & Opportunity are ready.")

if __name__ == "__main__":
    update_metadata()