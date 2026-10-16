#!/usr/bin/env bash
# GeoRescue 3D - Google Cloud Shell One-Click Setup & Launch Script
# GitHub Repository: https://github.com/kyungho-lee/20261016_Deepmind_AIHackathon.git
set -e

echo "=================================================================="
echo " GeoRescue 3D - Cloud Shell Backend Pipeline & 3D WebGL Launcher"
echo "=================================================================="

echo "[1/4] Installing Python dependencies (fastapi, uvicorn, networkx, google-genai)..."
pip install --user -r requirements.txt

echo "[2/4] Running make_data.py to generate 3D DEM Grid & Graphify JSON..."
python3 make_data.py

echo "[3/4] Running Autonomous Sandbox Verification & Argon Chief Jury Tournament..."
python3 main.py
python3 tournament_pipeline.py

# Ensure static/index.html is synced with latest Google Maps + 3D UI
cp -f static/index.html index.html

echo "[4/4] Starting FastAPI Server on 0.0.0.0:8080..."
echo ">>> Click Cloud Shell [Web Preview] -> [Preview on port 8080] <<<"
python3 -m uvicorn app:app --host 0.0.0.0 --port 8080
