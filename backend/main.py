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

# Database path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "starbleep.db")

# --- 1. MISSION REGISTRY ---
@app.get("/missions/all")
async def get_all_missions(body: str = None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    if body:
        cursor.execute("SELECT * FROM mission_details WHERE LOWER(celestial_body) = LOWER(?)", (body,))
    else:
        cursor.execute("SELECT * FROM mission_details")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --- 2. TELEMETRY FEED (Paths) ---
@app.get("/missions/{rover_name}/path")
def get_rover_path(rover_name: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT earth_date, sol, lat, lon, total_distance_km, photos_taken, event_log
        FROM rover_telemetry 
        WHERE mission_name = ? COLLATE NOCASE 
        ORDER BY earth_date ASC
    """, (rover_name,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return {"error": f"No telemetry data found for {rover_name}"}
    return [dict(row) for row in rows]

# --- 3. IMAGE GALLERY FEED ---
@app.get("/missions/{rover_name}/images")
async def get_rover_images(rover_name: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rover_images WHERE rover_name = ? COLLATE NOCASE", (rover_name,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return {"error": f"No images found for {rover_name}"}
    return [dict(row) for row in rows]

# --- 4. THE FULL DASHBOARD ---
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <body style="font-family: 'Courier New', monospace; padding: 50px; background: #0b0d17; color: #e0e0e0; line-height: 1.6;">
            <div style="max-width: 800px; margin: auto; text-align: center;">
                <h1 style="color: #ff4d4d; border-bottom: 2px solid #333; padding-bottom: 20px;">🚀 Starbleep Fleet Command</h1>
                <p>Global Mission Registry: <a style="color: #4cc9f0;" href="/missions/all">/missions/all</a></p>
                
                <div style="display: flex; justify-content: space-around; text-align: left; margin-top: 30px;">
                    <div>
                        <h3 style="color: #f72585;">🔴 MARS ROVERS</h3>
                        <p><b>Curiosity:</b> <a style="color: #4cc9f0;" href="/missions/curiosity/path">Path</a> | <a style="color: #4cc9f0;" href="/missions/curiosity/images">Images</a></p>
                        <p><b>Perseverance:</b> <a style="color: #4cc9f0;" href="/missions/perseverance/path">Path</a> | <a style="color: #4cc9f0;" href="/missions/perseverance/images">Images</a></p>
                        <p><b>Spirit:</b> <a style="color: #4cc9f0;" href="/missions/spirit/path">Path</a> | <a style="color: #4cc9f0;" href="/missions/spirit/images">Images</a></p>
                        <p><b>Opportunity:</b> <a style="color: #4cc9f0;" href="/missions/opportunity/path">Path</a> | <a style="color: #4cc9f0;" href="/missions/opportunity/images">Images</a></p>
                    </div>
                    <div>
                        <h3 style="color: #4361ee;">⚪ MOON MISSIONS</h3>
                        <p><b>Apollo 11:</b> <a style="color: #4cc9f0;" href="/missions/apollo%2011/images">Images</a></p>
                        <p><b>LRO:</b> <a style="color: #4cc9f0;" href="/missions/lro/images">Images</a></p>
                        <p><b>Yutu-2:</b> <a style="color: #4cc9f0;" href="/missions/yutu-2/images">Images</a></p>
                    </div>
                </div>

                <hr style="border: 1px solid #333; margin-top: 40px;">
                <p style="color: #00ff00; font-size: 0.8em;">Status: 10/10 Missions Active in API 🟢</p>
            </div>
        </body>
    </html>
    """