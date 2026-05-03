# KeyStone B2B JD Generation Tool — Frontend Design

> Phase 02 Plan — 2026-05-03
> Target User: Recruitment agencies (recruiters writing 10–50 JDs/day)
> Design Principle: Fast = minimal clicks to professional JD output

---

## 1. Product Position

**This is a TOOL, not a platform.**

| Input | Output |
|--------|--------|
| Job title | Professionally written JD |
| Required skills | Candidate persona |
| Experience requirements | Market insights |
| Company type | Client-ready format |
| Salary (optional) | |

**NOT:** Resume matching, candidate search, ATS features

---

## 2. UI/UX Principles

### Core UX Mandate
Recruiters are busy. Every screen must minimize clicks to result.

| Principle | Implication |
|-----------|-------------|
| **Mobile-friendly?** | Desktop-primary (recruiters use desktop), but responsive for candidate calls |
| **Light/dark mode?** | Light mode default — professional, readable; dark mode toggle |
| **Single-page app vs wizard?** | SPA with contextual panels — no full-page navigation |
| **Max clicks to JD** | 3 clicks from dashboard to generated JD |

### Visual Design Direction
- **Style**: Clean, professional, minimal chrome
- **Primary color**: Deep indigo `#4F46E5` (trust, professionalism)
- **Accent**: Warm amber `#F59E0B` (highlights, CTAs)
- **Background**: Light gray `#F9FAFB` (light mode), dark `#111827` (dark mode)
- **Typography**: Inter (primary), system-ui fallback
- **Density**: Medium-high — recruiters need information density

---

## 3. Key Screens

### 3.1 Dashboard (Home)

**Purpose**: At-a-glance summary, quick-start JD creation, recent activity

```
┌─────────────────────────────────────────────────────────────────┐
│  [Logo] KeyStone          [Dark Mode] [Settings] [Avatar ▼]     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Welcome back, Sarah                                          │
│                                                                 │
│  ┌─────────────────────┐  ┌─────────────────────┐             │
│  │   + Create New JD   │  │   My Templates      │             │
│  │   (Primary CTA)     │  │   (Quick access)    │             │
│  └─────────────────────┘  └─────────────────────┘             │
│                                                                 │
│  Your Plan: Pro ($69/mo)                        [Upgrade ↑]     │
│  JDs this month: 23/∞                                            │
│  ████████████████░░░░░░░░░ 23/∞                                │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Recent JDs                                      [View All →]    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 📄 Senior Software Engineer · TechCorp · 2h ago         │   │
│  │ 📄 Marketing Manager · Digital Agency · Yesterday       │   │
│  │ 📄 Sales Executive · fintech startup · 2 days ago       │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  Quick Stats                                                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                    │
│  │ 47       │  │ 12       │  │ 89%      │                    │
│  │ JDs Created│  │ Templates │  │ Client Approval│          │
│  └──────────┘  └──────────┘  └──────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Layout rules**:
- Primary CTA "Create New JD" is always visible, above fold
- Recent JDs show last 3, full list on "View All"
- Stats are informational (not gamified)
- No distracting metrics or charts on main view

### 3.2 JD Generator (Main Tool)

**Purpose**: Single-screen workflow — input on left, live preview on right

```
┌─────────────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard          JD Generator              [Save Draft] │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌──────────────────────────┐  ┌────────────────────────────────┐│
│  │  JOB DETAILS              │  │  LIVE PREVIEW                   ││
│  │                          │  │                                 ││
│  │  Job Title *             │  │  [Real-time JD preview here]     ││
│  │  ┌──────────────────────┐│  │                                 ││
│  │  │ Senior Software      ││  │  Loading skeleton until first   ││
│  │  │ Engineer            ││  │  field is filled                ││
│  │  └──────────────────────┘│  │                                 ││
│  │                          │  │                                 ││
│  │  Company Name *          │  │                                 ││
│  │  ┌──────────────────────┐│  │                                 ││
│  │  │ TechCorp Pte Ltd    ││  │                                 ││
│  │  └──────────────────────┘│  │                                 ││
│  │                          │  │                                 ││
│  │  Company Type            │  │                                 ││
│  │  [MNC              ▼]    │  │                                 ││
│  │                          │  │                                 ││
│  │  Location                │  │                                 ││
│  │  ┌──────────────────────┐│  │                                 ││
│  │  │ Singapore (Remote)  ││  │                                 ││
│  │  └──────────────────────┘│  │                                 ││
│  │                          │  │                                 ││
│  │  ─────────────────────── │  │                                 ││
│  │                          │  │                                 ││
│  │  REQUIREMENTS            │  │                                 ││
│  │                          │  │                                 ││
│  │  Required Skills *       │  │                                 ││
│  │  ┌──────────────────────┐│  │                                 ││
│  │  │ Python, AWS, Docker  ││  │                                 ││
│  │  │ + Add skill         ││  │                                 ││
│  │  └──────────────────────┘│  │                                 ││
│  │  [Chip: Python] [Chip: AWS] [Chip: Docker] [+ Add]            ││
│  │                          │  │                                 ││
│  │  Experience *            │  │                                 ││
│  │  ┌──────────────────────┐│  │                                 ││
│  │  │ 5+ years in software││  │                                 ││
│  │  │ development         ││  │                                 ││
│  │  └──────────────────────┘│  │                                 ││
│  │                          │  │                                 ││
│  │  Education               │  │                                 ││
│  │  [Bachelor's Degree  ▼] │  │                                 ││
│  │                          │  │                                 ││
│  │  ─────────────────────── │  │                                 ││
│  │                          │  │                                 ││
│  │  COMPENSATION (Optional) │  │                                 ││
│  │                          │  │                                 ││
│  │  Salary Range            │  │                                 ││
│  │  ┌────────┐ - ┌────────┐│  │                                 ││
│  │  │ $8,000 │   │ $12,000││  │                                 ││
│  │  └────────┘   └────────┘│  │                                 ││
│  │                          │  │                                 ││
│  │  [ ] Hide salary in JD  │  │                                 ││
│  │                          │  │                                 ││
│  │  ─────────────────────── │  │                                 ││
│  │                          │  │                                 ││
│  │  JD LENGTH               │  │                                 ││
│  │  [Standard (500-700w) ▼]│  │                                 ││
│  │                          │  │                                 ││
│  │  TONE                    │  │                                 ││
│  │  [Professional     ▼]   │  │                                 ││
│  │                          │  │                                 ││
│  │  ┌──────────────────────┐│  │                                 ││
│  │  │   Generate JD →     ││  │                                 ││
│  │  └──────────────────────┘│  │                                 ││
│  │                          │  │                                 ││
│  └──────────────────────────┘  └────────────────────────────────┘│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Key UX Decisions**:
1. **Two-panel layout**: Input left, live preview right — no switching pages
2. **Live preview updates as user types** (debounced 300ms)
3. **Skills as chips**: Easy add/remove, no manual comma parsing
4. **Progressive disclosure**: Compensation and tone are collapsed by default
5. **Template selector**: "Start from scratch" or "Use a template" before form

**Post-Generation Actions**:
```
┌─────────────────────────────────────────────────────────────────┐
│  JD Generated ✓                            [Copy] [Download ▼]   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │ [Edit ▼]    [Regenerate]    [Create Similar JD]          │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
│  [Save to Templates] [Send to Client] [Add to Job Board]        │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 Template Manager

**Purpose**: Create, edit, and organize reusable JD templates

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard          Template Manager                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [+ Create Template]                    [Search: ____________]   │
│                                                                 │
│  My Templates (12)                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ┌─────┐                                                    ││
│  │ │ 📄  │  Software Engineer (Generic)         [Edit] [···] ││
│  │ └─────┘  Used 23 times · Last used 2h ago                 ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ┌─────┐                                                    ││
│  │ │ 📄  │  Sales Representative                 [Edit] [···] ││
│  │ └─────┘  Used 15 times · Last used Yesterday              ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ┌─────┐                                                    ││
│  │ │ 📄  │  Marketing Coordinator                 [Edit] [···] ││
│  │ └─────┘  Used 8 times · Last used 3 days ago              ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Team Templates (3)                          [Request Access →] │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ ┌─────┐                                                    ││
│  │ │ 👥  │  Standard JD Format (Agency)          [Copy] [···] ││
│  │ └─────┘  Created by: Agency Admin · Used 45 times          ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Template Card States**:
- Default: Shows title, usage count, last-used
- Hover: Shows preview snippet
- [···] menu: Edit, Duplicate, Delete, Share (Team only)

### 3.4 Team Management (Team Plan Only)

**Purpose**: Manage team members, roles, and shared templates

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard          Team Management                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Your Team (3/5)                              [+ Invite Member] │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 👤 Sarah Chen (You)              Owner     admin@agency.com  ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 👤 Marcus Tan                      Editor   marcus@agency.com ││
│  │    Can create and edit JDs      [Remove]                    ││
│  └─────────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 👤 Lisa Wong                       Viewer  lisa@agency.com   ││
│  │    View-only access               [Remove]                  ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  Shared Templates                                              │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ [✓] Software Engineer (Agency)                             ││
│  │ [✓] Sales JD Standard                                       ││
│  │ [ ] Marketing Roles                                         ││
│  └─────────────────────────────────────────────────────────────┘│
│  [Save Changes]                                                │
│                                                                 │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Team Usage                                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ Sarah Chen    ████████████████████░░░░ 24 JDs               ││
│  │ Marcus Tan    ██████████░░░░░░░░░░░░░░░░ 11 JDs            ││
│  │ Lisa Wong     ████░░░░░░░░░░░░░░░░░░░░░░░ 4 JDs           ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Role Permissions**:
| Role | Create JD | Edit Templates | Manage Team | Billing |
|------|-----------|----------------|-------------|---------|
| Owner | ✓ | ✓ | ✓ | ✓ |
| Editor | ✓ | ✓ | ✗ | ✗ |
| Viewer | ✓ (read-only) | ✗ | ✗ | ✗ |

### 3.5 Settings / Billing

**Purpose**: Account settings, subscription management, billing history

```
┌─────────────────────────────────────────────────────────────────┐
│  ← Back to Dashboard          Settings                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [Profile]  [Billing]  [Templates]  [Team]  [Security]        │
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  Billing & Subscription                                         │
│                                                                 │
│  Current Plan: Pro                                              │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 💎 Pro — $69/month                                       │  │
│  │                                                          │  │
│  │ • Unlimited JDs                                          │  │
│  │ • Unlimited templates                                    │  │
│  │ • Export to PDF, Word                                    │  │
│  │ • Priority support                                       │  │
│  │                                                          │  │
│  │ [Upgrade to Team ($179/mo)]                              │  │
│  │ [Cancel Subscription]                                   │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Payment Method                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ 💳 •••• •••• •••• 4242                                  │  │
│  │ Visa expires 12/2027                        [Update →]   │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Billing History                                                │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ May 1, 2026    Pro Plan         $69.00       [Receipt] │  │
│  │ Apr 1, 2026    Pro Plan         $69.00       [Receipt] │  │
│  │ Mar 1, 2026    Pro Plan         $69.00       [Receipt] │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
│  Usage This Month                                               │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │ JDs Created: 47                                          │  │
│  │ Templates Used: 8                                        │  │
│  │ Storage: 2.3 MB                                          │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Inventory

### 4.1 JD Form Components

| Component | States | Notes |
|-----------|--------|-------|
| **Text Input** | Default, Focus, Filled, Error, Disabled | Required fields marked with `*` |
| **Skills Chip Input** | Empty, Has chips, Focus | Chips removable with `×`, comma/completion adds new |
| **Select Dropdown** | Default, Open, Selected, Disabled | Company type, education level, JD length, tone |
| **Salary Range** | Empty, Filled, "Hide salary" checked | Dual input, optional |
| **Checkbox** | Unchecked, Checked | "Hide salary in JD" |
| **Primary Button** | Default, Hover, Active, Loading, Disabled | "Generate JD →" |
| **Secondary Button** | Default, Hover, Active | "Save Draft", "Cancel" |

### 4.2 JD Preview/Editor Components

| Component | States | Notes |
|-----------|--------|-------|
| **Live Preview Panel** | Loading skeleton, Rendering, Complete | Updates debounced 300ms |
| **JD Sections** | Collapsed, Expanded | Sections: Summary, Responsibilities, Requirements, Benefits |
| **Inline Edit** | View mode, Edit mode | Click section to edit inline |
| **Word Count Badge** | Under target, In range, Over target | Color-coded |
| **Regenerate Button** | Default, Loading | Regenerates with same inputs |
| **Diff View** | Original, Generated | Toggle to compare changes |

### 4.3 Template Selector

| Component | States | Notes |
|-----------|--------|-------|
| **Template Card** | Default, Hover, Selected | Shows title, preview snippet, usage count |
| **Template Preview Modal** | Loading, Loaded | Full preview before selecting |
| **Empty State** | No templates | "Start from scratch" option prominent |

### 4.4 Export Options

| Component | States | Notes |
|-----------|--------|-------|
| **Copy Button** | Default, Copied ✓ | Copies rich text to clipboard |
| **Download Dropdown** | Closed, Open | PDF, Word (.docx), Plain text |
| **Share Button** | Default, Sending, Sent | Email JD directly to client |

### 4.5 Analytics Dashboard

| Component | States | Notes |
|-----------|--------|-------|
| **Stat Card** | Loading, Loaded | Large number, label, optional trend |
| **Usage Chart** | Empty, Partial, Full | Monthly JD creation over time |
| **Template Usage Table** | Loading, Loaded | Template name, use count, last used |
| **Client Approval Rate** | Calculated | "X% of JDs approved by client" |

---

## 5. User Flows

### 5.1 Onboarding (Quick Start)

```
Step 1: Sign Up / Log In
         ↓
Step 2: Select Plan (Solo/Pro/Team) or "Start Free Trial"
         ↓
Step 3: Quick tour (skippable, 3 screens):
         - "Add job details on the left"
         - "See your JD preview on the right"
         - "Export when ready"
         ↓
Step 4: Land on Dashboard with "Create New JD" CTA prominent
```

**Onboarding principles**:
- No email verification gate before first JD
- First JD always generates (build trust before paywall)
- Quick tour is 3 screenshots, not a video

### 5.2 Core JD Generation Flow

```
Dashboard → Click "Create New JD"
         ↓
JD Generator (blank form)
         ↓
Optional: Select Template (or start from scratch)
         ↓
Fill required fields (title, company, skills, experience)
         ↓
Optional: Expand compensation, tone, length
         ↓
Click "Generate JD →"
         ↓
Live preview shows generated JD (3-5 seconds)
         ↓
Review JD
  ├── Satisfied → [Copy] / [Download] / [Save to Templates]
  ├── Needs tweaks → [Edit section] or [Regenerate]
  └── Similar JD needed → [Create Similar JD] (pre-fills form)
         ↓
Save to Templates (optional)
         ↓
Send to Client or Download
         ↓
Return to Dashboard
```

**Key decision points**:
- Template selection is pre-form (reduces friction)
- Live preview eliminates "submit and wait" anxiety
- Post-generation actions are immediate, no modal

### 5.3 Template Creation Flow

```
Template Manager → Click "Create Template"
         ↓
Template Editor (blank)
         ↓
Enter template name
         ↓
Build template sections:
  - Default JD sections (Summary, Responsibilities, etc.)
  - Custom sections
  - Placeholder syntax for: {job_title}, {company_name}, {skills}, etc.
         ↓
Preview with sample data
         ↓
Save Template
         ↓
Template available in JD Generator
```

**Placeholder system**:
```
{job_title}       → "Senior Software Engineer"
{company_name}    → "TechCorp Pte Ltd"
{required_skills} → "Python, AWS, Docker"
{experience}      → "5+ years"
{salary_range}    → "$8,000 - $12,000" or "Competitive"
{location}        → "Singapore (Remote)"
```

### 5.4 Team Collaboration Flow

```
Team Owner: Invite member via email
         ↓
Invited member receives email with link
         ↓
Member signs up/logs in, added to team
         ↓
Member sees Team Templates in Template Manager
         ↓
Member creates JD (uses team or personal templates)
         ↓
Owner sees team usage in Team Management
         ↓
Owner can promote/demote roles, remove members
```

**Team features by plan**:
| Feature | Solo | Pro | Team |
|---------|------|-----|------|
| Single user | ✓ | ✓ | ✓ (1 owner + 4) |
| Personal templates | ✓ | ✓ | ✓ |
| Team templates | ✗ | ✗ | ✓ |
| Team usage tracking | ✗ | ✗ | ✓ |
| Role management | ✗ | ✗ | ✓ |

---

## 6. Technical Stack Confirmation

### Confirmed Stack
| Layer | Technology | Notes |
|-------|------------|-------|
| **Framework** | Next.js 14+ (App Router) | SPA behavior with SSR benefits |
| **Styling** | Tailwind CSS | Utility-first, consistent with shadcn/ui |
| **Components** | shadcn/ui | Accessible, customizable |
| **State** | React Context + useState | Simple, no Redux needed for this scope |
| **Forms** | React Hook Form + Zod | Validation, schema-based |
| **HTTP** | fetch or Axios | Standard |

### Additional Libraries

| Library | Purpose | Justification |
|---------|---------|---------------|
| **@tiptap/react** | Rich text editor | For inline JD editing in preview |
| **html2pdf.js** | PDF export | Client-side PDF generation |
| **docx** | Word export | Generate .docx files |
| **Framer Motion** | Animations | Smooth transitions, loading states |
| **Lucide React** | Icons | Consistent with shadcn/ui |
| **date-fns** | Date formatting | Billing dates, usage stats |

### File Structure (Proposed)

```
apps/web/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── signup/
│   ├── (dashboard)/
│   │   ├── layout.tsx          # Authenticated shell
│   │   ├── page.tsx            # Dashboard
│   │   ├── jd/
│   │   │   ├── new/
│   │   │   └── [id]/
│   │   ├── templates/
│   │   ├── team/
│   │   └── settings/
│   ├── api/                    # API routes (or proxy to backend)
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── ui/                     # shadcn/ui components
│   ├── jd/
│   │   ├── jd-form.tsx
│   │   ├── jd-preview.tsx
│   │   ├── jd-editor.tsx
│   │   └── skills-input.tsx
│   ├── templates/
│   │   ├── template-card.tsx
│   │   └── template-editor.tsx
│   ├── dashboard/
│   │   ├── stats-card.tsx
│   │   └── recent-jds.tsx
│   └── team/
│       ├── team-member-row.tsx
│       └── usage-chart.tsx
├── lib/
│   ├── utils.ts
│   ├── api.ts                  # API client
│   └── constants.ts
├── hooks/
│   ├── use-jd-generation.ts
│   ├── use-templates.ts
│   └── use-team.ts
└── types/
    └── index.ts                # TypeScript types
```

---

## 7. Responsive Behavior

### Desktop-First Breakpoints

| Breakpoint | Behavior |
|------------|----------|
| < 768px (Mobile) | Stack form above preview, collapsible sections |
| 768-1024px (Tablet) | Narrower panels, condensed spacing |
| > 1024px (Desktop) | Full two-panel layout |

### Mobile Adaptations

```
Mobile (< 768px):
┌─────────────────────┐
│  JD Generator   [←] │
├─────────────────────┤
│  [Form Fields]      │
│  ─────────────────  │
│  [Show Preview ▼]   │
│  ─────────────────  │
│  [Generated JD]      │
└─────────────────────┘
```

- Form inputs are full-width
- Preview collapses by default, expandable
- Sticky "Generate" button at bottom

---

## 8. Dark Mode

```
Light Mode (Default):
- Background: #F9FAFB
- Surface: #FFFFFF
- Primary: #4F46E5
- Text: #111827

Dark Mode:
- Background: #111827
- Surface: #1F2937
- Primary: #6366F1 (lighter for contrast)
- Text: #F9FAFB
```

- Toggle in header (sun/moon icon)
- Persisted in localStorage
- System preference detection on first load

---

## 9. Loading & Empty States

### JD Generation Loading
```
While generating (3-5s):
┌─────────────────────────────────────┐
│  Generating your JD...              │
│  ████████████░░░░░░░  60%           │
│                                     │
│  "Crafting a compelling role         │
│   summary for Senior Software        │
│   Engineer at TechCorp..."           │
└─────────────────────────────────────┘
```
- Progress bar (real, not fake)
- Contextual message about what AI is doing
- Do NOT say "AI is thinking"

### Empty States

| Screen | Empty State |
|--------|-------------|
| Dashboard (no JDs) | "No JDs yet. Create your first one." + CTA |
| Templates (no templates) | "No templates. Save your next JD as a template." |
| Team (no members) | "Invite team members to collaborate." + CTA |
| JD Preview (form empty) | Skeleton with field placeholders |

---

## 10. Error Handling

| Scenario | UX Treatment |
|----------|--------------|
| **Network error on submit** | Toast: "Connection error. Your draft is saved." + Retry button |
| **Generation failed** | Inline error: "Couldn't generate JD. [Try again]" + specific reason |
| **Template load failed** | Skeleton fallback, then retry |
| **Session expired** | Redirect to login with "Session expired" message |
| **Rate limit hit** | Toast: "You've reached your JD limit. Upgrade for unlimited." |

---

## 11. Accessibility

| Requirement | Implementation |
|-------------|----------------|
| Tap targets | Minimum 44×44px |
| Color contrast | WCAG AA (4.5:1 minimum) |
| Focus states | Visible focus rings, never hidden |
| Keyboard navigation | Full tab order, shortcuts for power users |
| Screen reader | ARIA labels on all interactive elements |
| Form errors | Inline, associated with fields |

### Keyboard Shortcuts (Power Users)

| Key | Action |
|-----|--------|
| `Cmd/Ctrl + N` | New JD |
| `Cmd/Ctrl + S` | Save draft |
| `Cmd/Ctrl + Enter` | Generate JD |
| `Cmd/Ctrl + E` | Export (opens dropdown) |
| `Escape` | Close modal / cancel edit |

---

## 12. Implementation Phases

| Phase | Components | Effort |
|-------|------------|--------|
| **Phase 1** | Shell/layout, Dashboard, JD Form | ~1 week |
| **Phase 2** | Live Preview, Generation flow | ~1 week |
| **Phase 3** | Template Manager, CRUD | ~1 week |
| **Phase 4** | Export (PDF/Word), Copy | ~3 days |
| **Phase 5** | Team Management (Team plan) | ~1 week |
| **Phase 6** | Settings/Billing, Dark mode | ~3 days |

---

## Summary: Key UX Decisions

1. **3 clicks to JD**: Dashboard → Fill required → Generate
2. **Two-panel layout**: Input left, live preview right — no page switches
3. **Live preview**: Updates as user types (debounced)
4. **Skills as chips**: No comma-parsing confusion
5. **Light mode default**: Professional, readable; dark mode toggle
6. **Desktop-first, mobile-responsive**: Recruiters desktop-primary
7. **Plain loading states**: Real progress, contextual messages, no "AI thinking"
8. **Plain language errors**: No technical jargon, actionable recovery
