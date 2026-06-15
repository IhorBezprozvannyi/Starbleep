from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import json
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "starbleep.db")
CURIOSITY_DB = os.path.join(BASE_DIR, "curiosity.db")
PERSEVERANCE_DB = os.path.join(BASE_DIR, "perseverance.db")

# --- PATH ENDPOINT ---
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

@app.get("/missions/{rover_name}/path")
def get_rover_path(rover_name: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT earth_date, sol, lat, lon
        FROM rover_telemetry 
        WHERE mission_name = ? COLLATE NOCASE 
        ORDER BY earth_date ASC
    """, (rover_name,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# --- SENSOR ENDPOINT (DB + JSON FALLBACK) ---
@app.get("/missions/{rover_name}/sensors/{sol}")
async def get_rover_sensors(rover_name: str, sol: int):
    name = rover_name.lower()
    
    # 1. Point to the correct dedicated database
    if name == "curiosity":
        target_db = CURIOSITY_DB
    elif name == "perseverance":
        target_db = PERSEVERANCE_DB
    else:
        target_db = DB_PATH

    # 2. Try DB execution
    if os.path.exists(target_db):
        conn = sqlite3.connect(target_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT sol, sclk, ltst, lmst, pressure FROM meda_ps_data WHERE sol = ? ORDER BY sclk ASC", (sol,))
            rows = [dict(row) for row in cursor.fetchall()]
            conn.close()
            if rows: 
                return {"timeline": rows}
        except:
            conn.close()

    # 3. Fallback to JSON (Only if DB fails/is missing)
    if name == "perseverance" and os.path.exists("per_ps.json"):
        with open("per_ps.json", "r") as f:
            data = json.load(f)
            timeline = [item for item in data if item.get("sol") == sol]
            return {"timeline": timeline}
            
    return {"timeline": []}

# --- LIST ENDPOINT ---
@app.get("/missions/list")
def list_rovers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # If the table exists, pull from it; otherwise default list
    try:
        cursor.execute("SELECT DISTINCT mission_name FROM rover_telemetry")
        rovers = [row[0] for row in cursor.fetchall()]
    except:
        rovers = ["Perseverance", "Curiosity", "Spirit", "Opportunity"]
    
    if "Curiosity" not in rovers and "curiosity" not in [r.lower() for r in rovers]:
        rovers.append("Curiosity")
    conn.close()
    return rovers

@app.get("/missions/{rover_name}/sensors/{sol}/chart")
async def get_chart_data(rover_name: str, sol: int, step: int = 10):
    # 'step' defaults to 10, meaning it will grab every 10th row.
    # You can change this to 20 or 50 if the charts are still laggy.
    
    target_db = CURIOSITY_DB if rover_name.lower() == "curiosity" else PERSEVERANCE_DB
    
    if os.path.exists(target_db):
        conn = sqlite3.connect(target_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # This subquery assigns a number (1, 2, 3...) to every row in that Sol
        # Then the outer query picks only the rows where the number is divisible by your step
        query = """
            SELECT ltst, pressure FROM (
                SELECT ltst, pressure, ROW_NUMBER() OVER (ORDER BY sclk ASC) as rn
                FROM meda_ps_data 
                WHERE sol = ?
            ) WHERE rn % ? = 0
        """
        
        cursor.execute(query, (sol, step))
        rows = cursor.fetchall()
        conn.close()
        
        return {
            "labels": [row["ltst"] for row in rows],
            "data": [row["pressure"] for row in rows]
        }
    
    return {"labels": [], "data": []}

# --- DASHBOARD ---
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <style>
                body { background: #0b0d17; color: #e0e0e0; font-family: 'Courier New', monospace; padding: 40px; }
                .container { max-width: 900px; margin: auto; border: 1px solid #333; padding: 20px; }
                h1 { color: #ff4d4d; border-bottom: 1px solid #333; padding-bottom: 10px; }
                .rover-card { background: #161b22; padding: 15px; margin: 10px 0; border-left: 4px solid #4cc9f0; }
                a { color: #4cc9f0; text-decoration: none; margin-right: 15px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Starbleep Fleet Command</h1>
                <div id="fleet"></div>
            </div>
            <script>
                fetch('/missions/list')
                    .then(r => r.json())
                    .then(rovers => {
                        const container = document.getElementById('fleet');
                        rovers.forEach(r => {
                            let div = document.createElement('div');
                            div.className = 'rover-card';
                            div.innerHTML = `
                                <strong>${r.toUpperCase()}</strong><br>
                                <a href="/missions/${r}/path">View Telemetry Path</a>
                                <a href="/missions/${r}/sensors/1">View Sensor Data</a>
                            `;
                            container.appendChild(div);
                        });
                    });
            </script>
        </body>
    </html>
    """