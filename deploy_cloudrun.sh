#!/usr/bin/env bash
# GeoRescue 3D — Google Cloud Run One-Click Deployment Script
set -euo pipefail

PROJECT_ID="${1:-h2gdm-hack26icn-2618}"
REGION="${2:-asia-northeast3}"
SERVICE_NAME="georescue3d"

echo "========================================================================"
echo " [GeoRescue 3D] Google Cloud Run One-Click Deployment"
echo "  - Project ID : ${PROJECT_ID}"
echo "  - Region     : ${REGION}"
echo "  - Service    : ${SERVICE_NAME}"
echo "========================================================================"

gcloud config set project "${PROJECT_ID}"

gcloud run deploy "${SERVICE_NAME}" \
  --source . \
  --region "${REGION}" \
  --allow-unauthenticated \
  --port 8080
