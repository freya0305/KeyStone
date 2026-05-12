# Task #16 — Analytics Dashboard with Thresholds

> Status: pending | Priority: CRITICAL | Depends on: Task #12 (quality gate)

---

## What

Dashboard showing: personal response rate, per-stage pass rates, applications by stage/month trend line. Minimum 5 applications before showing response rate. Minimum 15 before benchmark comparison.

---

## Deliverables

### 1. Analytics API endpoints

**File**: `src/keystone/api/analytics.py` (new file)

```python
@router.get("/analytics/dashboard")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
):
    # Only active applications (≥2 status updates)
    active_apps = await analytics.get_active_applications(current_user.id)

    if len(active_apps) < 5:
        return {
            "status": "insufficient_data",
            "active_count": len(active_apps),
            "required": 5,
            "message": "Add more applications to see your response rate"
        }

    # Response rate
    total = len(active_apps)
    responded = sum(1 for a in active_apps if a.has_response)
    response_rate = responded / total

    # Per-stage pass rates
    stage_stats = compute_stage_stats(active_apps)

    # Trend line: applications by stage over time
    trend = compute_trend(active_apps)

    # Benchmark comparison (requires ≥15 active apps)
    benchmark = None
    if total >= 15:
        benchmark = get_platform_benchmark()

    return {
        "response_rate": response_rate,
        "total_active": total,
        "stage_stats": stage_stats,
        "trend": trend,
        "benchmark": benchmark,
    }

def compute_stage_stats(apps):
    stages = ["applied", "response", "screening", "interview", "final", "decision"]
    stats = {}
    for stage in stages:
        stage_apps = [a for a in apps if a.current_stage == stage]
        if stage_apps:
            passed = sum(1 for a in stage_apps if a.outcome == "passed")
            stats[stage] = {
                "count": len(stage_apps),
                "pass_rate": passed / len(stage_apps) if stage_apps else 0
            }
    return stats
```

### 2. Dashboard frontend page

**File**: `apps/web/src/app/(app)/app/analytics/page.tsx` (new)

Components:

- Response rate card (large percentage, trend arrow)
- Stage funnel visualization (how many pass each stage)
- Monthly applications chart (bar chart by month)
- Benchmark comparison card (if ≥15 apps)

```typescript
// Show message if < 5 applications
if (data.status === "insufficient_data") {
  return (
    <div className="analytics-empty">
      <p>You've tracked {data.active_count} active applications.</p>
      <p>Add {data.required - data.active_count} more to see your response rate.</p>
    </div>
  )
}
```

---

## Acceptance Criteria

- [ ] Dashboard requires ≥5 active applications to show response rate
- [ ] Response rate shows as percentage with trend indicator
- [ ] Per-stage pass rate funnel displayed
- [ ] Monthly trend bar chart rendered
- [ ] Benchmark comparison only shown when ≥15 active applications
- [ ] Insufficient data state shows friendly message with progress
