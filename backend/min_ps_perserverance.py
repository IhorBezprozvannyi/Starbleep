import sqlite3

def create_daily_summary_fast():
    conn = sqlite3.connect("starbleep.db")
    cursor = conn.cursor()
    
    print("Calculating daily averages inside the database (this is faster)...")
    
    # 1. Create the table structure first
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_stats (
            sol INTEGER PRIMARY KEY,
            avg_pressure REAL,
            min_pressure REAL,
            max_pressure REAL
        )
    """)
    
    # 2. Perform the calculation and insert in one go
    # This avoids loading everything into RAM
    query = """
    INSERT INTO daily_stats (sol, avg_pressure, min_pressure, max_pressure)
    SELECT sol, AVG(pressure), MIN(pressure), MAX(pressure)
    FROM meda_ps_data
    GROUP BY sol
    ORDER BY sol ASC
    """
    
    try:
        cursor.execute(query)
        conn.commit()
        print("Done! 'daily_stats' table created.")
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_daily_summary_fast()