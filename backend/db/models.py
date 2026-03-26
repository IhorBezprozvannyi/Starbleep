#connects to the SQLite database.
from sqlalchemy import Column, Integer, String, Float
from db.database import Base

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    mission = Column(String)
    timestamp = Column(String)

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)

