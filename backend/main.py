# FastAPI app. what starts my api server (uvicorn main:app)
from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel

from db.database import SessionLocal
from db.models import MarsExpressHRSC, MarsExpressOmega, MarsExpressMarsis, MarsExpressPfs

app = FastAPI()

# Schemas
class HRSCImage(BaseModel):
    product_id: str
    observation_id: str
    start_time: str
    latitude: float
    longitude: float
    resolution: float
    file_url: str
    file_size_mb: float

    class Config:
        orm_mode = True


class OmegaProduct(BaseModel):
    product_id: str
    observation_id: str
    start_time: str
    latitude: float
    longitude: float
    wavelength_min: float
    wavelength_max: float
    file_url: str

    class Config:
        orm_mode = True


class MarsisProduct(BaseModel):
    product_id: str
    observation_id: str
    start_time: str
    latitude: float
    longitude: float
    frequency_mhz: float
    penetration_depth_km: float
    file_url: str

    class Config:
        orm_mode = True


class PfsProduct(BaseModel):
    product_id: str
    observation_id: str
    start_time: str
    latitude: float
    longitude: float
    temperature_k: float
    co2_concentration: float
    file_url: str

    class Config:
        orm_mode = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Starbleep backend is running"}


@app.get("/mars-express/hrsc", response_model=List[HRSCImage])
def get_hrsc_images(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    images = db.query(MarsExpressHRSC).offset(skip).limit(limit).all()
    return images


@app.get("/mars-express/omega", response_model=List[OmegaProduct])
def get_omega_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = db.query(MarsExpressOmega).offset(skip).limit(limit).all()
    return results


@app.get("/mars-express/marsis", response_model=List[MarsisProduct])
def get_marsis_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = db.query(MarsExpressMarsis).offset(skip).limit(limit).all()
    return results


@app.get("/mars-express/pfs", response_model=List[PfsProduct])
def get_pfs_products(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    results = db.query(MarsExpressPfs).offset(skip).limit(limit).all()
    return results


@app.get("/mars-express/stats")
def get_stats(db: Session = Depends(get_db)):
    return {
        "hrsc_images": db.query(MarsExpressHRSC).count(),
        "omega_products": db.query(MarsExpressOmega).count(),
        "marsis_products": db.query(MarsExpressMarsis).count(),
        "pfs_products": db.query(MarsExpressPfs).count(),
    }
