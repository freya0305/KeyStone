# KY3 — Frontend Implementation

> Based on `workspaces/keystone/mockup/index.html` — convert mockup to real Next.js app.

---

## KY3.1 — Project Setup + Design System

**What**: Next.js 14 app with shadcn/ui + Tailwind.

**Deliverables**:
- `apps/web/` with Next.js 14 App Router
- Tailwind config with KeyStone design tokens:
  - Primary: indigo-600 (`#4F46E5`)
  - Background: stone-50 (`#FAFAF9`)
  - Success: green-600 / Warning: amber-500 / Error: red-500
- shadcn/ui components installed
- Dark mode support
- Inter font family

**Acceptance**: Mockup's visual style matches in code.

---

## KY3.2 — Navigation + Product Switcher

**What**: Top nav with dual-product switcher.

**Deliverables**:
- Sticky nav with KeyStone logo
- Product switcher: "For Job Seekers" | "For Recruiters"
- Job Seeker nav: Dashboard, Analyze, History
- Recruiter nav: Dashboard, JD Generator, Templates
- User avatar + plan indicator (top right)

**Acceptance**:
- Clicking product switcher shows correct product views
- Mobile responsive (hamburger menu)

---

## KY3.3 — Recruiter JD Generator Page

**What**: Core recruiter workflow — JD creation with live preview.

**Layout**: Two-panel (input left, preview right)

**Input panel**:
- Job title (text input)
- Company name (text input)
- Company type (dropdown: Banking / FinTech / Startup / MNC / Other)
- Required skills (chip input — type to add, click to remove)
- Seniority (radio: Junior / Mid / Senior / Lead)

**Preview panel**:
- Live preview updates as user types
- JD content with formatting (sections: Overview, Responsibilities, Requirements, Nice to Have)
- Word count
- Action buttons: Copy Text, Share Link, Regenerate

**Generate button**: Triggers `POST /api/v1/recruiter/jd`, shows loading state, populates preview

**Acceptance**:
- All mockup interactions work (skills chips, live preview, generate simulation)
- Generate button calls real API endpoint
- Share link creates and copies to clipboard

---

## KY3.4 — Recruiter Dashboard + Templates

**What**: Dashboard stats and brand template management.

**Dashboard**:
- Stats cards: JDs Created (this month), Templates, Share Links, Avg Rating
- Quick action: "New JD" button

**Templates page**:
- Template list with preview thumbnails
- "Create Template" form: name, upload logo, pick brand colors
- Apply template to JD generation

**Acceptance**:
- Dashboard stats match API data
- Template CRUD works end-to-end

---

## KY3.5 — Job Seeker Core Pages

**What**: Resume analysis flow (based on existing M2-M5 todos, simplified).

**Analyze page**:
- Upload resume (PDF/DOCX) or paste text
- Paste job description
- "Analyze" button → match breakdown

**Match display**:
- Overall match % with bar
- Skills match list (green/amber/red)
- Section-by-section suggestions

**Acceptance**:
- Resume parsing works (extract text from PDF)
- Match calculation displays correctly
- Mockup interactions preserved

---

## KY3.6 — Mobile Responsive + Polish

**What**: Ensure all pages work on mobile.

**Acceptance**:
- All pages responsive down to 375px width
- Share view page (client-facing) fully mobile-friendly (red team finding F11)
- No horizontal scroll on any page
