from backend.db.database import SessionLocal, Base, engine
from backend.db.models import Mission

Base.metadata.create_all(bind=engine)

missions = [
    {
        "name": "LRO",
        "agency": "NASA",
        "launch_date": "2009-06-18",
        "status": "active",
        "description": "Lunar Reconnaissance Orbiter, polar orbit ~50km, 1000kg, payload instruments list..."
    },
    {
        "name": "Chandrayaan-1",
        "agency": "ISRO",
        "launch_date": "2008-10-22",
        "status": "radar_reconstructed",
        "description": "India’s first Moon orbiter, mission lasted 312 days, trajectory extrapolated to 2022."
    },
    {
        "name": "GRAIL-A",
        "agency": "NASA",
        "launch_date": "2011-09-10",
        "status": "impacted",
        "description": "Twin spacecraft Ebb/Flow, gravity mapping, deorbited Dec 2012."
    }
]

db = SessionLocal()

for m in missions:
    mission = Mission(**m)
    db.add(m)

db.commit()
db.close()
print("Missions added!")