"""Sandbox Verification Engine executed by `antigravity-preview-09-2026`.

Audits candidate NetworkX A* evacuation paths over `data/gangnam_graphify.json`
against the GeoRescue 3D Flood Safety Invariants defined in `AGENTS.md`:
  - z_elevation > 18.5m (under water_level=2.0m basin surge)
  - z_elevation > current_water_depth
  - water_level_m <= 0.15m pedestrian wading safety threshold
  - Designated shelter reachability and Golden Time (<= 1800s)
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import sys
from typing import Any

from src.astar_evacuation import (
    AStarRoutingParams,
    EvacuationRouteResult,
    FloodAwareAStar,
)


@dataclass
class SafetyViolation:
    """Single safety invariant violation detected during sandbox audit."""

    invariant_id: str
    severity: str  # "CRITICAL" | "HIGH" | "MEDIUM"
    element_type: str  # "NODE" | "EDGE" | "ROUTE"
    element_id: str
    element_name: str
    observed_value: float
    threshold_value: float
    message: str


@dataclass
class SandboxAuditReport:
    """Structured audit report produced by `antigravity-preview-09-2026`."""

    agent_model: str
    sandbox_mode: str
    passed: bool
    status: str  # "VERIFIED_SAFE" | "UNSAFE_ROUTE_DETECTED" | "NO_ROUTE_FOUND"
    route: dict[str, Any]
    invariants_checked: dict[str, bool]
    violations: list[dict[str, Any]]
    recommended_blocked_nodes: list[str]
    recommended_blocked_edges: list[str]
    recommended_min_z_elevation_m: float
    recommended_max_water_level_m: float
    summary: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SandboxRouteVerifier:
    """Deterministic safety auditor for `antigravity-preview-09-2026`."""

    AGENT_MODEL = "antigravity-preview-09-2026"

    def __init__(self, graph_path: str | Path) -> None:
        self.engine = FloodAwareAStar(graph_path)
        thresholds = self.engine.metadata.get("safety_thresholds", {})
        self.scenario_water_level_m: float = float(
            thresholds.get("scenario_water_level_m", 2.0)
        )
        self.min_safe_z_elevation_m: float = float(
            thresholds.get("min_safe_z_elevation_m", 18.5)
        )
        self.safe_water_limit_m: float = float(
            thresholds.get("safe_water_level_limit_m", 0.15)
        )
        self.critical_water_limit_m: float = float(
            thresholds.get("critical_submerged_limit_m", 0.30)
        )
        self.max_shelter_water_m: float = float(
            thresholds.get("max_shelter_water_level_m", 0.05)
        )
        self.max_evacuation_time_sec: float = float(
            thresholds.get("max_evacuation_time_sec", 1800.0)
        )

    def verify_route(self, route: EvacuationRouteResult) -> SandboxAuditReport:
        """Audit a NetworkX A* evacuation route against GeoRescue 3D Safety Invariants."""
        violations: list[SafetyViolation] = []
        blocked_nodes: list[str] = []
        blocked_edges: list[str] = []

        if not route.found or not route.node_path:
            return SandboxAuditReport(
                agent_model=self.AGENT_MODEL,
                sandbox_mode="remote / proceed-in-sandbox (isolated)",
                passed=False,
                status="NO_ROUTE_FOUND",
                route=route.to_dict(),
                invariants_checked={
                    "INV_01_Z_ELEVATION_CLEARANCE": False,
                    "INV_02_HARD_FLOOD_DEPTH_LIMIT": False,
                    "INV_03_SHELTER_REACHABILITY": False,
                    "INV_04_EVACUATION_GOLDEN_TIME": False,
                },
                violations=[
                    asdict(
                        SafetyViolation(
                            invariant_id="INV_03_SHELTER_REACHABILITY",
                            severity="CRITICAL",
                            element_type="ROUTE",
                            element_id=route.origin_id,
                            element_name="No reachable path",
                            observed_value=0.0,
                            threshold_value=1.0,
                            message="NetworkX A* search found no reachable evacuation shelter path.",
                        )
                    )
                ],
                recommended_blocked_nodes=[],
                recommended_blocked_edges=[],
                recommended_min_z_elevation_m=self.min_safe_z_elevation_m,
                recommended_max_water_level_m=self.safe_water_limit_m,
                summary="[FAIL] No reachable shelter route found under current constraints.",
            )

        # Invariant 1: z_elevation > 18.5m and z_elevation > current_water_depth
        inv1_pass = True
        for step in route.steps:
            if (
                step.z_elevation <= self.min_safe_z_elevation_m
                or step.z_elevation <= step.current_water_depth
            ):
                inv1_pass = False
                severity = "CRITICAL" if step.z_elevation < 15.0 else "HIGH"
                violations.append(
                    SafetyViolation(
                        invariant_id="INV_01_Z_ELEVATION_CLEARANCE",
                        severity=severity,
                        element_type="NODE",
                        element_id=step.node_id,
                        element_name=step.node_name,
                        observed_value=step.z_elevation,
                        threshold_value=self.min_safe_z_elevation_m,
                        message=(
                            f"Node '{step.node_name}' ({step.node_id}) has z_elevation={step.z_elevation:.2f}m "
                            f"(<= required {self.min_safe_z_elevation_m:.2f}m flood plane under "
                            f"water_level={self.scenario_water_level_m:.1f}m; current_water_depth={step.current_water_depth:.2f}m)."
                        ),
                    )
                )
                if step.node_id != route.origin_id and step.node_id not in blocked_nodes:
                    blocked_nodes.append(step.node_id)

        # Invariant 2: Hard Flood Depth Limit (water_level_m <= 0.15m)
        inv2_pass = True
        for step in route.steps:
            if step.node_water_level_m > self.safe_water_limit_m:
                inv2_pass = False
                severity = (
                    "CRITICAL"
                    if step.node_water_level_m >= self.critical_water_limit_m
                    else "HIGH"
                )
                violations.append(
                    SafetyViolation(
                        invariant_id="INV_02_HARD_FLOOD_DEPTH_LIMIT",
                        severity=severity,
                        element_type="NODE",
                        element_id=step.node_id,
                        element_name=step.node_name,
                        observed_value=step.node_water_level_m,
                        threshold_value=self.safe_water_limit_m,
                        message=(
                            f"Node '{step.node_name}' ({step.node_id}) surface water_level_m="
                            f"{step.node_water_level_m:.2f}m exceeds safe limit ({self.safe_water_limit_m:.2f}m)."
                        ),
                    )
                )
                if step.node_id != route.origin_id and step.node_id not in blocked_nodes:
                    blocked_nodes.append(step.node_id)

            if step.edge_id and step.edge_water_level_m > self.safe_water_limit_m:
                inv2_pass = False
                severity = (
                    "CRITICAL"
                    if step.edge_water_level_m >= self.critical_water_limit_m
                    else "HIGH"
                )
                violations.append(
                    SafetyViolation(
                        invariant_id="INV_02_HARD_FLOOD_DEPTH_LIMIT",
                        severity=severity,
                        element_type="EDGE",
                        element_id=step.edge_id,
                        element_name=step.road_name or step.edge_id,
                        observed_value=step.edge_water_level_m,
                        threshold_value=self.safe_water_limit_m,
                        message=(
                            f"Road segment '{step.road_name}' ({step.edge_id}) water_level_m="
                            f"{step.edge_water_level_m:.2f}m exceeds safe limit ({self.safe_water_limit_m:.2f}m)."
                        ),
                    )
                )
                if step.edge_id not in blocked_edges:
                    blocked_edges.append(step.edge_id)

        # Invariant 3: Shelter Reachability & Safety
        inv3_pass = True
        dest_id = route.destination_id or route.node_path[-1]
        dest_node = self.engine.nodes.get(dest_id, {})
        dest_water = float(dest_node.get("water_level_m", 99.0))
        if not dest_node.get("is_shelter", False) or dest_water > self.max_shelter_water_m:
            inv3_pass = False
            violations.append(
                SafetyViolation(
                    invariant_id="INV_03_SHELTER_REACHABILITY",
                    severity="CRITICAL",
                    element_type="NODE",
                    element_id=dest_id,
                    element_name=dest_node.get("name", dest_id),
                    observed_value=dest_water,
                    threshold_value=self.max_shelter_water_m,
                    message=(
                        f"Destination '{dest_node.get('name', dest_id)}' ({dest_id}) fails shelter criteria "
                        f"(is_shelter=True, water_level_m <= {self.max_shelter_water_m:.2f}m)."
                    ),
                )
            )

        # Invariant 4: Evacuation Golden Time
        inv4_pass = route.estimated_time_sec <= self.max_evacuation_time_sec
        if not inv4_pass:
            violations.append(
                SafetyViolation(
                    invariant_id="INV_04_EVACUATION_GOLDEN_TIME",
                    severity="HIGH",
                    element_type="ROUTE",
                    element_id="->".join(route.node_path),
                    element_name="Total Evacuation Duration",
                    observed_value=route.estimated_time_sec,
                    threshold_value=self.max_evacuation_time_sec,
                    message=(
                        f"Estimated evacuation duration ({route.estimated_time_sec:.1f}s) exceeds "
                        f"Golden Time limit ({self.max_evacuation_time_sec:.1f}s)."
                    ),
                )
            )

        invariants_checked = {
            "INV_01_Z_ELEVATION_CLEARANCE": inv1_pass,
            "INV_02_HARD_FLOOD_DEPTH_LIMIT": inv2_pass,
            "INV_03_SHELTER_REACHABILITY": inv3_pass,
            "INV_04_EVACUATION_GOLDEN_TIME": inv4_pass,
        }
        passed = all(invariants_checked.values())
        status = "VERIFIED_SAFE" if passed else "UNSAFE_ROUTE_DETECTED"

        if passed:
            rec_water = self.safe_water_limit_m
            rec_z = self.min_safe_z_elevation_m
            summary = (
                f"[PASS / VERIFIED_SAFE] Route {' -> '.join(route.node_path)} verified safe "
                f"(min z_elevation={route.min_z_elevation_m:.2f}m > {self.min_safe_z_elevation_m:.2f}m, "
                f"max water_level_m={route.max_water_level_m:.2f}m <= {self.safe_water_limit_m:.2f}m, "
                f"ETA={route.estimated_time_sec:.1f}s)."
            )
        else:
            if route.max_water_level_m >= self.critical_water_limit_m:
                rec_water = self.critical_water_limit_m - 0.02
                rec_z = 16.0
            else:
                rec_water = self.safe_water_limit_m
                rec_z = self.min_safe_z_elevation_m
            summary = (
                f"[FAIL / UNSAFE_ROUTE_DETECTED] Route {' -> '.join(route.node_path)} triggered "
                f"{len(violations)} safety invariant violations "
                f"(min z_elevation={route.min_z_elevation_m:.2f}m, "
                f"max water_level_m={route.max_water_level_m:.2f}m)."
            )

        return SandboxAuditReport(
            agent_model=self.AGENT_MODEL,
            sandbox_mode="remote / proceed-in-sandbox (isolated)",
            passed=passed,
            status=status,
            route=route.to_dict(),
            invariants_checked=invariants_checked,
            violations=[asdict(v) for v in violations],
            recommended_blocked_nodes=blocked_nodes,
            recommended_blocked_edges=blocked_edges,
            recommended_min_z_elevation_m=round(rec_z, 2),
            recommended_max_water_level_m=round(rec_water, 3),
            summary=summary,
        )


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Run antigravity-preview-09-2026 sandbox verification on data/gangnam_graphify.json"
    )
    parser.add_argument(
        "--graph",
        type=str,
        default="data/gangnam_graphify.json",
        help="Path to Graphify JSON dataset",
    )
    parser.add_argument(
        "--params-json",
        type=str,
        default="{}",
        help="JSON string of AStarRoutingParams",
    )
    args = parser.parse_args()

    raw_params = json.loads(args.params_json)
    params = AStarRoutingParams(
        scenario_water_level_m=float(raw_params.get("scenario_water_level_m", 2.0)),
        min_safe_z_elevation_m=float(raw_params.get("min_safe_z_elevation_m", 0.0)),
        max_allowed_water_level_m=float(
            raw_params.get("max_allowed_water_level_m", 0.50)
        ),
        flood_penalty_weight=float(raw_params.get("flood_penalty_weight", 0.0)),
        elevation_bonus_weight=float(raw_params.get("elevation_bonus_weight", 0.0)),
        blocked_nodes=list(raw_params.get("blocked_nodes", [])),
        blocked_edges=list(raw_params.get("blocked_edges", [])),
        rationale=str(
            raw_params.get("rationale", "Sandbox CLI execution parameters.")
        ),
    )

    verifier = SandboxRouteVerifier(args.graph)
    route = verifier.engine.find_evacuation_route(params)
    report = verifier.verify_route(route)
    print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
