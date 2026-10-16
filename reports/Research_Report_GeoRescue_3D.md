# Deep Research Report: GeoRescue 3D (Three.js/WebGL & Multi-Agent Flood Evacuation Digital Twin)

This technical research report documents the **architectural references, 3D GIS terrain and hydrological simulation model, Gemini 4 Argon multi-agent competitive tournament, and autonomous sandbox verification pipeline** powering **GeoRescue 3D** for the Seoul Gangnam Station Basin.

- **Live Cloud Run Production URL**: [`https://georescue3d-464836279033.asia-northeast3.run.app/`](https://georescue3d-464836279033.asia-northeast3.run.app/)
- **GitHub Repository**: [`https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon.git`](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon.git)

---

## 1. Three.js 3D WebGL Digital Twin & Hydrological Terrain Modeling

### 1.1 IDW (Inverse Distance Weighting) 3D Terrain Mesh & Contour Synthesis
- **64x64 High-Resolution DEM Mesh (`data/gangnam_3d_grid.csv`)**:
  - Models the actual bowl-shaped topography of the Seoul Gangnam Station Basin (`13.5m` central underpass depression rising to `38.5m` at Kukkiwon Hill and `41.2m` at Yeoksam Middle School Shelter).
  - Uses a unified 12-control-point Inverse Distance Weighting (IDW) interpolation model across both backend (`make_data.py`) and frontend (`static/index.html`) so that every road node's `z_elevation` matches the 3D terrain mesh vertex height with `0.00m` vertical discrepancy.
- **Hypsometric Topographic Contours & Flood Boundary Rendering**:
  - Dynamically renders `2.5m` topographic contour lines (`등고선`) and the critical `18.5m` flood plane boundary directly onto the 3D GIS surface texture, paired with a real-time longitudinal elevation cross-section chart (`#elevProfileCanvas`).

### 1.2 Real-Time Hydrological Surface & Rain Particle System
- **Interactive Flood Plane (`0.5m` – `5.0m`)**:
  - Simulates flash-flood surface accumulation in the Gangnam depression while dynamically recalculating `NetworkX` A* edge weights via FastAPI (`/api/evacuation-route`).

---

## 2. Gemini 4 Argon Multi-Agent Tournament & Autonomous Sandbox Verification

```
[ Weather & 3D DEM Sensor Grid (gangnam_3d_grid.csv / gangnam_graphify.json) ]
             │
             ▼
[ Gemini 4 Argon Chief Jury (gemini-4-argon, thinking_level="high") ]
  • Orchestrates 3-Team Competitive Tournament (Team Alpha, Team Beta, Team Gamma)
  • Evaluates candidate backends & 3D WebGL UIs on a 100-point rubric
             │
             ▼
[ Antigravity Autonomous Sandbox Verification Loop (antigravity-preview-09-2026) ]
  • Executes Python NetworkX A* pathfinding in an isolated verification sandbox
  • Audits invariants: z_elevation > 18.5m, water_level_m <= 0.15m, Golden Time <= 1800s
  • Triggers autonomous Self-Correction (Iteration #1 -> Iteration #2) when GN_02/GN_03 flood
             │
             ▼
[ Three.js 3D WebGL Digital Twin + Human-in-the-Loop (HITL) Dispatch Console ]
  • Slope-hugging 3D evacuation tube + WGS84 Google Maps deep-link + Officer Approval gate
```

- **Self-Correction Verification Proof**:
  - **Iteration #1 (Rejected)**: Naive shortest path `GN_01 -> GN_02 -> GN_06 -> GN_08` fails sandbox invariants because `GN_02` (Gangnam Station Underpass) sits at `z_elevation = 13.5m <= 18.5m` with `water_level_m = 0.45m > 0.15m`.
  - **Iteration #2 (Verified Safe)**: Autonomous penalty re-weighting routes around the flooded basin via high-ground ridges `GN_01 (19.2m) -> GN_04 (22.8m) -> GN_05 (38.5m) -> GN_06 (34.0m) -> GN_08 (41.2m)`, achieving `min_z_elevation = 19.2m` and `max_water_level = 0.12m` in `1,537.7s` (`25.6 min <= 30 min` Golden Time).

---

## 3. Open GIS Compliance & Responsible AI Guardrails

| Category | Standard / Reference | Implementation in GeoRescue 3D |
| :--- | :--- | :--- |
| **Open GIS Licensing** | V-World 3D DEM (MOLIT) & OpenStreetMap (ODbL v1.0) | Embedded in `/api/evacuation-route` JSON payload (`gis_attribution`) and 3D HUD badge |
| **Human-in-the-Loop (HITL)** | Public Emergency Broadcast Safety Standard | Mandatory Control Center Officer Verification & Dispatch Approval button before public alert release |
| **Academic Foundation** | *Towards a Serious Games Evacuation Simulator* (`arXiv:1805.09138`, `arXiv:1905.11082`) | Interactive 3D spatial visualization significantly improves emergency route comprehension and evacuation self-efficacy |

---
*Research & Verification Report generated for the GeoRescue 3D Hackathon Submission.*
