# Official Project Description: GeoRescue 3D

## 1. Project Name & One-Line Summary
**GeoRescue 3D — Real-Time Spatial Disaster Evacuation Simulator & AI Training Engine**  
An autonomous multi-agent 3D flood evacuation digital twin for the Seoul Gangnam Station Basin powered by **Gemini 4 Argon (`gemini-4-argon`)**, **Antigravity Sandbox Verification (`antigravity-preview-09-2026`)**, **NetworkX A\* Pathfinding**, and **Three.js WebGL**.

- **Live Demo URL (Google Cloud Run)**: [https://georescue3d-464836279033.asia-northeast3.run.app/](https://georescue3d-464836279033.asia-northeast3.run.app/)
- **Public GitHub Repository**: [https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon)

---

## 2. Track Alignment
- **Primary Track**: **Track 2 (Gemini 4 Argon in Hard Tech)** — 3D spatial digital twin synthesis, hydrological elevation modeling, and formal algorithmic verification in an isolated code sandbox.
- **Secondary Track**: **Track 3 (Google AI for Social Good)** — Life-critical urban flash-flood evacuation routing with Open GIS compliance and Human-in-the-Loop (HITL) emergency dispatch governance.

---

## 3. Problem & Impact
Urban flash floods in bowl-shaped, concave metropolitan terrain—most notably the **Seoul Gangnam Station Basin** (`13.5m` central elevation surrounded by `38.5m–41.2m` ridges at Kukkiwon Hill and Yeoksam Plateau)—pose a lethal threat during extreme monsoon cloudbursts:
1. **Why 2D Flat Navigation Maps Fail**: Conventional 2D navigation systems optimize purely for horizontal shortest distance (`GN_01 -> GN_02 -> GN_06 -> GN_08`). During flash flooding (`water_level >= 2.0m`, critical flood plane `z = 18.5m`), this shortest path routes pedestrians directly into the submerged **Gangnam Station Underpass (`GN_02`, `z_elevation = 13.5m`, `water_level_m = 0.85m`)** and **Seocho Low Road (`GN_03`, `z_elevation = 17.2m`, `water_level_m = 0.35m`)**.
2. **Why Unverified LLM Advice Is Insufficient**: Pure text-based LLM responses cannot guarantee physical terrain invariants (`z_elevation > current_water_depth` and pedestrian wading threshold `water_level_m <= 0.15m`) without deterministic graph verification.
3. **Real-World Social Impact**: **GeoRescue 3D** bridges generative AI reasoning with hard physical verification, ensuring every recommended evacuation corridor is mathematically verified in a Python `NetworkX` A\* sandbox, rendered on a terrain-accurate 3D WebGL digital twin, and approved by a human control center officer before broadcast.

---

## 4. How We Built It: Data Pipeline, Graphify & Loop Engineering with Gemini 4 Argon

### 4.1 Data Pipeline & Graphify Spatial Knowledge Graph (`make_data.py`)
- **Real-World Topographic & GIS Anchors**: Anchored on real-world WGS84 coordinates and road networks from **OpenStreetMap (ODbL v1.0)** and actual elevation benchmarks (`13.5m` at the Gangnam Station Underpass up to `41.2m` at Yeoksam Middle School Shelter, modeled after Korea's **V-World 3D DEM** and the 2022 Gangnam extreme flood profile).
- **Deterministic 3D DEM Interpolation (`data/gangnam_3d_grid.csv`)**: Uses 12 real-world topographic control points with **Inverse-Distance Weighting (IDW)** to generate a reproducible 3D elevation grid (`441` backend validation cells / `4,096` WebGL vertices) with `0.00m` vertical drift inside isolated sandboxes.
- **Graphify Spatial Topology Conversion (`data/gangnam_graphify.json`)**: Converts continuous 3D terrain and urban road corridors into an elevation-annotated, AI-executable spatial knowledge graph (`Graphify` format: 8 key intersection/shelter nodes and 10 weighted road edges with `z_elevation`, `distance_m`, `water_level_m`, and `is_shelter` attributes) so both LLMs and Python `NetworkX` operate on the exact same topological ground truth.

### 4.2 Multi-Agent Team Built via Dual-Loop Engineering (`Gemini 4 Argon` + `Antigravity`)
Instead of relying on single-shot LLM prompts that hallucinate unsafe routes, we engineered our multi-agent system around **Dual-Loop Engineering**:
1. **Inner Loop — Autonomous Sandbox Verification & Self-Correction Loop (`antigravity-preview-09-2026` + `gemini-3.8-flash`)**:
   - **`gemini-3.8-flash` (Data & Schema Validator)** validates the Graphify JSON topology and DEM CSV integrity in parallel (`~1.04ms`).
   - **`antigravity-preview-09-2026` (Sandbox Verification Agent)** executes deterministic Python `NetworkX` A\* (`nx.astar_path`) against `gangnam_graphify.json` inside an isolated Linux sandbox.
   - **Closed-Loop Self-Correction**: When **Iteration #1** (`GN_01 -> GN_02 -> GN_06 -> GN_08`, `850m`) fails the flood safety invariant at `GN_02` (`z_elevation = 13.5m <= 18.5m`, `water_level_m = 0.45m > 0.15m`), the loop automatically feeds the constraint violation back, blacklists flooded nodes, increases elevation penalty weights, and converges in **Iteration #2** on the verified high-ground ridge route (`GN_01 [19.2m] -> GN_04 [22.8m] -> GN_05 [38.5m] -> GN_06 [34.0m] -> GN_08 [41.2m]`), outputting `[SUCCESS] Verified by Python A* Algorithm`.
2. **Outer Loop — 3-Team Competitive Tournament & Argon Chief Jury Loop (`gemini-4-argon` + `gemini-3.5-flash-lite`)**:
   - **`gemini-4-argon` (`1M Context`, `thinking_level="high"`, `background=True`)** orchestrates three competing subagent teams (**Team Alpha** for A\* heuristics, **Team Beta** for Three.js 3D WebGL, **Team Gamma** for full-stack safety invariants) within its shared 1M-token context window.
   - Every candidate build is audited by the Inner Sandbox Loop and scored on a 100-point rubric (`tournament_pipeline.py`). Disqualified builds (Alpha: `47.0`, Beta: `44.0`) are rejected, and the winning build (**Team Gamma: `97.6 / 100`**) is promoted with mandatory **Human-in-the-Loop (HITL)** guardrails enforced by **`gemini-3.5-flash-lite`**.

### 4.3 Google Cloud Run Serverless Production Deployment
- Fully containerized **FastAPI + Three.js WebGL + Google Maps** application (`Dockerfile`) deployed to **Google Cloud Run** (`asia-northeast3`, Project `h2gdm-hack26icn-2618`) serving real-time REST endpoints (`/api/evacuation-route`, `/api/grid`, `/api/graph`) and interactive 3D visualization over HTTPS.

---

## 5. Key Features & Innovation

1. **Terrain-Locked 3D WebGL Digital Twin (`Three.js`)**:
   - 64x64 IDW-interpolated 3D terrain mesh of the Gangnam Basin with hypsometric elevation coloring, `2.5m` topographic contour lines, and a crimson `18.5m` flood boundary ring.
   - Slope-hugging 3D green evacuation tube (`TubeGeometry`) and road network that follow exact terrain gradients (`0.00m` elevation mismatch).
2. **Real-Time Water-Level Slider Simulation (`0.5m` – `5.0m`)**:
   - Interactive flood slider dynamically raises/lowers the translucent 3D flood plane, updates rain particle intensity, and triggers live `NetworkX` A\* route recalculation via FastAPI.
3. **Autonomous Python A\* Verification Console & Longitudinal Elevation Profile**:
   - Displays real-time sandbox verification status (`VERIFIED_SAFE`), self-correction iteration logs (`Iteration #1 Failed -> Iteration #2 Passed`), and a 2D longitudinal elevation cross-section chart comparing route terrain height against the `18.5m` flood plane.
4. **Synchronized Google Maps WGS84 Panel & HITL Officer Approval**:
   - Pairs the 3D digital twin with real-world WGS84 coordinates, a one-click Google Maps Walking Directions deep-link, and a Control Center Officer Approval (`Human-in-the-Loop`) dispatch workflow.

---

## 6. Live Demo URL & Verification Links
- **Live Cloud Run URL**: [https://georescue3d-464836279033.asia-northeast3.run.app/](https://georescue3d-464836279033.asia-northeast3.run.app/)
- **Live API Verification Endpoint**: [https://georescue3d-464836279033.asia-northeast3.run.app/api/evacuation-route?water_level=2.0](https://georescue3d-464836279033.asia-northeast3.run.app/api/evacuation-route?water_level=2.0)
- **Public GitHub Repository**: [https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon)
