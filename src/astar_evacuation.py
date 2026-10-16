"""NetworkX-based flood-aware A* evacuation pathfinding engine for GeoRescue 3D."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
import math
from pathlib import Path
from typing import Any

import networkx as nx


@dataclass
class AStarRoutingParams:
    """Parameters tuned by Lead Orchestrator (gemini-4-argon) across verification iterations."""

    scenario_water_level_m: float = 2.0
    min_safe_z_elevation_m: float = 0.0
    max_allowed_water_level_m: float = 0.50
    flood_penalty_weight: float = 0.0
    elevation_bonus_weight: float = 0.0
    blocked_nodes: list[str] = field(default_factory=list)
    blocked_edges: list[str] = field(default_factory=list)
    rationale: str = "Initial baseline geometric A* search (distance-prioritized)."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RouteStep:
    """Single node/edge step along a candidate evacuation route."""

    node_id: str
    node_name: str
    z_elevation: float
    current_water_depth: float
    node_water_level_m: float
    edge_id: str | None = None
    road_name: str | None = None
    edge_distance_m: float = 0.0
    edge_water_level_m: float = 0.0
    step_time_sec: float = 0.0


@dataclass
class EvacuationRouteResult:
    """Candidate NetworkX A* evacuation route output."""

    found: bool
    origin_id: str
    destination_id: str | None
    node_path: list[str]
    edge_path: list[str]
    steps: list[RouteStep]
    total_distance_m: float
    min_z_elevation_m: float
    max_node_water_level_m: float
    max_edge_water_level_m: float
    max_water_level_m: float
    estimated_time_sec: float
    total_weighted_cost: float
    params_used: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "found": self.found,
            "origin_id": self.origin_id,
            "destination_id": self.destination_id,
            "node_path": self.node_path,
            "edge_path": self.edge_path,
            "steps": [asdict(s) for s in self.steps],
            "total_distance_m": round(self.total_distance_m, 2),
            "min_z_elevation_m": round(self.min_z_elevation_m, 2),
            "max_node_water_level_m": round(self.max_node_water_level_m, 3),
            "max_edge_water_level_m": round(self.max_edge_water_level_m, 3),
            "max_water_level_m": round(self.max_water_level_m, 3),
            "estimated_time_sec": round(self.estimated_time_sec, 2),
            "total_weighted_cost": round(self.total_weighted_cost, 2),
            "params_used": self.params_used,
        }


class FloodAwareAStar:
    """NetworkX A* pathfinder over Gangnam flood graph data."""

    def __init__(self, graph_path: str | Path) -> None:
        self.graph_path = Path(graph_path)
        with self.graph_path.open("r", encoding="utf-8") as f:
            self.raw_data: dict[str, Any] = json.load(f)

        self.metadata: dict[str, Any] = self.raw_data.get("metadata", {})
        self.nodes: dict[str, dict[str, Any]] = {
            n["id"]: n for n in self.raw_data.get("nodes", [])
        }
        raw_edges = self.raw_data.get("edges") or self.raw_data.get("links", [])
        self.edges: list[dict[str, Any]] = raw_edges

        # Build base NetworkX Graph
        self.base_graph = nx.Graph()
        for node_id, attrs in self.nodes.items():
            self.base_graph.add_node(node_id, **attrs)
        for edge in self.edges:
            u = edge["source"]
            v = edge["target"]
            if u in self.nodes and v in self.nodes:
                self.base_graph.add_edge(u, v, **edge)

    @staticmethod
    def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Compute great-circle distance in meters between two WGS84 coordinates."""
        radius_m = 6_371_000.0
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = (
            math.sin(dphi / 2.0) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
        )
        return 2.0 * radius_m * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    @staticmethod
    def compute_walking_speed_mps(
        water_level_m: float, base_speed_mps: float = 1.35
    ) -> float:
        """Model pedestrian wading speed reduction as flood depth increases."""
        if water_level_m <= 0.02:
            return base_speed_mps
        reduction_factor = max(0.20, 1.0 - 1.85 * water_level_m)
        return base_speed_mps * reduction_factor

    def _build_filtered_nx_graph(self, params: AStarRoutingParams) -> nx.Graph:
        """Build a filtered NetworkX graph applying Lead Agent constraints and edge weights."""
        g = nx.Graph()
        blocked_nodes_set = set(params.blocked_nodes)
        blocked_edges_set = set(params.blocked_edges)

        for node_id, attrs in self.nodes.items():
            if node_id in blocked_nodes_set:
                continue
            z_elev = float(attrs.get("z_elevation", attrs.get("elevation_m", 0.0)))
            if z_elev < params.min_safe_z_elevation_m:
                continue
            g.add_node(node_id, **attrs)

        for edge in self.edges:
            u, v = edge["source"], edge["target"]
            if u not in g or v not in g:
                continue
            edge_id = edge.get("id", f"{u}->{v}")
            if edge_id in blocked_edges_set:
                continue

            edge_water = float(edge.get("water_level_m", 0.0))
            u_water = float(self.nodes[u].get("water_level_m", 0.0))
            v_water = float(self.nodes[v].get("water_level_m", 0.0))
            segment_max_water = max(edge_water, u_water, v_water)

            if segment_max_water > params.max_allowed_water_level_m:
                continue

            distance_m = float(edge.get("distance_m", 100.0))
            mean_z = 0.5 * (
                float(self.nodes[u].get("z_elevation", 0.0))
                + float(self.nodes[v].get("z_elevation", 0.0))
            )
            flood_multiplier = 1.0 + params.flood_penalty_weight * (
                (segment_max_water / 0.15) ** 2
            )
            elev_discount = params.elevation_bonus_weight * max(0.0, mean_z - 18.5)
            weight = max(1.0, (distance_m * flood_multiplier) - elev_discount)
            g.add_edge(u, v, **edge, astar_weight=weight)

        return g

    def find_evacuation_route(
        self,
        params: AStarRoutingParams,
        origin_id: str | None = None,
        target_shelters: list[str] | None = None,
    ) -> EvacuationRouteResult:
        """Execute NetworkX A* search (`nx.astar_path`) from origin to the optimal shelter."""
        start_id = origin_id or self.metadata.get("origin_node", "GN_01")
        shelters = target_shelters or self.metadata.get("target_shelters") or [
            nid for nid, n in self.nodes.items() if n.get("is_shelter", False)
        ]
        base_speed = (
            self.metadata.get("safety_thresholds", {}).get("base_walking_speed_mps", 1.35)
        )

        g = self._build_filtered_nx_graph(params)
        if start_id not in g:
            return self._empty_result(start_id, params)

        best_path: list[str] | None = None
        best_cost = float("inf")
        best_shelter: str | None = None

        for shelter_id in shelters:
            if shelter_id not in g:
                continue
            try:
                candidate_path = nx.astar_path(
                    g,
                    source=start_id,
                    target=shelter_id,
                    heuristic=lambda u, v: self.haversine_m(
                        self.nodes[u]["lat"],
                        self.nodes[u]["lon"],
                        self.nodes[v]["lat"],
                        self.nodes[v]["lon"],
                    ),
                    weight="astar_weight",
                )
                candidate_cost = float(
                    nx.astar_path_length(
                        g,
                        source=start_id,
                        target=shelter_id,
                        heuristic=lambda u, v: self.haversine_m(
                            self.nodes[u]["lat"],
                            self.nodes[u]["lon"],
                            self.nodes[v]["lat"],
                            self.nodes[v]["lon"],
                        ),
                        weight="astar_weight",
                    )
                )
                if candidate_cost < best_cost:
                    best_cost = candidate_cost
                    best_path = candidate_path
                    best_shelter = shelter_id
            except nx.NetworkXNoPath:
                continue

        if not best_path or best_shelter is None:
            return self._empty_result(start_id, params)

        steps: list[RouteStep] = []
        origin_node = self.nodes[start_id]
        origin_z = float(origin_node.get("z_elevation", origin_node.get("elevation_m", 0.0)))
        steps.append(
            RouteStep(
                node_id=start_id,
                node_name=origin_node.get("name", start_id),
                z_elevation=origin_z,
                current_water_depth=float(
                    origin_node.get("current_water_depth", origin_node.get("water_level_m", 0.0))
                ),
                node_water_level_m=float(origin_node.get("water_level_m", 0.0)),
            )
        )

        total_dist = 0.0
        total_time = 0.0
        min_z_elev = origin_z
        max_node_w = float(origin_node.get("water_level_m", 0.0))
        max_edge_w = 0.0
        edge_ids: list[str] = []

        for idx in range(len(best_path) - 1):
            u, v = best_path[idx], best_path[idx + 1]
            edge_data = g.edges[u, v]
            next_node = self.nodes[v]
            e_id = edge_data.get("id", f"{u}->{v}")
            edge_ids.append(e_id)

            dist = float(edge_data.get("distance_m", 0.0))
            e_water = float(edge_data.get("water_level_m", 0.0))
            n_water = float(next_node.get("water_level_m", 0.0))
            n_z = float(next_node.get("z_elevation", next_node.get("elevation_m", 0.0)))
            n_depth = float(next_node.get("current_water_depth", n_water))

            effective_water = max(e_water, n_water)
            speed_mps = self.compute_walking_speed_mps(effective_water, base_speed)
            step_time = dist / speed_mps

            total_dist += dist
            total_time += step_time
            min_z_elev = min(min_z_elev, n_z)
            max_node_w = max(max_node_w, n_water)
            max_edge_w = max(max_edge_w, e_water)

            steps.append(
                RouteStep(
                    node_id=v,
                    node_name=next_node.get("name", v),
                    z_elevation=n_z,
                    current_water_depth=n_depth,
                    node_water_level_m=n_water,
                    edge_id=e_id,
                    road_name=edge_data.get("road_name", e_id),
                    edge_distance_m=dist,
                    edge_water_level_m=e_water,
                    step_time_sec=round(step_time, 2),
                )
            )

        return EvacuationRouteResult(
            found=True,
            origin_id=start_id,
            destination_id=best_shelter,
            node_path=best_path,
            edge_path=edge_ids,
            steps=steps,
            total_distance_m=total_dist,
            min_z_elevation_m=min_z_elev,
            max_node_water_level_m=max_node_w,
            max_edge_water_level_m=max_edge_w,
            max_water_level_m=max(max_node_w, max_edge_w),
            estimated_time_sec=total_time,
            total_weighted_cost=best_cost,
            params_used=params.to_dict(),
        )

    @staticmethod
    def _empty_result(
        start_id: str, params: AStarRoutingParams
    ) -> EvacuationRouteResult:
        return EvacuationRouteResult(
            found=False,
            origin_id=start_id,
            destination_id=None,
            node_path=[],
            edge_path=[],
            steps=[],
            total_distance_m=0.0,
            min_z_elevation_m=0.0,
            max_node_water_level_m=0.0,
            max_edge_water_level_m=0.0,
            max_water_level_m=0.0,
            estimated_time_sec=0.0,
            total_weighted_cost=float("inf"),
            params_used=params.to_dict(),
        )
