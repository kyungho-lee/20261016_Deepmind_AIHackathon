# GeoRescue 3D — Official Hackathon Pitch Deck (8 Slides)

- **Project**: GeoRescue 3D — Real-Time Spatial Disaster Evacuation Simulator & AI Training Engine
- **Tracks**: Track 2 (Gemini 4 Argon in Hard Tech) & Track 3 (Google AI for Social Good)
- **Live Cloud Run URL**: https://georescue3d-464836279033.asia-northeast3.run.app/
- **GitHub Repository**: https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon

---

## Slide 1: Title & Vision
### **GeoRescue 3D**
**Real-Time Spatial Disaster Evacuation Simulator & AI Verification Engine**
- **Powered by**: `gemini-4-argon` (1M Context, `thinking_level="high"`) + `antigravity-preview-09-2026` (Autonomous Sandbox Verifier)
- **Live Cloud Run Production**: `https://georescue3d-464836279033.asia-northeast3.run.app/`
- **Core Value**: Transforming AI from an unverified text advisor into a **mathematically verified, 3D terrain-aware life-saving dispatch system**.

---

## Slide 2: The Problem — Why 2D Navigation & Raw LLMs Fail in Flash Floods
- **Bowl-Shaped Urban Topography (Seoul Gangnam Station Basin)**:
  - Central underpass sits at **`13.5m` elevation**, surrounded by **`38.5m–41.2m` steep ridges** (Kukkiwon Hill & Yeoksam Plateau).
- **Fatal Flaw of 2D Flat Navigation**:
  - Optimizes purely for horizontal distance (`850m`), routing citizens straight into the submerged **Gangnam Station Underpass (`GN_02`, `z = 13.5m`, `water_level = 0.45m`)**.
- **Fatal Flaw of Unverified LLMs**:
  - Text-only LLMs hallucinate routes without verifying physical terrain elevation (`z_elevation`) or pedestrian wading limits (`<= 0.15m`).

---

## Slide 3: Our Solution — GeoRescue 3D Digital Twin
- **100% Terrain-Locked 3D WebGL Digital Twin (`Three.js`)**:
  - 64x64 Inverse Distance Weighting (IDW) DEM mesh with `2.5m` topographic contour lines and critical `18.5m` flood boundary ring.
- **Autonomous `NetworkX` A\* Sandbox Self-Correction**:
  - Automatically detects and blacklists submerged basin nodes (`GN_02`, `GN_03`) and reroutes pedestrians along safe high-ground ridges (`GN_01 -> GN_04 -> GN_05 -> GN_06 -> GN_08`).
- **Human-in-the-Loop (HITL) Emergency Governance**:
  - Synchronized WGS84 Google Maps deep-link + mandatory Control Center Officer approval before public broadcast.

---

## Slide 4: Multi-Agent Architecture (`AGENTS.md`)
| Agent Role | Model / ID | Core Responsibility |
| :--- | :--- | :--- |
| **1. Chief Jury & Lead Orchestrator** | `gemini-4-argon` (`thinking_level="high"`, 1M Context) | Orchestrates 3-Team Competitive Tournament & 100-pt rubric selection |
| **2. Backend & GIS Data Specialist** | `gemini-4-argon` (`medium`) + `gemini-3.8-flash` | Generates `gangnam_3d_grid.csv` & `gangnam_graphify.json` (`make_data.py`) & FastAPI (`app.py`) |
| **3. Autonomous Sandbox Verifier** | `antigravity-preview-09-2026` (`remote`) | Executes isolated Python `NetworkX` A\* self-correction loop (`z > 18.5m`, `water <= 0.15m`) |
| **4. Fast Schema & Graph Worker** | `gemini-3.8-flash` | Parallel CSV/JSON validation & sub-millisecond graph serialization (`1.04ms`) |
| **5. Legal & Safety Guardrail** | `gemini-3.5-flash-lite` | V-World 3D DEM & OpenStreetMap (ODbL v1.0) compliance + HITL disclaimer |

---

## Slide 5: Autonomous Sandbox Verification Loop in Action
- **Scenario**: Extreme Flash Flood (`water_level = 2.0m`, Basin Flood Plane `z = 18.5m`)
- **Iteration #1 (Rejected by `antigravity-preview-09-2026`)**:
  - Candidate Path: `GN_01 (19.2m) -> GN_02 (13.5m) -> GN_06 (34.0m) -> GN_08 (41.2m)`
  - **4 Critical Violations**: `GN_02` submerged (`13.5m <= 18.5m`, surface water `0.45m > 0.15m`).
- **Iteration #2 (`[SUCCESS] Verified by Python A* Algorithm`)**:
  - `gemini-4-argon` blacklists `GN_02` and re-weights elevation bonus (`2.0`) & flood penalty (`0.4`).
  - **Verified Safe Path**: `GN_01 (19.2m) -> GN_04 (22.8m) -> GN_05 (38.5m) -> GN_06 (34.0m) -> GN_08 Shelter (41.2m)`.

---

## Slide 6: 3-Team Competitive Tournament & Argon Chief Jury
- **3 Competing Agent Engineering Teams**:
  - **Team Alpha**: Pure A\* Haversine distance optimization (`47.0 / 100` — failed flood plane gate)
  - **Team Beta**: 3D WebGL visual prototype (`44.0 / 100` — failed flood plane gate)
  - **Team Gamma (Adopted Winner)**: Full-Stack Safety Invariants + 3D Contour Mesh + HITL Guardrails (**`97.6 / 100` in Tournament / `100.0 / 100` Production Build**)

---

## Slide 7: Verified Quantitative Metrics & Live Cloud Run Performance
| Metric | Safety Requirement | GeoRescue 3D Verified Result |
| :--- | :--- | :--- |
| **Minimum Route Elevation (`min_z`)** | `> 18.50 m` | **`19.20 m`** (Peak `41.20 m` at Shelter) |
| **Maximum Surface Water (`max_water`)** | `<= 0.15 m` | **`0.12 m`** (`PASS`) |
| **Golden Time Evacuation ETA** | `<= 1,800 sec` (`30 min`) | **`1,524.6 sec`** (`25.4 min`, `1,900m`) |
| **Node-to-3D Terrain Vertical Error** | `0.00 m` | **`0.00 m`** (Unified IDW DEM Model) |
| **Cloud Run API Latency** | `< 50 ms` | **`1.04 ms`** (`asia-northeast3`) |

---

## Slide 8: Live Deployment & Future Roadmap
- **Live Now on Google Cloud Run**:
  - URL: [https://georescue3d-464836279033.asia-northeast3.run.app/](https://georescue3d-464836279033.asia-northeast3.run.app/)
  - GitHub: [https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon)
- **Next Steps**:
  1. Nationwide expansion across Korean flood-prone urban basins using live KMA (Korea Meteorological Administration) radar feeds.
  2. Real-time mobile AR pedestrian guidance & municipal emergency broadcast integration.
