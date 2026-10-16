# GeoRescue 3D — Official Hackathon Submission Package

## 1. Basic Submission Information (Copy & Paste)

- **Project Name**: GeoRescue 3D
- **Tagline / One-Line Pitch**: Autonomous Multi-Agent 3D Flood Evacuation Digital Twin for the Seoul Gangnam Basin with NetworkX A* Sandbox Self-Correction and Three.js WebGL Visualization.
- **Live Production Demo URL (Google Cloud Run)**: https://georescue3d-464836279033.asia-northeast3.run.app/
- **GitHub Repository URL**: https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon
- **GCP Project & Region**: `h2gdm-hack26icn-2618` (`asia-northeast3`, Seoul)

---

## 2. Project Summary / Abstract (English — For Submission Form)

**Problem**: Urban flash floods in bowl-shaped low-lying basins—such as the Seoul Gangnam Station intersection (`13.5m` elevation surrounded by `38m–41m` hills)—rapidly submerge standard shortest-path pedestrian routes and underground passages within minutes. Standard navigation apps often route citizens directly through flooded underpasses, while unverified LLM-generated advice risks hallucinating unsafe paths during life-critical emergencies.

**Solution**: **GeoRescue 3D** is an end-to-end **Multi-Agent 3D Flood Evacuation Digital Twin** orchestrated by **Gemini 4 Argon (`gemini-4-argon`, `thinking_level="high"`)** and verified by an **Autonomous Sandbox Verification Agent (`antigravity-preview-09-2026`)**:
1. **Multi-Agent Competitive Tournament**: Three specialized agent teams (`Team Alpha` for A* Haversine & elevation optimization, `Team Beta` for Three.js 3D WebGL & Google Maps visualization, and `Team Gamma` for flood safety invariants & legal guardrails) compete to generate the optimal full-stack implementation, evaluated on a 100-point rubric by the **Argon Chief Jury (`97.6 / 100` winning score)**.
2. **Autonomous NetworkX A* Sandbox Self-Correction**: When extreme rainfall (`water_level = 2.0m`, basin flood plane `z = 18.5m`) submerges the Gangnam Station Underpass (`GN_02`, `z = 13.5m`) and Seocho Low Road (`GN_03`, `z = 17.2m`), the sandbox verifier automatically rejects the naive shortest path (`Iteration #1`) and self-corrects (`Iteration #2`) onto a high-ground ridge trajectory: `GN_01 (19.2m) -> GN_04 (22.8m) -> GN_05 Kukkiwon Hill (38.5m) -> GN_06 Yeoksam Plateau (34.0m) -> GN_08 Yeoksam Middle School Shelter (41.2m)`.
3. **Terrain-Aligned 3D WebGL Digital Twin & HITL Dispatch**: Renders a 64x64 IDW-interpolated 3D elevation mesh with `2.5m` topographic contour lines, slope-hugging 3D evacuation tubes, a longitudinal elevation cross-section chart, Google Maps WGS84 deep-links, Open GIS license attribution (V-World & OpenStreetMap ODbL), and a mandatory **Human-in-the-Loop (HITL) Control Center Officer Approval** workflow.

---

## 3. Key Quantitative Verification Metrics

| Verification Metric | Target Threshold | Verified Sandbox Value | Status |
| :--- | :--- | :--- | :--- |
| **Minimum Route Elevation (`min_z_elevation_m`)** | `> 18.50 m` | **`19.20 m`** (`GN_01` -> `41.20 m` `GN_08`) | `PASS` |
| **Maximum Surface Water Depth (`max_water_level_m`)** | `<= 0.15 m` | **`0.12 m`** | `PASS` |
| **Golden Time Evacuation ETA** | `<= 1,800 s` (`30 min`) | **`1,537.7 s`** (`25.6 min`, `1,900 m`) | `PASS` |
| **Autonomous Self-Correction Loop** | Automatic bypass of `GN_02` & `GN_03` | **2 Iterations (`1.04 ms` API latency)** | `VERIFIED_SAFE` |
| **Argon Chief Jury Score** | `>= 90.0 / 100` | **`97.6 / 100`** (`Team Gamma`) | `ADOPTED` |
| **Open GIS & HITL Guardrails** | V-World + OSM ODbL + Officer Approval | **Embedded in API & 3D HUD** | `COMPLIANT` |

---

## 4. Architecture & Tech Stack

- **Multi-Agent Orchestration & Verification**: `gemini-4-argon` (`thinking_level="high"`), `antigravity-preview-09-2026` (Sandbox Verifier), `gemini-3.8-flash` (Data & Schema Worker), `gemini-3.5-flash-lite` (Legal & HITL Guardrail Agent)
- **Backend & Routing Engine**: Python 3.11, FastAPI, Uvicorn, NetworkX (`nx.astar_path` with Haversine distance + dynamic flood-depth & elevation penalty weighting)
- **Frontend 3D & GIS Visualization**: Three.js (`r128` WebGL), 64x64 IDW DEM Terrain Mesh, Dynamic Flood Plane Shader, HTML5 2D Longitudinal Elevation Profile Canvas, Google Maps Platform JS API & Directions Deep-Link
- **Cloud Infrastructure**: Docker, Google Cloud Build, Google Artifact Registry, Google Cloud Run (`asia-northeast3`)
