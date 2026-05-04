# KY2 — Recruiter JD Tool Backend

> B2B JD generation: core API endpoints for the recruiter product.

---

## KY2.1 — JD Generation API

**What**: Core JD creation endpoint with Claude Haiku.

**Endpoint**: `POST /api/v1/recruiter/jd`

**Input**:
```json
{
  "title": "Senior Software Engineer",
  "company": "DBS Bank",
  "company_type": "banking",  // banking/fintech/startup/other
  "skills": ["Python", "AWS", "Microservices"],  // 5-10 skills
  "seniority": "senior"  // junior/mid/senior/lead
}
```

**Output**:
```json
{
  "id": "uuid",
  "title": "...",
  "company": "...",
  "content": "Full JD text...",
  "word_count": 450,
  "generated_at": "2026-05-04T..."
}
```

**Acceptance**:
- JD generated in <5s
- Output is 300-600 words
- Skills are mentioned contextually, not just a bullet list
- No NRIC or personal data in output

---

## KY2.2 — Share Links + Version History

**What**: JD sharing and version tracking.

**Endpoints**:
- `POST /api/v1/recruiter/jd/{id}/share` — create share link (7-day expiry, not 24h)
- `GET /api/v1/recruiter/share/{token}` — view shared JD (no auth required)
- `POST /api/v1/recruiter/jd/{id}/versions` — save version
- `GET /api/v1/recruiter/jd/{id}/versions` — list versions
- `POST /api/v1/recruiter/jd/{id}/restore/{version_id}` — restore version

**Share link expiry**: 7 days minimum (red team finding F4: 24h is too short)

**Acceptance**:
- Share link accessible without login
- Client can view JD on mobile
- Version history tracks all saves

---

## KY2.3 — Brand Templates API

**What**: Custom JD templates with brand colors/logo.

**Endpoints**:
- `POST /api/v1/recruiter/templates` — create template
- `GET /api/v1/recruiter/templates` — list tenant's templates
- `PUT /api/v1/recruiter/templates/{id}` — update template
- JD generation accepts `template_id` to apply brand styling

**Template data**: logo_s3_key, brand_primary_color, brand_secondary_color, font_choice

**Acceptance**:
- Template applied to JD preview
- PDF export uses brand colors (v2)

---

## KY2.4 — Team Management (B2B)

**What**: Multi-user team workspace.

**Endpoints**:
- `POST /api/v1/recruiter/team/invite` — invite user by email
- `GET /api/v1/recruiter/team/members` — list team members
- `PUT /api/v1/recruiter/team/members/{id}/role` — change role (admin/member)
- `DELETE /api/v1/recruiter/team/members/{id}` — remove member

**Access levels**: admin (full), member (create/edit own JDs)

**Acceptance**:
- Admin can see all team JDs
- Member can only see/edit their own JDs
- Team tier supports 5 seats

---

## KY2.5 — JD Quality Rating (Post-Generation)

**What**: Simple feedback loop on JD quality.

**Endpoint**: `POST /api/v1/recruiter/jd/{id}/rate`

**Input**: `{ "rating": 4, "feedback": "Good but salary range missing" }`

**Why (red team finding F6)**: Without this, we have no quality signal and will fly blind on whether the product is actually good.

**Acceptance**:
- Rating stored in DB
- Analytics endpoint shows average rating over time
- NPS calculation possible from ratings
