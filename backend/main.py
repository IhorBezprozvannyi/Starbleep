from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sqlite3
import os

app = FastAPI()

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "starbleep.db")

@app.get("/missions/{rover_name}/path")
def get_rover_path(rover_name: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Fetch all points for the specific rover, ordered by time
    cursor.execute("""
        SELECT earth_date, lat, lon 
        FROM rover_telemetry 
        WHERE mission_name = ? COLLATE NOCASE 
        ORDER BY earth_date ASC
    """, (rover_name,))
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return {"error": f"No data found for {rover_name}. Run the import script!"}
        
    return [dict(row) for row in rows]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body style="font-family: sans-serif; text-align: center; padding: 50px; background: #1a1a1a; color: white;">
            <h1>🚀 Starbleep Mars API</h1>
            <p>Curiosity: <a style="color: #4cc9f0;" href="/missions/curiosity/path">/missions/curiosity/path</a></p>
            <p>Perseverance: <a style="color: #4cc9f0;" href="/missions/perseverance/path">/missions/perseverance/path</a></p>
        </body>
    </html>
    """