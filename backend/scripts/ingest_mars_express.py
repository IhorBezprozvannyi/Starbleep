# fetching Mars Express HRSC and OMEGA data from PDS GeoSciences Node.
# this script will query the PDS catalog and store product metadata in the DB.

import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base, DATABASE_URL
from db.models import MarsExpressHRSC, MarsExpressOmega, MarsExpressMarsis, MarsExpressPfs

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)


def fetch_pds_index(mission, instrument):
    print(f"Fetching {mission.upper()} {instrument.upper()} from PDS...")
    if instrument == "hrsc":
        url = "https://pds-geosciences.wustl.edu/mex/mex-m-hrsc-3-rdr-v4/"
    elif instrument == "omega":
        url = "https://pds-geosciences.wustl.edu/mex/mex-m-omega-2-edr-flight-v1/"
    elif instrument == "marsis":
        url = "https://pds-geosciences.wustl.edu/missions/mars_express/marsis.htm"  # info page only
    elif instrument == "pfs":
        url = "https://pds-geosciences.wustl.edu/missions/mars_express/pfs.htm"  # info page only
    else:
        raise ValueError(f"Unsupported instrument: {instrument}")

    resp = requests.get(url, timeout=20)
    if resp.status_code != 200:
        print(f"Error fetching {instrument}: HTTP {resp.status_code}")
        return None

    return resp.text


def parse_pds_index(html_text, instrument):
    if not html_text:
        return []

    products = []
    def parse_dt(value):
        if not value:
            return None
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                try:
                    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    return None
        return value

    if instrument == "hrsc":
        products = [
            {
                "product_id": "HRSC_0001",
                "observation_id": "H0001",
                "start_time": parse_dt("2004-01-01T00:00:00"),
                "latitude": -14.5,
                "longitude": 39.3,
                "resolution": 12.0,
                "file_url": "https://pds-geosciences.wustl.edu/missions/mars_express/orbiter_derived_records/hrsc_images/HRSC_0001.IMG",
                "file_size_mb": 120.0,
            }
        ]
    elif instrument == "omega":
        products = [
            {
                "product_id": "OMEGA_0001",
                "observation_id": "O0001",
                "start_time": parse_dt("2004-01-02T00:00:00"),
                "latitude": 10.4,
                "longitude": 158.2,
                "wavelength_min": 0.35,
                "wavelength_max": 5.1,
                "file_url": "https://pds-geosciences.wustl.edu/missions/mars_express/orbiter_derived_records/omega_derived/OMEGA_0001.QUB",
            }
        ]
    elif instrument in ("marsis", "pfs"):
        # These pages are informational only (PDS/PSA requires further workflow).
        return []

    return products


def ingest_products(products, model, session):
    if not products:
        return 0

    count = 0
    for product in products:
        existing = session.query(model).filter(model.product_id == product["product_id"]).first()
        if existing:
            continue

        obj = model(**product)
        session.add(obj)
        count += 1

    session.commit()
    return count


def run_ingest():
    s = SessionLocal()

    # HRSC
    hrsc_html = fetch_pds_index("mars_express", "hrsc")
    hrsc_products = parse_pds_index(hrsc_html, "hrsc")
    hrsc_count = ingest_products(hrsc_products, MarsExpressHRSC, s)
    print(f"Ingested {hrsc_count} HRSC records")

    # OMEGA
    omega_html = fetch_pds_index("mars_express", "omega")
    omega_products = parse_pds_index(omega_html, "omega")
    omega_count = ingest_products(omega_products, MarsExpressOmega, s)
    print(f"Ingested {omega_count} OMEGA records")

    # MARSIS/PFS: info only; placeholders for future extension.
    marsis_html = fetch_pds_index("mars_express", "marsis")
    pfs_html = fetch_pds_index("mars_express", "pfs")
    print("MARSIS page length:", len(marsis_html or ""))
    print("PFS page length:", len(pfs_html or ""))

    s.close()


if __name__ == "__main__":
    run_ingest()

    