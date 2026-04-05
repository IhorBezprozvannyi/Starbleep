#puts initial data into databse file starbleep.db

import sqlite3


def seed_missions() : 
    conn = sqlite3.connect('starbleep.db') #connect to db file
    cursor = conn.cursor() #create cursor object to execute SQL commands
    cursor.execute('''DROP TABLE IF EXISTS missions''') #drop missions table if it exists to avoid duplicate entries
    cursor.execute('''CREATE TABLE IF NOT EXISTS missions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT UNIQUE,
                   target TEXT,
                   naif_id INTEGER,
                   type TEXT,
                   status TEXT,
                   launch_date TEXT,
                   description TEXT)''') #create missions table if it doesn't exist
                    
    missions = [
        ('Mars Reconnaisance Orbiter', 'Mars', -74, 'Orbiter', 'Active', '2005-08-12', 'MRO is a NASA mission that has been orbiting Mars since 2006, providing high-resolution imagery and data about the planet\'s surface and atmosphere.'),
        ('Lunar Reconnaisance Orbiter', 'Moon', 190, 'Orbiter', 'Active', '2009-06-18', 'LRO is a NASA mission that has been orbiting the Moon since 2009, providing detailed imagery and data about the lunar surface.'),
        ('Chandrayaan-1', 'Moon', -86, 'Orbiter', 'Inactive', '2008-10-22', 'Chandrayaan-1 was an Indian Space Research Organisation (ISRO) mission that orbited the Moon from 2008 to 2009, providing valuable data about the lunar surface and discovering water ice.'),
        ('Curiosity Rover', 'Mars', -76, 'Rover', 'Active', '2011-11-26', 'Curiosity is a NASA rover that has been exploring the surface of Mars since 2012, studying the planet\'s geology and climate to assess its past habitability.')
    ] 
    #executing the sql command to insert data into missions table. THE INSERT or Ignore will prevent duplicate errors, if by mistake run twice

    cursor.executemany(
        'INSERT OR IGNORE INTO missions (name, target, naif_id, type, status, launch_date, description) VALUES (?, ?, ?, ?, ?, ?, ?)''', 
        missions)

    conn.commit() #commit changes to db
    conn.close() #close connection to db
    print('Missions added to starbleep.db!')

if __name__ == "__main__":
    seed_missions() #run when executed