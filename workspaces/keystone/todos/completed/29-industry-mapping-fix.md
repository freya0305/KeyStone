# Task 29: Fix industry field mapping for JD Generator

**Status**: pending
**Priority**: P1
**Created**: 2026-05-11
**Source**: /redteam audit

## Description

4 industries map to "other" causing no skill data match:

- Marketing & Communications
- Sales & Business Development
- Human Resources
- Operations & Logistics
- Legal & Compliance

## Requirements

Add these to industry_map in jd_generator.py, or add skill frequency data for "other" baseline.

## Files to modify

- src/keystone/api/jd_generator.py
