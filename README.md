# GeoRescue 3D — Multi-Agent Flood Evacuation Digital Twin (Seoul Gangnam Basin)

**Repository**: [`https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon.git`](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon.git)

GeoRescue 3D is an autonomous multi-agent 3D flood evacuation routing and verification system built for the **Seoul Gangnam Station Basin**. It combines a **Hybrid Multi-Agent Competitive Tournament** (`Team Alpha`, `Team Beta`, `Team Gamma`), an **Autonomous Sandbox Verification Loop** (`antigravity-preview-09-2026`), and **Argon Chief Jury Selection** (`gemini-4-argon`, `thinking_level="high"`) with a real-time **FastAPI + NetworkX A\* + Three.js 3D WebGL + Google Maps** digital twin.

---

## 1. Multi-Agent Architecture & Agent Team Roles (`AGENTS.md`)

| Agent / Team Role | Assigned Model / Agent ID | Primary Responsibility |
| :--- | :--- | :--- |
| **1. Argon Chief Jury & Lead Orchestrator** | `gemini-4-argon` (`thinking_level="high"`) | System architecture, multi-agent tournament orchestration (`client.interactions.create`), 100-pt rubric evaluation, and final code adoption |
| **2. Backend & Data Pipeline Specialist Agent** | `gemini-4-argon` (`medium`) + `gemini-3.8-flash` | Generates `data/gangnam_3d_grid.csv` & `data/gangnam_graphify.json` via `make_data.py` and builds the FastAPI server (`app.py`) |
| **3. Autonomous Verification Agent** | `antigravity-preview-09-2026` (`environment="remote"`) | Executes isolated sandbox `NetworkX` A\* verification and autonomous self-correction (`z_elevation > 18.5m`, `water_level_m <= 0.15m`) |
| **4. Fast Subagent & Tool Worker** | `gemini-3.8-flash` | Parallel CSV/JSON schema validation, API contract verification, and sub-millisecond graph serialization |
| **5. Legal & Safety Guardrail Agent** | `gemini-3.5-flash-lite` | V-World 3D DEM & OpenStreetMap (ODbL v1.0) license compliance and mandatory Human-in-the-Loop (`AI-Assisted Evacuation Disclaimer`) |
| **Competing Teams (Alpha / Beta / Gamma)** | Multi-Model Tournament | **Team Alpha**: A\* Haversine optimization • **Team Beta**: Three.js 3D WebGL & Google Maps UI • **Team Gamma**: Full-stack flood safety invariants |

---

## 2. Verified Sandbox Results (`water_level = 2.0m`, Flood Plane `z = 18.5m`)

- **Origin**: `GN_01` — Gangnam Station Exit 10 (`37.497942, 127.027621`, `z_elevation = 19.2m`)
- **Bypassed Flooded Nodes**:
  - `GN_02` — Gangnam Station Underpass (`z_elevation = 13.5m <= 18.5m`, `water_level_m = 0.85m`)
  - `GN_03` — Seocho Elementary Low Road (`z_elevation = 17.2m <= 18.5m`, `water_level_m = 0.35m`)
- **Verified Safe High-Ground Route**:
  - `GN_01 (19.2m) -> GN_04 (22.8m) -> GN_05 (38.5m) -> GN_06 (34.0m) -> GN_08 Yeoksam Middle School Shelter (41.2m)`
- **Safety Metrics**:
  - Minimum Route Elevation: **`19.20m`** (`> 18.5m` flood plane)
  - Maximum Surface Water on Route: **`0.12m`** (`<= 0.15m` pedestrian limit)
  - Total Evacuation Distance / Golden Time ETA: **`1,900.0m` / `1,524.6s` (`25.4 min <= 30 min`)**
  - Argon Chief Jury Winning Score: **`97.6 / 100`** (`reports/tournament_report.json`)

---

## 3. Quick Start (Google Cloud Shell & Local Environment)

### Option A: Run Directly in Google Cloud Shell (via GitHub)
```bash
git clone https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon.git ~/georescue3d
cd ~/georescue3d
bash cloudshell_setup.sh
```
Then click **Web Preview -> Preview on port 8080** in Google Cloud Shell.

### Option B: Manual Execution
```bash
pip install -r requirements.txt
python make_data.py
python main.py
python tournament_pipeline.py
uvicorn app:app --host 0.0.0.0 --port 8080
```

### Option C: Deploy to Google Cloud Run
```bash
gcloud run deploy georescue3d \
  --source . \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --port 8080
```

---

## 4. Google Maps Platform Integration (Optional Live 2D Map Layer)

The frontend (`static/index.html`) includes a synchronized **Real-World Gangnam WGS84 Map Panel** alongside the Three.js 3D WebGL Digital Twin:
- Set `export GOOGLE_MAPS_API_KEY="YOUR_KEY"` before running `uvicorn app:app --host 0.0.0.0 --port 8080`, or paste a [Google Maps Platform Demo Key](https://mapsplatform.google.com/maps-demo-key?utm_campaign=gmp_git_agentskills_v1) directly in the UI panel.
- Even without an API key, the built-in **Zero-Fail Interactive WGS84 Coordinate Map & One-Click Google Maps Directions Deep-Link** operates automatically.
