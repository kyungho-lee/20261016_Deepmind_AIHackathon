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

## 4. How We Built It with Gemini 4 Argon & Antigravity

### 4.1 Gemini 4 Argon (`gemini-4-argon`, 1M Context Window, `thinking_level="high"`, `background=True`)
- **Lead Orchestrator & Chief Jury**: Leverages the shared **1M-token context window** (`thinking_level="high"`, `background=True`) to ingest the entire 3D Digital Elevation Model (`data/gangnam_3d_grid.csv`, 64x64 IDW terrain grid), the road network topology (`data/gangnam_graphify.json`), and multi-team candidate codebases simultaneously.
- **Long-Decode 3D & Physics Synthesis**: Generates the unified 12-control-point Inverse Distance Weighting (IDW) terrain elevation physics model, dynamic flood surface rise functions, and Three.js WebGL rendering shaders with `0.00m` vertical discrepancy between graph nodes and 3D terrain vertices.
- **Multi-Agent Competitive Tournament**: Orchestrates three specialized engineering teams (**Team Alpha** for A\* Haversine & elevation optimization, **Team Beta** for Three.js 3D WebGL & Google Maps visualization, and **Team Gamma** for full-stack safety invariants) and evaluates them on a strict 100-point rubric (`97.6 / 100` winning build).

### 4.2 Antigravity Managed Agent (`antigravity-preview-09-2026`, `environment="remote"`)
- **Autonomous Sandbox Verification Loop**: Executes Python `NetworkX` (`nx.astar_path`) shortest-path verification inside an isolated sandbox environment (`main.py` & `app.py --verify-json`).
- **Self-Correction Invariant Enforcement**:
  - **Iteration #1 (Rejected)**: Detects that the naive shortest route (`GN_01 -> GN_02 -> GN_06 -> GN_08`) violates `z_elevation > 18.5m` and `water_level_m <= 0.15m` at `GN_02 (13.5m)`.
  - **Iteration #2 (Verified Safe)**: Autonomously applies dynamic flood-depth penalties and re-solves the A\* path over high-ground ridges (`GN_01 [19.2m] -> GN_04 [22.8m] -> GN_05 [38.5m] -> GN_06 [34.0m] -> GN_08 [41.2m]`), outputting `[SUCCESS] Verified by Python A* Algorithm`.

### 4.3 Fast Leaf Worker (`gemini-3.8-flash`) & Legal/Safety Guardrail (`gemini-3.5-flash-lite`)
- **`gemini-3.8-flash`**: Performs parallel CSV/JSON dataset schema validation and sub-millisecond graph serialization (`~1.04ms` API response time).
- **`gemini-3.5-flash-lite`**: Enforces V-World 3D DEM & OpenStreetMap (ODbL v1.0) open GIS license attribution and attaches the mandatory Human-in-the-Loop (`AI-Assisted Evacuation Disclaimer`) gate.

### 4.4 Google Cloud Run Production Deployment
- Fully containerized **FastAPI + Three.js WebGL + Google Maps** application (`Dockerfile`) deployed to **Google Cloud Run** (`asia-northeast3`, Project `h2gdm-hack26icn-2618`) serving real-time REST endpoints (`/api/evacuation-route`, `/api/grid`, `/api/graph`) and interactive 3D visualization over HTTPS.

---

## 5. Key Features & Innovation

1. **Terrain-Locked 3D WebGL Digital Twin (`Three.js`)**:
   - 64x64 IDW-interpolated 3D terrain mesh of the Gangnam Basin with hypsometric elevation coloring, `2.5m` topographic contour lines (`등고선`), and a crimson `18.5m` flood boundary ring.
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
