# Task 26: Implement suggestion-outcome correlation analysis

**Status**: pending
**Priority**: P0
**Source**: /redteam audit

## Description

VP2 core requirement: correlate SuggestionSignal records with Application outcomes.

## Requirements

1. Query joining SuggestionSignal → Application → outcome data
2. Aggregation: "Do apps where user accepted suggestions X,Y have higher response rates?"
3. Feed results back into suggestion ranking/scoring logic

This is the "validated AI recommendations" data flywheel.

## Value Proposition

Validated AI recommendations — model learns from outcome data which suggestions correlated with higher response rates.

## Files to examine

- src/keystone/api/job_seeker.py
- src/keystone/models/entities.py
