"""Entry point for the Gangnam Flood Evacuation A* Autonomous Verification Loop."""

from __future__ import annotations

import argparse
import asyncio
from pathlib import Path
import sys

from src.verification_pipeline import AutonomousVerificationLoopPipeline


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run Antigravity Autonomous Verification Loop "
            "(Lead Architect: gemini-4-argon, Sandbox Verifier: antigravity-preview-09-2026)"
        )
    )
    parser.add_argument(
        "--graph",
        type=str,
        default="data/gangnam_graphify.json",
        help="Path to the Gangnam Graphify JSON file",
    )
    parser.add_argument(
        "--agents-md",
        type=str,
        default="AGENTS.md",
        help="Path to the workspace AGENTS.md role specification",
    )
    parser.add_argument(
        "--report",
        type=str,
        default="reports/verification_report.json",
        help="Output path for the final JSON verification report",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=5,
        help="Maximum autonomous verification loop iterations",
    )
    return parser.parse_args()


async def async_main() -> int:
    args = parse_args()
    pipeline = AutonomousVerificationLoopPipeline(
        graph_path=Path(args.graph),
        agents_md_path=Path(args.agents_md),
        report_output_path=Path(args.report),
        max_iterations=args.max_iterations,
    )
    summary = await pipeline.run()
    if summary.get("converged", False):
        print(
            "[SUCCESS] Verified by Python A* Algorithm | "
            f"Safe Route: {' -> '.join(summary.get('final_node_path', []))} "
            f"(min_z_elevation={summary.get('min_z_elevation_m')}m > 18.5m, "
            f"max_water_level={summary.get('max_water_level_m')}m <= 0.15m)"
        )
        return 0
    return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(asyncio.run(async_main()))
