from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

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

@app.get("/missions/{rover_name}/sensors/{sol}")
async def get_rover_sensors(rover_name: str, sol: int):
    # Choose database: Curiosity uses its own file, others use starbleep.db
    target_db = CURIOSITY_DB if rover_name.lower() == "curiosity" else DB_PATH
    
    conn = sqlite3.connect(target_db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Standardized query format including all your requested fields
    query = "SELECT sol, sclk, ltst, lmst, pressure FROM meda_ps_data WHERE sol = ? ORDER BY sclk ASC"
    
    try:
        cursor.execute(query, (sol,))
        rows = [dict(row) for row in cursor.fetchall()]
    except sqlite3.OperationalError:
        # Fallback if the table doesn't exist for a specific rover
        rows = []
    
    conn.close()
    return {"timeline": rows}

@app.get("/missions/list")
def list_rovers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT mission_name FROM rover_telemetry")
    rovers = [row[0] for row in cursor.fetchall()]
    # Ensure Curiosity is in the list
    if "curiosity" not in [r.lower() for r in rovers]:
        rovers.append("Curiosity")
    conn.close()
    return rovers

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