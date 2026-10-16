# GeoRescue 3D Multi-Agent Competitive Tournament, Backend Pipeline & Verification Specification (`AGENTS.md`)

- **Live Cloud Run Production URL**: [https://georescue3d-464836279033.asia-northeast3.run.app/](https://georescue3d-464836279033.asia-northeast3.run.app/)
- **Public GitHub Repository**: [https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon)

## 1. Architecture Overview: Multi-Agent Backend Pipeline, Competitive Generation & Argon Chief Jury Selection

GeoRescue 3D operates on a **Hybrid Multi-Agent Architecture** combining a **Specialized Backend & Data Pipeline Agent**, a **3-Team Competitive Development Tournament (Team Alpha, Team Beta, Team Gamma)**, an **Autonomous Sandbox Verification Agent (`antigravity-preview-09-2026`)**, and the **Argon Chief Jury (`gemini-4-argon`, `thinking_level="high"`, 1M Context Window)**:

1. **Antigravity Agent Workspace**:
   - **Backend & Data Pipeline Specialist Agent** generates `make_data.py` (`data/gangnam_3d_grid.csv`, `data/gangnam_graphify.json`) and FastAPI `app.py` (`uvicorn app:app --host 0.0.0.0 --port 8080`).
   - **Competing Teams (Alpha, Beta, Gamma)** generate candidate implementations of `app.py` and `static/index.html` (`index.html`).
   - **Autonomous Verification Agent (`antigravity-preview-09-2026`)** executes the `NetworkX` A* self-correction verification loop in the isolated sandbox.
   - **Argon Chief Jury (`gemini-4-argon`, `thinking_level="high"`)** audits sandbox metrics, conducts the jury vote, and promotes the winning build.
2. **Google Cloud Shell & Cloud Run Runtime**:
   - Launches the FastAPI server (`uvicorn app:app --host 0.0.0.0 --port 8080`), serves the Three.js 3D WebGL preview (`static/index.html`), and deploys to Google Cloud Run (`https://georescue3d-464836279033.asia-northeast3.run.app/`).

```
+---------------------------------------------------------------------------------------------------+
|                         Argon Chief Jury & Lead Orchestrator                                      |
|                     Model: gemini-4-argon (1M Context, thinking_level="high")                     |
|  - Coordinates Backend Pipeline Agent, Competitive Teams (Alpha/Beta/Gamma), and Sandbox Verifier |
|  - Audits sandbox execution results, conducts Jury Vote, adopts make_data.py, app.py & index.html |
+-------------------+---------------------------+---------------------------+-----------------------+
                    |                           |                           |
                    v                           v                           v
+-----------------------------------+ +-------------------+ +---------------------------------------+
|  Backend & Data Pipeline Agent    | |  Competing Teams  | |    Autonomous Verification Agent      |
|   (Backend & GIS Data Pipeline)   | | (Alpha/Beta/Gamma)| |     (Sandbox Verification & Safety)   |
| Model: gemini-4-argon (medium)    | |  - Team Alpha: A* | | Model: antigravity-preview-09-2026    |
|        + gemini-3.8-flash         | |  - Team Beta: 3D  | |        + gemini-3.5-flash-lite        |
| • make_data.py (CSV + JSON)       | |  - Team Gamma:    | | • Isolated Sandbox NetworkX A* Audit  |
| • FastAPI app.py (Port 8080 REST) | |    Full-Stack Safe| | • Self-Correction Loop (z > 18.5m)    |
+-----------------------------------+ +-------------------+ +---------------------------------------+
```

---

## 2. Agent Team Roles & Responsibilities

| Agent / Team Role | Assigned Model / Agent ID | Primary Focus & Deliverable Responsibility |
| :--- | :--- | :--- |
| **1. Argon Chief Jury & Lead Orchestrator** | `gemini-4-argon` (`thinking_level="high"`, `background=True`) | • Overall system architecture, 1M-context tournament orchestration via `client.interactions.create`<br>• Multi-criteria rubric scoring (100-pt scale), final jury vote & adoption of `make_data.py`, `app.py`, and `static/index.html` (`index.html`) |
| **2. Backend & Data Pipeline Specialist Agent** | `gemini-4-argon` (`thinking_level="medium"`) + `gemini-3.8-flash` | • Authoring & executing `make_data.py` to generate `data/gangnam_3d_grid.csv` (3D DEM grid) and `data/gangnam_graphify.json` (road network graph)<br>• Building production FastAPI backend (`app.py`) with `NetworkX` A* dynamic flood water-level weighting (`/api/evacuation-route`, `/api/grid`, `/api/graph`) for Cloud Shell & Cloud Run (`uvicorn app:app --host 0.0.0.0 --port 8080`) |
| **3. Autonomous Verification Agent** | `antigravity-preview-09-2026` (`environment="remote"`) | • Running Python `NetworkX` A* shortest-path verification inside the isolated sandbox<br>• Auditing flood safety invariants (`z_elevation > 18.5m`, `z_elevation > current_water_depth`, `water_level_m <= 0.15m`) and triggering autonomous self-correction (`[SUCCESS] Verified by Python A* Algorithm`) |
| **4. Fast Subagent & Tool Worker** | `gemini-3.8-flash` | • Parallel CSV/JSON dataset schema validation (`gangnam_3d_grid.csv`, `gangnam_graphify.json`), API contract testing, and sub-millisecond graph serialization |
| **5. Legal & Safety Guardrail Agent** | `gemini-3.5-flash-lite` | • V-World 3D DEM & OpenStreetMap (ODbL v1.0) open GIS license compliance verification and mandatory Human-in-the-Loop `'AI-Assisted Evacuation Disclaimer'` attachment |
| **Team Alpha (Algorithmic Optimization Team)** | `gemini-3.8-flash` + `antigravity-preview-09-2026` | • High-performance Python `networkx` A* Haversine heuristic design and elevation-aware edge weight optimization |
| **Team Beta (3D Spatial Visualization Team)** | `gemini-4-argon` (`thinking_level="medium"`) | • Three.js 3D WebGL digital twin terrain elevation mesh, interactive water-level slider, rain particle system, and green 3D evacuation path line (`static/index.html` & `index.html`) |
| **Team Gamma (Safety Verification & Full-Stack Team)** | `antigravity-preview-09-2026` + `gemini-3.5-flash-lite` | • End-to-end flood safety invariant enforcement, self-correction loop integration, and full-stack guardrail compliance |

---

## 3. Sandbox Verification & Jury Voting Rubric (100 Points Total)

Every candidate submission and backend pipeline build is executed in an isolated sandbox against `data/gangnam_3d_grid.csv` and `data/gangnam_graphify.json` (`water_level = 2.0m`, critical basin flood plane `z_elevation = 18.5m`):

1. **Sandbox Flood Safety Invariants (35 Points)** — *Mandatory Gate*:
   - Every node on the A* evacuation route must satisfy `z_elevation > 18.5m` and `z_elevation > current_water_depth`.
   - Every node and road segment must satisfy `water_level_m <= 0.15m`.
   - Destination node must be a designated safe shelter (`is_shelter == True`) reached within Golden Time (`<= 1800s`).
2. **Backend Pipeline, Algorithmic Optimization & API Integrity (25 Points)**:
   - `make_data.py` deterministically generates `data/gangnam_3d_grid.csv` and `data/gangnam_graphify.json`.
   - `app.py` uses Python `networkx` (`nx.Graph`, `nx.astar_path`) with admissible Haversine heuristics, flood water-level weighting, and exposes FastAPI endpoints (`/`, `/static`, `/api/grid`, `/api/graph`, `/api/evacuation-route`) ready for `uvicorn app:app --host 0.0.0.0 --port 8080`.
3. **Three.js 3D WebGL Visualization Fidelity (25 Points)**:
   - `static/index.html` (and `index.html`) renders interactive Three.js 3D terrain from `gangnam_3d_grid.csv`, dynamic flood water surface plane with slider control, animated rain particles, and bright green 3D evacuation path geometry.
4. **Legal & Safety Guardrail Compliance (15 Points)**:
   - Explicit V-World & OpenStreetMap (ODbL) GIS license attribution and Human-in-the-Loop `'AI-Assisted Evacuation Disclaimer'` embedded in both API payload (`app.py`) and 3D HUD (`static/index.html`).

---

## 4. Execution Protocol (`make_data.py` -> `main.py` -> `tournament_pipeline.py` -> `uvicorn app:app`)

1. **[Step 1 — Backend Data Pipeline Generation]**: Backend & Data Pipeline Specialist Agent runs `make_data.py` to generate `data/gangnam_3d_grid.csv` and `data/gangnam_graphify.json`.
2. **[Step 2 — Autonomous Sandbox Verification Loop]**: `antigravity-preview-09-2026` and `gemini-4-argon` execute `main.py` and `app.py --verify-json` to verify and self-correct the NetworkX A* route (`[SUCCESS] Verified by Python A* Algorithm`).
3. **[Step 3 — Argon Chief Jury Evaluation & Adoption]**: `tournament_pipeline.py` evaluates all candidates and promotes the winning backend (`app.py`) and 3D frontend (`static/index.html` & `index.html`).
4. **[Step 4 — Cloud Shell & Cloud Run Server]**: Launch `uvicorn app:app --host 0.0.0.0 --port 8080` and deploy to Google Cloud Run (`https://georescue3d-464836279033.asia-northeast3.run.app/`).
