# Mars & Moon Mission Data Sources so far 

## Overview
This document locks in data source decisions for all missions. Each mission has 4 data categories: mission metadata, current position, science data, and images. Where no REST API exists, we use static data or document the limitation.

---

## Lunar Missions

### LRO (Lunar Reconnaissance Orbiter)
**NAIF ID:** -85 | **Status:** Active | **Last Updated:** 2026-03-24

| Data Type | Source | Status | Notes |
|-----------|--------|--------|-------|
| Mission Info | JPL Horizons API | Working | Launch (2009-Jun-18), 50km polar orbit, 1000kg, payload list |
| Current Position | JPL Horizons API | Working | RA/DEC, distance, velocity, trajectory to 2027 |
| Images (LROC) | LROC Archive (ASU) | Not Usable | HTML-only interface, no REST API, 8.1M images archived but inaccessible programmatically |
| **Overall Decision** | | | Use Horizons for tracking only. LROC images require manual portal access or scraping. |

---

### Chandrayaan-1
**NAIF ID:** -86 | **Status:** Inactive (Dead) | **Last Updated:** 2016 (Radar-reconstructed)

| Data Type | Source | Status | Notes |
|-----------|--------|--------|-------|
| Mission Info | JPL Horizons API | Working | Launch (2008-Oct-22), 1050kg, 312-day mission, 70k+ images |
| Current Position | JPL Horizons API | Not Available | No ephemeris after 2022-Sep-30. Last position reconstructed from 7 radar detections (2016 Goldstone). Use last known: START_TIME=2022-09-29&STOP_TIME=2022-09-30 |
| Science Data (SIR-2) | ESA PSA TAP | Working | Near-Infrared Spectrometer observations. Query by date (2009-Feb to 2009-Aug) or orbit number. Download-ready PDS files. |
| Images (TMC/HySI/M3) | ISRO ISSDC Portal | Auth Gated | 1003 TMC + 772 HySI products. Requires free ISRO registration. No public REST API. |
| **Overall Decision** | | | Use Horizons (static) + ESA PSA for spectra. Flag mission as "radar_reconstructed" in tracking_status. Skip images. |

---

### GRAIL-A ("Ebb") & GRAIL-B ("Flow")
**NAIF IDs:** -177 (Ebb), -178 (Flow) | **Status:** Impacted (2012-Dec-17) | **Last Updated:** Mission End

| Data Type | Source | Status | Notes |
|-----------|--------|--------|-------|
| Mission Info | JPL Horizons API | Working | Twin spacecraft, 50km polar orbit, 175-225km separation. LGRS gravity instrument. Exact impact: 75.609°N, 333.413°E, 2012-Dec-17 22:29:54 UTC. |
| Current Position | N/A | Not Available | Impacted 2012-Dec-17. No ephemeris available. Tracking status: impacted. |
| Science Data (LGRS) | NASA ODE | Catalog Only | 12k+ GRAIL products cataloged (EDR, CDRL1A/B, RSDMAP, etc.). ODE lists them but doesn't serve via REST. Full archive at PDS Geosciences (Washington Univ). Complex access workflow. |
| Images (MoonKAM) | GRAILMoonKAM.com | Defunct | Portal dead. No REST API. Images archived but inaccessible. |
| **Overall Decision** | | | Use Horizons metadata only. Skip live tracking and image/science data. Historical mission only. |

---

## Mars Missions

### MRO (Mars Reconnaissance Orbiter)
**NAIF ID:** -74 | **Status:** Active | **Last Updated:** 2026-03-24

| Data Type | Source | Status | Notes |
|-----------|--------|--------|-------|
| Mission Info | JPL Horizons API | Working | Launch (2005-Aug-12), Mars arrival (2006-Mar-10), 2180kg, trajectory to 2026-Apr-13 |
| Current Position | JPL Horizons API | Working | Live elements: 3648km semi-major axis (~258km altitude), 80.7° inclination, 111 min period. Updated 2026 data available. |
| SHARAD Data | PDS Geosciences Node | Working | Subsurface radar (15 MHz). 14MB cumulative index. Thumbnail browse products publicly accessible. No auth. Directory browseable. |
| **Overall Decision** | | | Use both Horizons (position) + PDS Geosciences SHARAD (science). Reliable, public, actively updated. |

---

### Mars Odyssey (MO)
**NAIF ID:** -77 | **Status:** Active | **Last Updated:** 2026-03-24

| Data Type | Source | Status | Notes |
|-----------|--------|--------|-------|
| Mission Info | PDS Mission Catalog | Working | Launch (2001-Apr-07), Mars arrival (2001-Oct-24), 1223kg. THEMIS (IR/VIS), GRS (Gamma Ray), NS (Neutron). Primary rover comms relay. |
| Current Position | JPL Horizons API | Partial | No 2026 ephemeris in API, but mission status is active. Fixed parameters known: ~400km altitude, 93° sun-synchronous orbit. Use static data + flag as "estimated". |
| GRS/NS Data | UArizona GRS PDS Node | Working | Surface chemistry (H/Fe/Si elemental mapping). Global 5°×5° grid products. PDS3 .lbl + .TAB format. Queryable by lat/lon/time. No auth. Maintained 24/7. (Note: main node under maintenance 2026-03-24 19:30 UTC) |
| **Overall Decision** | | | Use Horizons (static orbital params) + UArizona GRS node for science. GRS is reliable and actively maintained. |

---

### Mars Express (MEX)
**NAIF ID:** Mars Express (text) | **Status:** Active | **Last Updated:** 2026-03-24

| Data Type | Source | Status | Notes |
|-----------|--------|--------|-------|
| Mission Info | PDS/ESA Mission Page | Working | Launch (2003-Jun-02), Mars orbit (2003-Dec-25), 1223kg. Instruments: MARSIS (1-5MHz radar), HRSC (12m/pixel stereo), OMEGA (NIR mineralogy), PFS (FTIR), VMC (visual monitoring). |
| Current Position | JPL Horizons API | Working | Highly elliptical orbit (298×10,107km, 86.9° inclination, ~24h period). 2026 active. Query by text "Mars Express" not NAIF ID. |
| MARSIS Data | PDS Geosciences Node | Working | Subsurface radar (1-5 MHz, km-scale penetration). Complements SHARAD. Public access, no auth. |
| HRSC Imagery | PDS Geosciences Node | Working | 12m/pixel stereo coverage. Global database. Public access. |
| OMEGA Spectra | PDS Geosciences Node | Working | NIR mineral & water ice mapping. Queryable. Public access. |
| **Overall Decision** | | | Use Horizons (position) + PDS Geosciences for all science (MARSIS, HRSC, OMEGA). Single reliable source for all data. |

---

## Rovers (Not Actively Tracked)

### Curiosity, Perseverance, Opportunity, Spirit, Yutu/Pragyan
**Status:** No Live APIs

| Data Type | Decision |
|-----------|----------|
| Position | Static hardcoded waypoints from mission summaries (last known lat/lon). Update manually if rover moves. |
| Images | NASA Rover Photos API (MRPOD) is **dead**. Gateway offline. Use rover-specific archives (raw.nasa.gov for Curiosity/Perseverance rover images) or snapshot from rover pages. |
| Science Data | REMS (environmental) dead. RAD data in PDS. No live telemetry for most rovers. Use static / manual updates. |

---

## Implementation Strategy

### Phase 1: Immediate (This Week)
- ✅ Horizons endpoints for all active orbiting spacecraft (LRO, MRO, Odyssey, Mars Express)
- ✅ PDS Geosciences SHARAD/GRS/MARSIS ingestion scripts
- ✅ ESA PSA TAP for Chandrayaan-1 SIR-2
- ✅ Static rover data (hardcoded waypoints)

### Phase 2: Secondary (Next Week)
- ⏳ HRSC/OMEGA metadata parsing (if high priority)
- ⏳ Dead spacecraft tracking (Chandrayaan legacy data)
- ⏳ GRAIL historical mission data (if time permits)

### Phase 3: Future (Blocked)
- ❌ LROC images (HTML scraping only, not recommended)
- ❌ ISRO data (registration required, terms unknown)
- ❌ MoonKAM (portal defunct)
- ❌ NASA Rover Photos (API deprecated)

---

## Rate Limits & Considerations

| Source | Rate Limit | Auth | Notes |
|--------|-----------|------|-------|
| JPL Horizons | ~10 req/sec | None | Reliable. Can be slow (~2-5s per query). Batch queries when possible. |
| PDS Geosciences | None documented | None | Static file server. No auth. Can be slow during maintenance. UArizona GRS more reliable. |
| ESA PSA TAP | None documented | None | ADQL interface. Reliable. Queryable by date/instrument. |

---

## Tracking Status Fields

Recommend adding to mission/spacecraft models:

```
tracking_status: enum ["active", "impacted", "radar_reconstructed", "hardcoded_static"]
last_position_update: datetime
last_position_confidence: enum ["live", "estimated", "historical", "unknown"]
ephemeris_available_until: datetime (e.g., 2022-09-30 for Chandrayaan-1)
```

This distinguishes:
- **active**: Live telemetry available (LRO, MRO, Odyssey, MEX)
- **impacted**: Mission ended via surface impact (GRAIL)
- **radar_reconstructed**: Position inferred from historical radar (Chandrayaan-1)
- **hardcoded_static**: Rover mission phase, static data only

---

## Slow/Problem Sources

- **PDS Geosciences Node**: Occasionally slow or under maintenance. UArizona GRS is faster alternative for Odyssey data.
- **JPL Horizons API**: Can take 2-5 seconds per query. Batch by mission/date range to reduce calls.
- **ESA PSA TAP**: Generally fast but slow initial connection. Cache query results.