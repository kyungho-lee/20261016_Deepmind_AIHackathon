"""Team Alpha Candidate: High-Speed NetworkX A* Backend (app.py).

Focus: Sub-millisecond NetworkX A* routing with Haversine heuristics.
Limitation: Uses soft flood penalty (0.2) without hard z_elevation > 18.5m cutoff.
"""

from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import sys
import time
import networkx as nx


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6_371_000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def compute_evacuation_route(graph_path: str = "data/gangnam_graphify.json") -> dict:
    t0 = time.perf_counter()
    data = json.loads(Path(graph_path).read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in data["nodes"]}
    g = nx.Graph()
    for nid, attrs in nodes.items():
        g.add_node(nid, **attrs)
    for edge in data["edges"]:
        u, v = edge["source"], edge["target"]
        dist = float(edge["distance_m"])
        water = float(edge.get("water_level_m", 0.0))
        # Team Alpha: fast soft penalty, blocks only extreme water > 0.30m
        if water > 0.30:
            continue
        g.add_edge(u, v, **edge, weight=dist * (1.0 + 0.2 * water))

    origin = data["metadata"].get("origin_node", "GN_01")
    shelters = data["metadata"].get("target_shelters", ["GN_07", "GN_08"])
    best_path, best_cost = None, float("inf")
    for s in shelters:
        if s not in g:
            continue
        try:
            path = nx.astar_path(
                g,
                origin,
                s,
                heuristic=lambda a, b: haversine_m(
                    nodes[a]["lat"], nodes[a]["lon"], nodes[b]["lat"], nodes[b]["lon"]
                ),
                weight="weight",
            )
            cost = nx.astar_path_length(g, origin, s, weight="weight")
            if cost < best_cost:
                best_cost, best_path = cost, path
        except nx.NetworkXNoPath:
            continue

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    min_z = min(float(nodes[n]["z_elevation"]) for n in best_path) if best_path else 0.0
    max_w = max(float(nodes[n]["water_level_m"]) for n in best_path) if best_path else 99.0
    total_dist = sum(
        float(g.edges[best_path[i], best_path[i + 1]]["distance_m"])
        for i in range(len(best_path) - 1)
    ) if best_path else 0.0

    return {
        "team": "Team Alpha (Algorithm Optimization)",
        "model": "gemini-3.8-flash + networkx",
        "node_path": best_path or [],
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
