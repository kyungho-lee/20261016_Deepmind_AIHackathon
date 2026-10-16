# GeoRescue 3D — 3-Minute Demo Video Script & Storyboard (`DEMO_VIDEO_SCRIPT.md`)

- **Project Title**: GeoRescue 3D — Real-Time Spatial Disaster Evacuation Simulator & AI Training Engine
- **Target Duration**: 3 Minutes (`0:00` – `3:00`)
- **Language**: English (Voiceover & Captions)
- **Live Cloud Run URL Shown on Screen**: `https://georescue3d-464836279033.asia-northeast3.run.app/`
- **GitHub Repository**: `https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon`

---

## 🎬 Scene 1: Problem & Overview (`0:00 - 0:45`)

### 🖥️ Visual Storyboard (What to Show on Screen)
1. **`0:00 - 0:15`**: Open the live Google Cloud Run URL (`https://georescue3d-464836279033.asia-northeast3.run.app/`). Orbit the camera slowly around the **Three.js 3D WebGL Digital Twin** of the Seoul Gangnam Station Basin. Point the cursor at the deep blue/brown central depression (`GN_02: 13.5m` Underpass) surrounded by steep green ridges (`GN_05: 38.5m` Kukkiwon Hill, `GN_08: 41.2m` Yeoksam Middle School Shelter).
2. **`0:15 - 0:30`**: Hover over the **2.5m topographic contour lines** and the crimson **`18.5m` flood boundary line** rendered directly on the 3D terrain mesh.
3. **`0:30 - 0:45`**: Point to the dashed red bypassed path (`GN_01 -> GN_02 -> GN_06`) versus the glowing green 3D evacuation tube hugging the high-ground slope (`GN_01 -> GN_04 -> GN_05 -> GN_06 -> GN_08`).

### 🎙️ English Voiceover Script
> *"Welcome to **GeoRescue 3D**, an autonomous multi-agent spatial disaster evacuation simulator built with **Gemini 4 Argon** and **Google Antigravity**.*  
> *During extreme urban flash floods in concave basins like Seoul's Gangnam Station, rainwater rapidly pools into the central `13.5-meter` depression.*  
> *Traditional 2D flat navigation maps optimize only for horizontal distance—routing citizens straight into the submerged Gangnam Station Underpass at `GN_02`.*  
> *Unverified AI chatbots also risk hallucinating deadly routes. GeoRescue 3D solves this by combining **Gemini 4 Argon's 1-million-token spatial reasoning** with an **Autonomous Python NetworkX A-Star Verification Loop** and a real-time **Three.js 3D WebGL Digital Twin**."*

---

## 🌊 Scene 2: Live Technical Demonstration (`0:45 - 1:45`)

### 🖥️ Visual Storyboard (What to Show on Screen)
1. **`0:45 - 1:05`**: In the left HUD control panel, drag the **Flood Water Level Slider** smoothly from **`1.0m` up to `2.0m` and `3.5m`**. Show the translucent 3D water surface rising in real time across the Gangnam basin and rain particles intensifying.
2. **`1:05 - 1:25`**: Show the glowing green 3D evacuation polyline dynamically hugging the 3D terrain contours (`GN_01 [19.2m] -> GN_04 [22.8m] -> GN_05 [38.5m] -> GN_06 [34.0m] -> GN_08 [41.2m]`). Click the **`Top`**, **`Ridge`**, and **`Iso 3D`** camera preset buttons to prove that the 3D route matches the terrain elevation with zero vertical gap.
3. **`1:25 - 1:45`**: On the right panel, highlight the **Longitudinal Terrain Elevation Profile (`#elevProfileCanvas`)** showing the green terrain cross-section staying strictly above the crimson `18.5m` flood line, and click through the synchronized **Google Maps WGS84 Panel** & **Human-in-the-Loop (HITL) Officer Approval** button (`DISPATCH APPROVED`).

### 🎙️ English Voiceover Script
> *"Let's test the live simulation on Google Cloud Run. As we move the flood water slider from `1.0 meter` up to `3.5 meters`, the 3D water mesh rises across the Gangnam depression in real time.*  
> *Every slider movement triggers our FastAPI backend in under two milliseconds. Instead of cutting across the flooded `13.5-meter` underpass, the glowing green 3D evacuation corridor dynamically climbs the **Sinnonhyeon Ridge (`22.8m`)** and **Kukkiwon Hill (`38.5m`)** to reach **Yeoksam Middle School Shelter (`41.2m`)** within the 30-minute Golden Time.*  
> *On the right panel, our real-time **Longitudinal Elevation Cross-Section** proves that every meter of the route stays above the `18.5-meter` flood plane, paired with synchronized WGS84 Google Maps coordinates and a mandatory **Human-in-the-Loop Control Center Officer Approval** gate."*

---

## 🧪 Scene 3: Antigravity Verification Loop in Action (`1:45 - 2:30`)

### 🖥️ Visual Storyboard (What to Show on Screen)
1. **`1:45 - 2:05`**: Switch to the terminal / Cloud Shell console (or split screen with the bottom-right **Self-Correction Verification Log** in the UI) and run:
   ```bash
   python main.py
   ```
2. **`2:05 - 2:30`**: Highlight the terminal output showing:
   - `[ITERATION 1] Candidate Path: GN_01 -> GN_02 -> GN_06 -> GN_08 | FAILED (GN_02 z_elevation=13.5m <= 18.5m, water_level_m=0.45m > 0.15m)`
   - `[ITERATION 2] [SUCCESS] Verified by Python A* Algorithm | Safe Route: GN_01 -> GN_04 -> GN_05 -> GN_06 -> GN_08 (min_z=19.2m > 18.5m, max_water=0.12m <= 0.15m)`
   - Also show `python tournament_pipeline.py` outputting the **Argon Chief Jury (`97.6 / 100`)** selection.

### 🎙️ English Voiceover Script
> *"Under the hood, GeoRescue 3D is powered by an **Antigravity Autonomous Sandbox Verification Loop (`antigravity-preview-09-2026`)**.*  
> *When we execute the verification pipeline in the sandbox, Iteration 1 tests the naive shortest path through `GN_02` and immediately catches a safety violation: `z_elevation` is `13.5 meters`, below the `18.5-meter` flood plane.*  
> *Without human intervention, the agent penalizes submerged edges and re-executes the Python `NetworkX` A-Star solver in Iteration 2—printing `[SUCCESS] Verified by Python A* Algorithm` once every node satisfies `z_elevation > 18.5m` and surface water remains under `0.15m`.*  
> *Furthermore, **Gemini 4 Argon** acts as Chief Jury across three competing agent teams, adopting the winning `97.6-point` full-stack build."*

---

## ☁️ Scene 4: Architecture, Cloud Run & Conclusion (`2:30 - 3:00`)

### 🖥️ Visual Storyboard (What to Show on Screen)
1. **`2:30 - 2:45`**: Show the browser address bar with the live **Google Cloud Run HTTPS URL (`https://georescue3d-464836279033.asia-northeast3.run.app/`)** alongside the GitHub repository (`README.md`, `AGENTS.md`, `PROJECT_DESCRIPTION.md`).
2. **`2:45 - 3:00`**: Return to the 3D Gangnam Digital Twin view with the `DISPATCH APPROVED — BROADCAST ACTIVE` badge illuminated.

### 🎙️ English Voiceover Script
> *"Our entire architecture—from **Gemini 4 Argon's 1M-token context orchestrator**, **`gemini-3.8-flash` data validators**, and **`gemini-3.5-flash-lite` Open GIS & HITL guardrails**, to the **Antigravity Python A-Star sandbox**—is containerized and live on **Google Cloud Run**.*  
> *By uniting generative 3D digital twins with mathematically verified graph routing, **GeoRescue 3D** transforms AI from a passive advisor into a verifiable, life-saving disaster response engine. Thank you."*

---

## ✅ Pre-Recording Quick Checklist
1. Open Browser Tab 1: [https://georescue3d-464836279033.asia-northeast3.run.app/](https://georescue3d-464836279033.asia-northeast3.run.app/)
2. Open Browser Tab 2: [https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon](https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon)
3. Open Terminal Tab: Ready with `python main.py` and `python tournament_pipeline.py` output visible.
