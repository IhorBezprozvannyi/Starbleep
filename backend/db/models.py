#connects to the SQLite database.
from sqlalchemy import Column, Integer, String, Float, DateTime
from db.database import Base
from datetime import datetime

class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    mission = Column(String)
    timestamp = Column(String)

    x = Column(Float)
    y = Column(Float)
    z = Column(Float)


class MarsExpressHRSC(Base):
    __tablename__ = "mars_express_hrsc"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    observation_id = Column(String)
    start_time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    resolution = Column(Float)
    file_url = Column(String)
    file_size_mb = Column(Float)
    ingested_at = Column(DateTime, default=datetime.utcnow)


class MarsExpressOmega(Base):
    __tablename__ = "mars_express_omega"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    observation_id = Column(String)
    start_time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    wavelength_min = Column(Float)
    wavelength_max = Column(Float)
    file_url = Column(String)
    ingested_at = Column(DateTime, default=datetime.utcnow)


class MarsExpressMarsis(Base):
    __tablename__ = "mars_express_marsis"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    observation_id = Column(String)
    start_time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    frequency_mhz = Column(Float)
    penetration_depth_km = Column(Float)
    file_url = Column(String)
    ingested_at = Column(DateTime, default=datetime.utcnow)


class MarsExpressPfs(Base):
    __tablename__ = "mars_express_pfs"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    observation_id = Column(String)
    start_time = Column(DateTime)
    latitude = Column(Float)
    longitude = Column(Float)
    temperature_k = Column(Float)
    co2_concentration = Column(Float)
    file_url = Column(String)
    ingested_at = Column(DateTime, default=datetime.utcnow)

