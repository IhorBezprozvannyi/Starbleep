# FastAPI app. what starts my api server (uvicorn main:app)
from fastapi import FastAPI
import sqlite3 

app =FastAPI() #initialise

@app.get("/missions") #defining the get route for url
def get_missions(target:str = None) : 

    conn = sqlite3.connect('starbleep.db') #open connection
    conn.row_factory = sqlite3.Row #return data as dictonaires not tuples
    cursor = conn.cursor() #create cursor object to execute SQL commands

    if target  : 
        cursor.execute("SELECT * FROM missions WHERE target = ? COLLATE NOCASE", (target,)) #? for preventing sql injection, and comma to tell its tuple with one item
    else : 
        cursor.execute("SELECT * FROM missions") #if no target specified, return all missions

    rows = cursor.fetchall() #fetch all results
    conn.close() #close connection
    return [dict(row) for row in rows] #convert databse rows in list of dictionaries, fastapi will convert the list into json for ihor



from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>Starbleep API</title>
            <style>
                body { font-family: sans-serif; text-align: center; padding: 50px; background: #0b0d17; color: white; }
                h1 { color: #4cc9f0; }
                a { color: #f72585; text-decoration: none; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Starbleep Backend</h1>
            <p>View the data: <a href="/missions">/missions</a></p>
            <p>Interactive Docs: <a href="/docs">/docs</a></p>
        </body>
    </html>
    """