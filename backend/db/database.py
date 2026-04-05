#define the tables (Mission, RoverData, OrbiterData, SensorReading)
from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Mission(Base) : #Mission table as py class
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    target = Column(String) #which planet
    naif_id = Column(String) #nasa id number for tracking
    type = Column(String) #orbiter, rover, lander
    status = Column(String) #active or inactive
    launch_date = Column(String) #when it left earth
    description = Column(String) #a short bio of the mission
    
