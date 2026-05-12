"""Analytics service for application tracking dashboard.

Provides response rate calculations, stage funnel statistics, and trend analysis.
Quality gate: Only applications with ≥2 stage events are considered "active"
per mvp-scope.md Feature 4.
"""
import uuid
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncSession

from keystone.models.entities import Application, ApplicationStatus, ApplicationStage


class AnalyticsService:
    """Service for computing application analytics."""

    def __init__(self, db: AsyncSession):
        self.db = db

    def _is_active_stages_expression(self, min_stage_events: int = 2):
        """SQL expression to check if stages JSON array has ≥min_stage_events elements.

        Uses PostgreSQL's json_array_length function.
        For other dialects, falls back to Python-level filtering.
        """
        # PostgreSQL-specific: filter by JSON array length at SQL level
        # Stages must have at least min_stage_events entries to be "active"
        return func.json_array_length(Application.stages) >= min_stage_events

    async def get_active_applications(
        self, user_id: uuid.UUID, min_stage_events: int = 2
    ) -> list[Application]:
        """Get active applications with at least min_stage_events stage updates.

        Active applications are those that have had meaningful updates,
        indicating the user is actively tracking them.
        Quality gate (per mvp-scope.md Feature 4): Only applications with
        ≥2 status updates are recorded as 'active applications.'
        """
        # Query applications with at least the minimum number of stage events
        # using PostgreSQL's json_array_length for SQL-level filtering
        result = await self.db.execute(
            select(Application).where(
                Application.user_id == user_id,
                Application.auto_closed_at.is_(None),
                func.json_array_length(Application.stages) >= min_stage_events,
            )
        )
        return list(result.scalars().all())

    async def get_has_response(self, application_id: uuid.UUID) -> bool:
        """Check if an application has received a response (any stage with outcome 'received' or 'passed')."""
        result = await self.db.execute(
            select(ApplicationStage).where(
                ApplicationStage.application_id == application_id,
                ApplicationStage.outcome.in_(["received", "passed"]),
            )
        )
        stage = result.scalar_one_or_none()
        return stage is not None

    async def compute_response_rate(self, user_id: uuid.UUID) -> dict:
        """Compute response rate for a user's applications.

        Returns:
            Dictionary with total, responded count, and response_rate
        """
        active_apps = await self.get_active_applications(user_id)
        total = len(active_apps)

        if total == 0:
            return {"total": 0, "responded": 0, "response_rate": 0.0}

        responded = 0
        for app in active_apps:
            if await self.get_has_response(app.id):
                responded += 1

        response_rate = responded / total if total > 0 else 0.0

        return {
            "total": total,
            "responded": responded,
            "response_rate": response_rate,
        }

    async def compute_stage_stats(self, user_id: uuid.UUID) -> dict:
        """Compute per-stage pass rates.

        Returns:
            Dictionary mapping stage names to {count, pass_rate}
        """
        stages = ["applied", "response", "screening", "interview", "final", "decision"]
        stats = {}

        result = await self.db.execute(
            select(Application).where(
                Application.user_id == user_id,
                Application.auto_closed_at.is_(None),
            )
        )
        apps = result.scalars().all()

        for stage in stages:
            stage_apps = [a for a in apps if a.current_stage == stage]
            if stage_apps:
                passed = sum(
                    1 for a in stage_apps if a.final_outcome == "passed" or a.status == ApplicationStatus.OFFER
                )
                stats[stage] = {
                    "count": len(stage_apps),
                    "pass_rate": passed / len(stage_apps) if stage_apps else 0.0,
                }

        return stats

    def compute_trend(self, applications: list[Application]) -> list[dict]:
        """Compute monthly application trend.

        Returns:
            List of {month, count} dictionaries sorted by month
        """
        monthly: dict[str, int] = {}

        for app in applications:
            if app.created_at:
                month_key = app.created_at.strftime("%Y-%m")
                monthly[month_key] = monthly.get(month_key, 0) + 1

        # Convert to sorted list
        trend = [
            {"month": month, "count": count}
            for month, count in sorted(monthly.items())
        ]

        return trend

    def get_platform_benchmark(self) -> dict:
        """Get platform benchmark for comparison.

        Returns industry averages for response rates and stage conversion.
        These are placeholder values that would be computed from aggregate data.
        """
        # Industry benchmarks (placeholder - would be computed from aggregate data)
        return {
            "response_rate": 0.25,  # ~25% of applications get a response
            "screening_rate": 0.15,  # ~15% make it to screening
            "interview_rate": 0.05,  # ~5% get interviews
            "offer_rate": 0.02,  # ~2% receive offers
        }

    async def get_dashboard_data(self, user_id: uuid.UUID) -> dict:
        """Get complete dashboard data for a user.

        Returns:
            Dictionary with response_rate, stage_stats, trend, and benchmark
        """
        active_apps = await self.get_active_applications(user_id)
        total = len(active_apps)

        # Response rate
        response_info = await self.compute_response_rate(user_id)

        # Stage stats
        stage_stats = await self.compute_stage_stats(user_id)

        # Trend
        trend = self.compute_trend(active_apps)

        # Benchmark (only if >= 15 active apps)
        benchmark = None
        if total >= 15:
            benchmark = self.get_platform_benchmark()

        return {
            "response_rate": response_info["response_rate"],
            "total_active": total,
            "stage_stats": stage_stats,
            "trend": trend,
            "benchmark": benchmark,
        }
