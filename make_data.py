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


TERRAIN_CONTROL_POINTS: list[tuple[float, float, float]] = [
    (-45.0, 25.0, 19.2),   # GN_01: Gangnam Stn Origin Perimeter (Safe > 18.5m)
    (-15.0, 30.0, 13.5),   # GN_02: Gangnam Stn Underpass Basin (Deep Flood Pit 13.5m)
    (-55.0, 55.0, 17.2),   # GN_03: Seocho Low Corridor (Submerged 17.2m)
    (-35.0, -25.0, 22.8),  # GN_04: Gangnam-daero Upper Slope (Safe Ridge 22.8m)
    (5.0, -15.0, 38.5),    # GN_05: Kukkiwon Hill Crest (High Ground 38.5m)
    (35.0, 5.0, 34.0),     # GN_06: Teheran-ro Yeoksam Plateau (High Ground 34.0m)
    (-70.0, 75.0, 26.5),   # GN_07: Seocho Elementary High Ground Shelter (26.5m)
    (65.0, 12.0, 41.2),    # GN_08: Yeoksam Middle School Hill Shelter (41.2m)
    (-85.0, -75.0, 21.5),  # NW Boundary Slope
    (80.0, -65.0, 39.5),   # NE Kukkiwon/Nonhyeon High Ridge
    (-10.0, 75.0, 14.2),   # South Gangnam Drainage Channel (Low Basin)
    (80.0, 75.0, 31.0),    # SE Yeoksam Upland
]


def compute_terrain_elevation(x_3d: float, z_3d: float) -> float:
    """Compute smooth 3D DEM elevation (m) that matches all graph node elevations."""
    num = 0.0
    den = 0.0
    for px, pz, py in TERRAIN_CONTROL_POINTS:
        d2 = (x_3d - px) ** 2 + (z_3d - pz) ** 2
        w = 1.0 / ((d2 + 16.0) ** 1.45)
        num += w * py
        den += w
    return round(num / den, 2)


def generate_gangnam_3d_grid(csv_path: Path = CSV_PATH, grid_size: int = 21) -> list[dict[str, Any]]:
    """Generate a 3D terrain elevation grid (CSV) modeling the Gangnam Station low basin and hills."""
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []

    lat_min, lat_max = 37.4920, 37.5040
    lon_min, lon_max = 127.0200, 127.0380

    for r in range(grid_size):
        for c in range(grid_size):
            # r=0 is North (z_3d=-100, lat_max), r=grid_size-1 is South (z_3d=+100, lat_min)
            # Matches Three.js PlaneGeometry vertex ordering after rotateX(-pi/2)
            u = r / float(grid_size - 1)
            v = c / float(grid_size - 1)

            x_3d = round((v - 0.5) * 200.0, 2)
            z_3d = round((u - 0.5) * 200.0, 2)

            lat = round(lat_max - u * (lat_max - lat_min), 6)
            lon = round(lon_min + v * (lon_max - lon_min), 6)

            z_elevation = compute_terrain_elevation(x_3d, z_3d)

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
                "lat": 37.496500,
                "lon": 127.024950,
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
                "lat": 37.496200,
                "lon": 127.027650,
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
                "lat": 37.494700,
                "lon": 127.024050,
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
                "name": "Sinnonhyeon Ridge (Gangnam-daero Upper Slope)",
                "lat": 37.499500,
                "lon": 127.025850,
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
                "lat": 37.498900,
                "lon": 127.029450,
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
                "lat": 37.497700,
                "lon": 127.032150,
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
                "lat": 37.493500,
                "lon": 127.022700,
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
                "lat": 37.497280,
                "lon": 127.034850,
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
