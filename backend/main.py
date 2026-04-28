from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI()

# --- THE CRUCIAL BRIDGE (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "starbleep.db")

@app.get("/missions/{rover_name}/path")
def get_rover_path(rover_name: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # This works for ANY name you type in the URL automatically!
    cursor.execute("""
        SELECT earth_date, lat, lon 
        FROM rover_telemetry 
        WHERE mission_name = ? COLLATE NOCASE 
        ORDER BY earth_date ASC
    """, (rover_name,))
    
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return {"error": f"No data found for {rover_name}. Check the spelling or run the import script!"}
        
    return [dict(row) for row in rows]

@app.get("/missions/all")
def get_all_missions():
    """Returns every mission for Ihor's filter/gallery page"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mission_details")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body style="font-family: 'Courier New', monospace; text-align: center; padding: 50px; background: #0b0d17; color: #e0e0e0;">
            <h1 style="color: #ff4d4d;">🚀 Starbleep Mars Fleet API</h1>
            <p>Global Registry: <a style="color: #4cc9f0;" href="/missions/all">/missions/all</a></p>
            <hr style="border: 1px solid #333; width: 50%;">
            <h3>📡 Individual Coordinate Feeds</h3>
            <p>Curiosity: <a style="color: #4cc9f0;" href="/missions/curiosity/path">/path</a></p>
            <p>Perseverance: <a style="color: #4cc9f0;" href="/missions/perseverance/path">/path</a></p>
            <p>Spirit: <a style="color: #4cc9f0;" href="/missions/spirit/path">/path</a></p>
            <p>Opportunity: <a style="color: #4cc9f0;" href="/missions/opportunity/path">/path</a></p>
            <p style="color: #00ff00; margin-top: 40px; font-size: 0.8em;">CORS Bridge: 🟢 Online</p>
        </body>
    </html>
    """