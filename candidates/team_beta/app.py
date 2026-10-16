"""Team Beta Candidate: 3D Visualization-Centric Backend (app.py).

Focus: Supplies rich 3D node/terrain coordinates for Three.js WebGL scene.
Limitation: Pure Euclidean/Haversine shortest path without flood elevation filtering.
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys
import time
import networkx as nx


def compute_evacuation_route(graph_path: str = "data/gangnam_graphify.json") -> dict:
    t0 = time.perf_counter()
    data = json.loads(Path(graph_path).read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in data["nodes"]}
    g = nx.Graph()
    for nid, attrs in nodes.items():
        g.add_node(nid, **attrs)
    for edge in data["edges"]:
        g.add_edge(edge["source"], edge["target"], **edge, weight=float(edge["distance_m"]))

    origin = data["metadata"].get("origin_node", "GN_01")
    path = nx.astar_path(g, origin, "GN_08", weight="weight")
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    min_z = min(float(nodes[n]["z_elevation"]) for n in path)
    max_w = max(float(nodes[n]["water_level_m"]) for n in path)
    total_dist = sum(
        float(g.edges[path[i], path[i + 1]]["distance_m"]) for i in range(len(path) - 1)
    )

    return {
        "team": "Team Beta (3D Visualization)",
        "model": "gemini-4-argon (medium)",
        "node_path": path,
        "total_distance_m": round(total_dist, 2),
        "min_z_elevation_m": round(min_z, 2),
        "max_water_level_m": round(max_w, 3),
        "execution_time_ms": round(elapsed_ms, 3),
        "self_corrected": False,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-json", action="store_true")
    parser.add_argument("--graph", default="data/gangnam_graphify.json")
    args = parser.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(compute_evacuation_route(args.graph), indent=2))
