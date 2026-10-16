"""GeoRescue 3D Data Generation Pipeline (make_data.py).

Generates:
  1. data/gangnam_3d_grid.csv  - 3D Digital Elevation Model (DEM) terrain grid for Gangnam Basin
  2. data/gangnam_graphify.json - Road network graph for NetworkX A* flood evacuation routing

Data Attribution:
  - V-World 3D Digital Twin DEM (Ministry of Land, Infrastructure and Transport)
  - OpenStreetMap (OSM) Road Network (ODbL v1.0)
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import sys
from typing import Any


DATA_DIR = Path("data")
CSV_PATH = DATA_DIR / "gangnam_3d_grid.csv"
JSON_PATH = DATA_DIR / "gangnam_graphify.json"


def generate_gangnam_3d_grid(csv_path: Path = CSV_PATH, grid_size: int = 21) -> list[dict[str, Any]]:
    """Generate a 3D terrain elevation grid (CSV) modeling the Gangnam Station low basin and hills."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    lat_min, lat_max = 37.4920, 37.5060
    lon_min, lon_max = 127.0190, 127.0380

    for r in range(grid_size):
        for c in range(grid_size):
            u = r / float(grid_size - 1)
            v = c / float(grid_size - 1)

            lat = round(lat_min + u * (lat_max - lat_min), 6)
            lon = round(lon_min + v * (lon_max - lon_min), 6)

            # Map to 3D WebGL scene coordinates [-100, 100]
            x_3d = round((v - 0.5) * 200.0, 2)
            z_3d = round((0.5 - u) * 200.0, 2)

            # Bowl-shaped Gangnam Station depression centered near (x=-15, z=30) + Kukkiwon/Yeoksam hills
            dist_basin = math.hypot(x_3d + 15.0, z_3d - 30.0)
            basin_dip = -11.5 * math.exp(-(dist_basin ** 2) / (2.0 * (42.0 ** 2)))
            ridge_rise = 18.5 * (1.0 / (1.0 + math.exp(-(x_3d - 5.0) / 28.0))) + 6.5 * math.sin(
                (z_3d - 15.0) * 0.03
            )
            z_elevation = round(max(12.5, 22.0 + basin_dip + ridge_rise), 2)

            # Flood water depth at reference water_level = 2.0m (flood plane = 18.5m)
            flood_plane_m = 18.5
            base_water_depth = round(max(0.0, flood_plane_m - z_elevation), 2)

            if z_elevation <= 16.0:
                zone_type = "inundated_critical"
            elif z_elevation <= 18.5:
                zone_type = "inundated_warning"
            elif z_elevation >= 32.0:
                zone_type = "high_ground"
            else:
                zone_type = "safe_corridor"

            rows.append(
                {
                    "grid_id": f"G_{r:02d}_{c:02d}",
                    "row": r,
                    "col": c,
                    "x_3d": x_3d,
                    "z_3d": z_3d,
                    "lat": lat,
                    "lon": lon,
                    "z_elevation": z_elevation,
                    "base_water_depth": base_water_depth,
                    "zone_type": zone_type,
                }
            )

    fieldnames = [
        "grid_id",
        "row",
        "col",
        "x_3d",
        "z_3d",
        "lat",
        "lon",
        "z_elevation",
        "base_water_depth",
        "zone_type",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return rows


def generate_gangnam_graphify(json_path: Path = JSON_PATH) -> dict[str, Any]:
    """Generate the Gangnam road network graph JSON with elevation and flood depth attributes."""
    json_path.parent.mkdir(parents=True, exist_ok=True)

    graph_data: dict[str, Any] = {
        "metadata": {
            "dataset_name": "gangnam_flood_evacuation_graphify_v2026",
            "project": "GeoRescue 3D",
            "region": "Seoul Gangnam-gu / Seocho-gu Basin",
            "scenario": "Extreme Rainfall Surge (water_level=2.0m, Basin Flood Plane=18.5m)",
            "gis_data_sources": [
                "V-World 3D Digital Twin DEM (Ministry of Land, Infrastructure and Transport)",
                "OpenStreetMap (OSM) Road Network (ODbL v1.0)",
            ],
            "origin_node": "GN_01",
            "target_shelters": ["GN_07", "GN_08"],
            "safety_thresholds": {
                "scenario_water_level_m": 2.0,
                "min_safe_z_elevation_m": 18.5,
                "safe_water_level_limit_m": 0.15,
                "critical_submerged_limit_m": 0.30,
                "max_shelter_water_level_m": 0.05,
                "max_evacuation_time_sec": 1800,
                "base_walking_speed_mps": 1.35,
            },
        },
        "nodes": [
            {
                "id": "GN_01",
                "name": "Gangnam Station Intersection (Origin Perimeter)",
                "lat": 37.497942,
                "lon": 127.027621,
                "x_3d": -45.0,
                "z_3d": 25.0,
                "z_elevation": 19.2,
                "elevation_m": 19.2,
                "current_water_depth": 0.12,
                "water_level_m": 0.12,
                "is_shelter": False,
                "zone_type": "basin_origin_perimeter",
            },
            {
                "id": "GN_02",
                "name": "Gangnam Station Exit 11 (Teheran-ro Low Basin)",
                "lat": 37.498850,
                "lon": 127.028910,
                "x_3d": -15.0,
                "z_3d": 30.0,
                "z_elevation": 13.5,
                "elevation_m": 13.5,
                "current_water_depth": 2.00,
                "water_level_m": 0.45,
                "is_shelter": False,
                "zone_type": "inundated_critical",
            },
            {
                "id": "GN_03",
                "name": "Jinheung Apt Intersection (Seocho-daero Low Corridor)",
                "lat": 37.495810,
                "lon": 127.023100,
                "x_3d": -55.0,
                "z_3d": 55.0,
                "z_elevation": 17.2,
                "elevation_m": 17.2,
                "current_water_depth": 1.30,
                "water_level_m": 0.24,
                "is_shelter": False,
                "zone_type": "inundated_warning",
            },
            {
                "id": "GN_04",
                "name": "Sinnonhyeon Station Ridge (Gangnam-daero Upper Slope)",
                "lat": 37.504520,
                "lon": 127.025040,
                "x_3d": -35.0,
                "z_3d": -25.0,
                "z_elevation": 22.8,
                "elevation_m": 22.8,
                "current_water_depth": 0.05,
                "water_level_m": 0.05,
                "is_shelter": False,
                "zone_type": "safe_corridor",
            },
            {
                "id": "GN_05",
                "name": "Kukkiwon Hill Intersection (High Ground)",
                "lat": 37.501950,
                "lon": 127.031520,
                "x_3d": 5.0,
                "z_3d": -15.0,
                "z_elevation": 38.5,
                "elevation_m": 38.5,
                "current_water_depth": 0.01,
                "water_level_m": 0.01,
                "is_shelter": False,
                "zone_type": "high_ground",
            },
            {
                "id": "GN_06",
                "name": "Yeoksam Station Intersection (Teheran-ro Plateau)",
                "lat": 37.500622,
                "lon": 127.036456,
                "x_3d": 35.0,
                "z_3d": 5.0,
                "z_elevation": 34.0,
                "elevation_m": 34.0,
                "current_water_depth": 0.03,
                "water_level_m": 0.03,
                "is_shelter": False,
                "zone_type": "high_ground",
            },
            {
                "id": "GN_07",
                "name": "Seocho Elementary School Shelter",
                "lat": 37.493100,
                "lon": 127.020500,
                "x_3d": -70.0,
                "z_3d": 75.0,
                "z_elevation": 26.5,
                "elevation_m": 26.5,
                "current_water_depth": 0.02,
                "water_level_m": 0.02,
                "is_shelter": True,
                "zone_type": "shelter",
            },
            {
                "id": "GN_08",
                "name": "Yeoksam Middle School Regional Evacuation Shelter",
                "lat": 37.499850,
                "lon": 127.035800,
                "x_3d": 65.0,
                "z_3d": 12.0,
                "z_elevation": 41.2,
                "elevation_m": 41.2,
                "current_water_depth": 0.00,
                "water_level_m": 0.00,
                "is_shelter": True,
                "zone_type": "shelter",
            },
        ],
        "edges": [
            {
                "id": "E_GN01_GN02",
                "source": "GN_01",
                "target": "GN_02",
                "road_name": "Gangnam-daero to Teheran-ro Basin Entry",
                "distance_m": 180.0,
                "water_level_m": 0.45,
                "drainage_status": "overflow",
            },
            {
                "id": "E_GN02_GN06",
                "source": "GN_02",
                "target": "GN_06",
                "road_name": "Teheran-ro Direct Corridor",
                "distance_m": 320.0,
                "water_level_m": 0.35,
                "drainage_status": "submerged",
            },
            {
                "id": "E_GN01_GN03",
                "source": "GN_01",
                "target": "GN_03",
                "road_name": "Seocho-daero Low-Lying Segment",
                "distance_m": 480.0,
                "water_level_m": 0.26,
                "drainage_status": "poor",
            },
            {
                "id": "E_GN03_GN07",
                "source": "GN_03",
                "target": "GN_07",
                "road_name": "Seocho Elementary Access Road",
                "distance_m": 650.0,
                "water_level_m": 0.14,
                "drainage_status": "moderate",
            },
            {
                "id": "E_GN01_GN04",
                "source": "GN_01",
                "target": "GN_04",
                "road_name": "Gangnam-daero Northbound Uphill",
                "distance_m": 680.0,
                "water_level_m": 0.09,
                "drainage_status": "normal",
            },
            {
                "id": "E_GN04_GN05",
                "source": "GN_04",
                "target": "GN_05",
                "road_name": "Bongeunsa-ro to Kukkiwon Hill Climb",
                "distance_m": 490.0,
                "water_level_m": 0.02,
                "drainage_status": "clear",
            },
            {
                "id": "E_GN05_GN06",
                "source": "GN_05",
                "target": "GN_06",
                "road_name": "Nonhyeon-ro High-Ground Connector",
                "distance_m": 380.0,
                "water_level_m": 0.02,
                "drainage_status": "clear",
            },
            {
                "id": "E_GN06_GN08",
                "source": "GN_06",
                "target": "GN_08",
                "road_name": "Teheran-ro East Shelter Corridor",
                "distance_m": 350.0,
                "water_level_m": 0.01,
                "drainage_status": "clear",
            },
        ],
    }

    json_path.write_text(json.dumps(graph_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return graph_data


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    grid_rows = generate_gangnam_3d_grid()
    graph_data = generate_gangnam_graphify()

    print(
        json.dumps(
            {
                "status": "DATA_GENERATED",
                "csv_file": str(CSV_PATH),
                "csv_grid_points": len(grid_rows),
                "json_file": str(JSON_PATH),
                "graph_nodes": len(graph_data["nodes"]),
                "graph_edges": len(graph_data["edges"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
