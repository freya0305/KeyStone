# KeyStone Implementation Roadmap

## Order of Execution

```
KY1 (Platform Foundation) ──┬── KY1.1 Scaffold + Docker Compose
                            ├── KY1.2 Database Schema + RLS
                            ├── KY1.3 Claude API Layer + Circuit Breaker  ← CRITICAL
                            ├── KY1.4 Stripe Webhook                       ← CRITICAL
                            └── KY1.5 Auth + PDPA + NRIC Detection
                                    │
          ┌─────────────────────────┴─────────────────────────┐
          ▼                                                   ▼
KY2 (Recruiter Backend)                              KY3 (Frontend)
    ├── KY2.1 JD Generation API                          ├── KY3.1 Project Setup
    ├── KY2.2 Share Links + Versions (7d)               ├── KY3.2 Nav + Product Switcher
    ├── KY2.3 Brand Templates API                        ├── KY3.3 JD Generator Page
    ├── KY2.4 Team Management                           ├── KY3.4 Dashboard + Templates
    └── KY2.5 JD Quality Rating                         └── KY3.5 Job Seeker Pages
                                                            │
                                                            ▼
                                                      KY3.6 Polish
```

## Critical Path (Must Fix Before Launch)

| # | Item | Why Critical |
|---|------|-------------|
| KY1.3 | Circuit Breaker | Claude API failure = entire product fails |
| KY1.4 | Stripe Webhook | No webhook = payments not confirmed |
| KY1.2 | RLS Enforcement | Data leak = trust destroyed |
| KY1.5 | NRIC Detection | PDPA violation = legal risk |
| KY1.3 | Haiku 4K Cap | Long JD truncated = broken output |
| KY2.2 | 7-day Share Link | 24h expiry = client can't review (F4) |
| KY2.5 | JD Quality Rating | No feedback = blind product (F6) |

## Assumptions

- User interviews deferred — feature set based on secondary research
- Pricing: Free (3 matches/month), Pro SGD 12/month (unlimited)
- Regional expansion deferred (Singapore first)
- Training data sources documented but not yet integrated

## Pre-Launch Checklist

- [ ] Circuit breaker tested (inject 5 failures, verify open)
- [ ] Stripe webhook tested (real payment flow)
- [ ] RLS tested (tenant A cannot read tenant B)
- [ ] NRIC detection verified (test with fake NRIC)
- [ ] Share link 7 days (not 24h)
- [ ] JD quality rating visible in analytics
