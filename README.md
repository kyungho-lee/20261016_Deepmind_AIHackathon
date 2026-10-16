# GeoRescue 3D — Real-Time Spatial Disaster Evacuation Simulator & AI Training Engine

[![Google AI](https://img.shields.io/badge/Google_DeepMind-Gemini_4_Argon_(1M_Context)-4285F4?style=for-the-badge&logo=google)](https://georescue3d-464836279033.asia-northeast3.run.app/)
[![Antigravity Sandbox](https://img.shields.io/badge/Antigravity-Autonomous_A*_Verification-10B981?style=for-the-badge)](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon)
[![Google Cloud Run](https://img.shields.io/badge/Cloud_Run-Live_Production-0F9D58?style=for-the-badge&logo=google-cloud)](https://georescue3d-464836279033.asia-northeast3.run.app/)
[![Three.js WebGL](https://img.shields.io/badge/Three.js-3D_WebGL_Digital_Twin-000000?style=for-the-badge&logo=three.js)](https://georescue3d-464836279033.asia-northeast3.run.app/)
[![FastAPI](https://img.shields.io/badge/FastAPI-NetworkX_A*-009688?style=for-the-badge&logo=fastapi)](https://georescue3d-464836279033.asia-northeast3.run.app/api/evacuation-route?water_level=2.0)

- **Live Cloud Run Demo**: [**https://georescue3d-464836279033.asia-northeast3.run.app/**](https://georescue3d-464836279033.asia-northeast3.run.app/)
- **Live Verification API**: [`/api/evacuation-route?water_level=2.0`](https://georescue3d-464836279033.asia-northeast3.run.app/api/evacuation-route?water_level=2.0)
- **Public GitHub Repository**: [`https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon.git`](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon.git)
- **Hackathon Tracks**: **Track 2 (Gemini 4 Argon in Hard Tech)** & **Track 3 (Google AI for Social Good)**

**GeoRescue 3D** is an autonomous multi-agent 3D flood evacuation simulator and emergency dispatch digital twin built for the **Seoul Gangnam Station Basin**. It combines **Gemini 4 Argon (`gemini-4-argon`, 1M context, `thinking_level="high"`)**, an **Autonomous Python `NetworkX` A\* Sandbox Verification Loop (`antigravity-preview-09-2026`)**, and an interactive **Three.js 3D WebGL + Google Maps** visualization deployed on **Google Cloud Run**.

---

## 1. System Architecture Diagram

```
+---------------------------------------------------------------------------------------------------+
|                         1. GIS & Hydrological Terrain Data Pipeline (`make_data.py`)              |
|  • V-World 3D DEM Grid (`data/gangnam_3d_grid.csv` — 64x64 IDW elevation model, 13.5m to 44.0m)   |
|  • OSM Road Graph (`data/gangnam_graphify.json` — 8 Gangnam nodes, 10 weighted road segments)     |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|                   2. Gemini 4 Argon Lead Orchestrator & Chief Jury (`gemini-4-argon`)             |
|  • Shared 1M-token context window (`thinking_level="high"`, `background=True`)                    |
|  • Orchestrates 3-Team Competitive Tournament (Team Alpha / Team Beta / Team Gamma)               |
|  • Synthesizes 3D terrain elevation physics, flood rise functions, and rubric evaluation (97.6pt) |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|            3. Antigravity Autonomous Sandbox Verification Loop (`antigravity-preview-09-2026`)    |
|  • Executes Python `NetworkX` A* (`nx.astar_path`) in isolated verification sandbox (`main.py`)   |
|  • Enforces flood safety invariants: `z_elevation > 18.5m` AND `water_level_m <= 0.15m`           |
|  • Autonomous Self-Correction:                                                                    |
|      - Iteration #1: Rejects `GN_01 -> GN_02 (13.5m Flooded Underpass) -> GN_06 -> GN_08`         |
|      - Iteration #2: Verifies `[SUCCESS] GN_01 -> GN_04 -> GN_05 -> GN_06 -> GN_08` (Min 19.2m)   |
+-------------------------------------------------+-------------------------------------------------+
                                                  |
                                                  v
+---------------------------------------------------------------------------------------------------+
|          4. FastAPI Cloud Run Backend (`app.py`) & Three.js 3D WebGL UI (`static/index.html`)     |
|  • Real-time 3D DEM terrain mesh with 2.5m contour lines + slope-hugging 3D green evacuation tube |
|  • Interactive Water Rise Slider (0.5m - 5.0m) + Longitudinal Elevation Profile Cross-Section     |
|  • Synchronized Google Maps WGS84 Panel + Human-in-the-Loop (HITL) Officer Approval Console       |
+---------------------------------------------------------------------------------------------------+
```

---

## 2. Multi-Agent Team Configuration (`AGENTS.md`)

| Agent / Team Role | Assigned Model / Agent ID | Primary Responsibility |
| :--- | :--- | :--- |
| **1. Argon Chief Jury & Lead Orchestrator** | `gemini-4-argon` (`thinking_level="high"`) | 1M-context architecture orchestration, 3-team tournament evaluation (100-pt rubric), and final code adoption |
| **2. Backend & Data Pipeline Specialist** | `gemini-4-argon` (`medium`) + `gemini-3.8-flash` | Generates `data/gangnam_3d_grid.csv` & `data/gangnam_graphify.json` (`make_data.py`) and builds FastAPI (`app.py`) |
| **3. Autonomous Verification Agent** | `antigravity-preview-09-2026` (`environment="remote"`) | Isolated sandbox `NetworkX` A\* verification and autonomous self-correction (`z_elevation > 18.5m`, `water_level_m <= 0.15m`) |
| **4. Fast Subagent & Tool Worker** | `gemini-3.8-flash` | Parallel CSV/JSON schema validation, API contract testing, and sub-millisecond graph serialization |
| **5. Legal & Safety Guardrail Agent** | `gemini-3.5-flash-lite` | V-World 3D DEM & OpenStreetMap (ODbL v1.0) license compliance and mandatory Human-in-the-Loop (`AI-Assisted Evacuation Disclaimer`) |
| **Competing Teams (Alpha / Beta / Gamma)** | Multi-Model Tournament | **Team Alpha**: A\* Haversine optimization • **Team Beta**: Three.js 3D WebGL & Google Maps UI • **Team Gamma**: Full-stack flood safety invariants |

---

## 3. Verified Sandbox Results (`water_level = 2.0m`, Flood Plane `z = 18.5m`)

- **Origin**: `GN_01` — Gangnam Station Intersection (`37.4965, 127.02495`, `z_elevation = 19.2m`)
- **Bypassed Flooded Nodes (Rejected in Self-Correction Iteration #1)**:
  - `GN_02` — Gangnam Station Central Underpass (`z_elevation = 13.5m <= 18.5m`, `water_level_m = 0.45m > 0.15m`)
  - `GN_03` — Seocho Elementary Low Basin (`z_elevation = 17.2m <= 18.5m`, `water_level_m = 0.28m > 0.15m`)
- **Verified Safe High-Ground Route (Adopted in Self-Correction Iteration #2)**:
  - `GN_01 (19.2m) -> GN_04 Sinnonhyeon Ridge (22.8m) -> GN_05 Kukkiwon Hill (38.5m) -> GN_06 Yeoksam Plateau (34.0m) -> GN_08 Yeoksam Middle School Shelter (41.2m)`
- **Key Sandbox Metrics**:
  - **Minimum Route Elevation**: **`19.20m`** (`> 18.50m` critical flood plane)
  - **Maximum Surface Water Depth**: **`0.12m`** (`<= 0.15m` safe pedestrian wading limit)
  - **Total Evacuation Distance / Golden Time ETA**: **`1,900.0m` / `1,537.7s` (`25.6 min <= 30.0 min`)**
  - **Argon Chief Jury Winning Score**: **`97.6 / 100`** ([`reports/tournament_report.json`](reports/tournament_report.json))

---

## 4. Quickstart Guide (Local & Google Cloud Shell)

### Step 1: Clone Repository & Install Dependencies
```bash
git clone https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon.git
cd 20261016_Deepmind_AIHackathon
pip install -r requirements.txt
```

### Step 2: Generate 3D GIS Data & Run Autonomous Sandbox Verification
```bash
# 1. Generate 3D DEM grid (data/gangnam_3d_grid.csv) and road graph (data/gangnam_graphify.json)
python make_data.py

# 2. Execute Antigravity NetworkX A* verification & self-correction loop
python main.py

# 3. Run 3-Team Competitive Tournament & Argon Chief Jury evaluation
python tournament_pipeline.py
```

### Step 3: Launch FastAPI + Three.js 3D WebGL Server
```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```
Open `http://localhost:8080` (or click **Web Preview -> Port 8080** in Google Cloud Shell).

---

## 5. One-Command Google Cloud Run Deployment

Deploy the containerized FastAPI + Three.js 3D WebGL application directly to Google Cloud Run:

```bash
gcloud config set project h2gdm-hack26icn-2618
gcloud run deploy georescue3d \
  --source . \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --port 8080
```

- **Production Service URL**: [https://georescue3d-464836279033.asia-northeast3.run.app/](https://georescue3d-464836279033.asia-northeast3.run.app/)

---

## 6. Repository Submission Documents
- [`PROJECT_DESCRIPTION.md`](PROJECT_DESCRIPTION.md) — Official Hackathon Project Description (Track 2 & Track 3)
- [`AGENTS.md`](AGENTS.md) — Multi-Agent Tournament & Verification Architecture Specification
- [`DEMO_VIDEO_SCRIPT.md`](DEMO_VIDEO_SCRIPT.md) — 3-Minute Demo Video Voiceover Script & Storyboard
- [`SUBMISSION.md`](SUBMISSION.md) — Quick Copy-Paste Submission Form Sheet
- [`reports/Research_Report_GeoRescue_3D.md`](reports/Research_Report_GeoRescue_3D.md) — Technical Research & Hydrological Modeling Report
