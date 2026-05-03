# Analysis 26 — Design System Recommendations

> Phase 01 Analysis — 2026-04-29
> Question: What design system makes KeyStone feel like "a senior SG colleague who happens to be AI" rather than "another generic resume tool"?
> Audience: design lead, frontend lead, founder for visual approval before /implement.

---

## Core Design Thesis

KeyStone's visual identity has to do three things at once:

1. **Earn trust in 5 seconds** — a fresh grad lands on the page from a Reddit link and decides if this looks legitimate before they read a word.
2. **Feel SG-native, not derivative** — not Silicon Valley pastel-purple AI-startup, not mainland-China gradient-heavy SaaS, not US-corporate navy-and-orange. It must look like it was built in Singapore, for Singapore, by someone who knows how the market reads professional polish.
3. **Make the AI feel like a coach, not a magician** — confident but specific, never theatrical. No sparkle icons. No "AI is thinking…" mystique. The product's claim is "we know SG hiring"; the design has to act like it knows.

The visual approach: **clean professional + warm intelligence**. Closer to Linear / Notion / Stripe Press than to Jasper / Copy.ai / Rytr. No marketing-AI tropes.

---

## Part 1 — Color System

### 1.1 Brand Primary

**Choice: Teal-leaning blue** (not the default SaaS navy, not generic indigo, not "AI purple").

| Token | Hex | Tailwind | Usage |
|---|---|---|---|
| `brand-primary-50` | `#EFF8FA` | `sky-50`-adjacent | Surface tint, muted hover |
| `brand-primary-100` | `#D5ECF1` | — | Subtle backgrounds, badges |
| `brand-primary-300` | `#7FC4D2` | — | Decorative, illustrations |
| `brand-primary-500` | `#1E7A8C` | — | **Primary CTAs, brand mark** |
| `brand-primary-600` | `#155E6E` | — | CTA hover, active links |
| `brand-primary-700` | `#0F4751` | — | Pressed state, dark headlines |
| `brand-primary-900` | `#082C33` | — | Footer, dark-mode surface |

**Why teal-blue rather than pure navy or indigo**:
- Navy reads "bank corporate" — fine for trust, but signals slow/heavy. KeyStone is a fast tool; navy works against the speed claim.
- Indigo (the default Tailwind/shadcn brand) reads "generic SaaS startup" — every YC-deck product looks the same in that color, and SG buyers (especially university procurement) have seen it 200 times.
- Teal-blue carries professional trust + a hint of warmth and freshness; reads "modern SG public sector aesthetic" without being literally government-blue (avoid the SingPass red, the GovTech orange, the NLB green — those are owned).
- Differentiates from competitors: Jobscan uses orange-on-white, Teal uses literal teal-green (`#0DCEAA`-like) which we should NOT mimic to avoid name+color collision, VMock uses corporate blue + red.

**Brand mark**: a stylized keystone arch (the load-bearing wedge in an arch — the literal product metaphor) in `brand-primary-500` on white, or white reversed on `brand-primary-700`.

### 1.2 Neutral Scale (Foundation)

Use a slightly warm gray, not pure cool gray. Warm grays read as "professional document" (resume context); cool grays read as "developer dashboard."

| Token | Hex | Usage |
|---|---|---|
| `neutral-0` | `#FFFFFF` | Page background (light mode) |
| `neutral-50` | `#FAFAF9` | Card surface, hover background |
| `neutral-100` | `#F4F3F1` | Subtle dividers, disabled backgrounds |
| `neutral-200` | `#E7E5E1` | Borders, inactive elements |
| `neutral-300` | `#D0CDC7` | Strong borders, placeholder text |
| `neutral-500` | `#78756E` | Secondary text, captions |
| `neutral-700` | `#3F3D38` | Body text |
| `neutral-900` | `#1A1916` | Headlines, primary text |

Tailwind: closest match is `stone-*` scale. Specify `stone-*` in Tailwind config rather than `gray-*` or `slate-*`.

### 1.3 The Four-Level Match Color System (The Hardest Color Problem)

This is the most important color decision in the product. Most tools use traffic-light reds/yellows/greens, which (a) feel like a school grade ("you got a D"), (b) make Fundamental gaps feel punitive. KeyStone has to make Fundamental Gap feel like **honest information** — not "you failed."

**Design principle**: Strong → Transferable → Addressable → Fundamental is a **continuum of effort required**, not a continuum of pass/fail. The color system must communicate "this is how much work it takes to close" not "this is good/bad."

| Level | Token | Hex | Tailwind nearest | Background tint | Communicates |
|---|---|---|---|---|---|
| Strong match | `match-strong` | `#1F8F5F` | `emerald-600` | `#E6F4EE` | "You have this — let's make it visible" |
| Transferable | `match-transferable` | `#C68A1A` | `amber-600` | `#FBF3DF` | "You have it adjacent — connect the dots" |
| Addressable | `match-addressable` | `#D97338` | `orange-600` | `#FCEBDD` | "You can claim this with reframing" |
| Fundamental | `match-fundamental` | `#8B4A8B` | custom plum | `#F2E6F2` | "You don't have this — that's fine, we'll flag it" |

**Critical decision: Fundamental gap is PLUM, NOT RED.**

Why this matters:
- Red on Fundamental triggers a "rejection" emotional response. Mid-career switchers and PMET users (the highest-WTP segments) are emotionally raw — a red banner saying "FUNDAMENTAL GAP" reads as "you don't qualify, give up."
- Plum/muted-purple is unusual enough to read as **a category, not an alarm**. It says "this is information, not a verdict."
- The actual product behavior reinforces this: Fundamental gaps are flagged, not "fixed" — the tone of the color must match the tone of the message ("here's something to know about, separate from what we're improving").
- Red is reserved for **system errors and destructive actions** (delete account, payment failed). Mixing red for "your skill gap" with red for "your payment was declined" overloads the signal.

Visual treatment: each match level uses the foreground hex on the tint background. Borders use the foreground at 30% opacity. Icons (a small chevron or dot) use the foreground.

```
Strong       ●  Project management — Strong match
              "Led 3 cross-functional teams" demonstrates this clearly.

Transferable ●  Stakeholder communication — Transferable
              You've done this in finance reporting; reframe for marketing context.

Addressable  ●  Data analysis tooling — Addressable gap
              You've used Excel pivots; we'll reposition this as analytical tooling.

Fundamental  ●  5+ years SaaS product experience — Fundamental gap
              You don't have direct SaaS experience. We won't fabricate this; we'll flag it transparently.
```

### 1.4 Feedback / Status Colors

| Token | Hex | Purpose |
|---|---|---|
| `feedback-success` | `#1F8F5F` | Suggestion accepted, payment succeeded, application logged |
| `feedback-info` | `#1E7A8C` (= brand) | Neutral info, hints, "we're loading" |
| `feedback-warning` | `#C68A1A` | Soft warning ("your free quota is running low") |
| `feedback-destructive` | `#B43D3D` | **Destructive only** — delete account, payment failure, account locked. NEVER for skill gaps or AI feedback. |

Note `feedback-success` deliberately matches `match-strong`, and `feedback-warning` matches `match-transferable`. This is intentional: when the user accepts a suggestion (success), the affirmation color is the same as their "you have this skill" color — visual coherence reinforces "you're getting better."

### 1.5 Dark Mode

SG tech workers expect dark mode. PMET users mostly do not. Build it; default to light; remember the preference. Founder note: dark mode is not optional polish — Reddit/forum-acquired users will judge a 2026 SaaS without dark mode as unserious.

| Token | Light | Dark |
|---|---|---|
| Page surface | `neutral-0` `#FFFFFF` | `#0E1416` (warm-tinted near-black, not pure black) |
| Card surface | `neutral-50` `#FAFAF9` | `#161E21` |
| Border | `neutral-200` `#E7E5E1` | `#2A3438` |
| Body text | `neutral-700` `#3F3D38` | `#D8D6D1` |
| Headlines | `neutral-900` `#1A1916` | `#F4F3F1` |
| Brand primary | `brand-primary-500` | `brand-primary-300` (lifted for contrast) |

Match-level colors in dark mode: keep the same hue, lift saturation/lightness so they pass WCAG AA against the dark surface. Plum becomes `#B57FB5`, amber `#E0AD52`.

### 1.6 Accessibility Floor

Every text/background pair MUST hit WCAG AA (4.5:1 for body, 3:1 for large text). Match-level color + tint pairs all clear AA when the foreground is the chip text color and the background is the tint. `match-fundamental` plum is the tightest pair — verified at 4.6:1.

---

## Part 2 — Typography

### 2.1 Typeface Choices

**Primary (UI + body): Inter Variable.**
- The de facto SG/global SaaS body font. Reads professional, screens cleanly, has a wide weight range.
- Free, self-hostable, has CJK fallback chains.
- Already shipped in shadcn/ui defaults — zero integration cost.

**Display (hero headlines, marketing only): Fraunces or Instrument Serif** (pick one, do not mix).
- A serif display face on the marketing pages (landing, pricing, university B2B page) signals "considered, professional, written by a human" — differentiates from the all-Inter sea of generic SaaS landing pages.
- Inside the product itself: NO display serif. Stay in Inter to keep the working surface utilitarian.
- Recommendation: **Fraunces** — more character, better weight range; Instrument Serif is more austere and harder to use across sizes.

**Monospace (code-ish, technical surfaces): JetBrains Mono.**
- Used for: showing parsed JD content with highlights, "raw" resume text view, ID strings in B2B admin views.
- Not for body. Just for the moments where "this is the literal text from your input."

**CJK fallback chain** (for Chinese characters in user resume content — names, company names, education):
```css
font-family:
  "Inter Variable",
  "PingFang SC",      /* macOS / iOS Simplified */
  "Microsoft YaHei",  /* Windows */
  "Noto Sans SC",     /* Web fallback */
  system-ui, sans-serif;
```
This handles 张伟 / 新加坡国立大学 / 中国银行新加坡分行 cleanly without needing to ship a separate CJK font file.

### 2.2 Hierarchy and Scale

A 6-step type scale, all from Inter except where noted. Use Tailwind's default size tokens with explicit line-heights — avoid the trap of letting line-height scale linearly.

| Role | Size | Line height | Weight | Tailwind class | Usage |
|---|---|---|---|---|---|
| Display 1 | 56 / 60 | 1.05 | 600 | `text-6xl leading-tight font-semibold` | Landing hero (Fraunces, optional) |
| Display 2 | 40 / 44 | 1.1 | 600 | `text-4xl leading-tight font-semibold` | Section heroes |
| H1 | 30 / 36 | 1.2 | 600 | `text-3xl font-semibold` | Page title |
| H2 | 24 / 32 | 1.3 | 600 | `text-2xl font-semibold` | Section heading |
| H3 | 18 / 26 | 1.35 | 600 | `text-lg font-semibold` | Card title, suggestion title |
| Body | 15 / 24 | 1.6 | 400 | `text-[15px] leading-6` | **Body default — do NOT use 16px** |
| Body emphasis | 15 / 24 | 1.6 | 500 | `text-[15px] font-medium` | Bullet, label |
| Caption | 13 / 20 | 1.55 | 400 | `text-[13px] leading-5 text-stone-500` | Metadata, timestamps |
| Microcopy | 12 / 18 | 1.5 | 500 | `text-xs font-medium text-stone-500 tracking-wide uppercase` | Eyebrows, badge labels |

**Why 15px body, not 16px**: 16 is the web default and looks "blog-like" — fine for marketing pages, too loose for a working tool with dense suggestion content. 15 is the SaaS productivity-app standard (Linear, Notion, Vercel dashboard) and gets you ~10% more content per screen without losing readability. Use 16 only on the marketing landing page where reading rhythm matters.

**Resume content special case**: when displaying the user's actual resume text (the "before" side of a suggestion card), render at 14px in Inter with `tracking-normal` — slightly tighter than UI body — to evoke "this is a document, not chrome."

### 2.3 Numerals

Use Inter's tabular figures (`font-feature-settings: 'tnum'`) for **all numbers in dashboards and suggestion counters** (response rate, application count, suggestion N of M). Variable-width digits jitter when counters update; tabular digits hold their column.

```css
.tabular-nums { font-variant-numeric: tabular-nums; }
```

---

## Part 3 — Component Library (shadcn/ui + Tailwind)

shadcn/ui is the right base. The components below are the high-leverage ones — get these right, the rest follows.

### 3.1 The Suggestion Card (Core Component)

This is the most important component in the product. Three states (collapsed, expanded, post-decision), one container.

**Anatomy** (use shadcn `Card` + custom internals):

```
┌─────────────────────────────────────────────────────────────────┐
│  ●  Bullet from Work Experience · Suggestion 2 of 14            │ ← header
│  ─────────────────────────────────────────────────────────────  │
│                                                                 │
│  ORIGINAL                                                       │ ← eyebrow
│  Responsible for managing a team                                │ ← original (mono)
│                                                                 │
│  ↓                                                              │
│                                                                 │
│  SUGGESTED REWRITE                                              │
│  Led an 8-person cross-functional team across 3 business units, │ ← rewrite (Inter)
│  improving reporting efficiency by 30%                          │
│                                                                 │
│  WHY                                                            │
│  This GLC weights quantified team leadership; your phrasing     │ ← rationale
│  undersells scale. Singapore GLCs read "responsible for" as     │
│  ambiguous ownership.                                           │
│                                                                 │
│  Tags: Leadership · Quantified outcome · GLC convention         │ ← chips
│                                                                 │
│  [ ✓ Accept ]   [ ✎ Edit ]   [ ✗ Skip ]                         │ ← actions
└─────────────────────────────────────────────────────────────────┘
```

**Components used**:
- shadcn `Card`, `Badge` (chips), `Button` (variants: default, outline, ghost), `Tooltip` (rationale expansion if truncated), `DropdownMenu` (the "More — report bad suggestion / explain more" affordance).
- Custom: a small DiffViewer for the inline edit state (do NOT use a generic textarea — show the suggestion as the starting point with diff highlights as the user edits).

**Visual rules**:
- Original text in JetBrains Mono 13px on `neutral-50`, no border, just inset padding.
- Rewrite in Inter 15px, foreground `neutral-900`, background `brand-primary-50` tint with a 2px left border in `brand-primary-500`. This is the "AI's contribution" color flag.
- Rationale in Inter 14px, `neutral-600`, no background (tertiary).
- Tags use `Badge` variant `outline` with the appropriate match-level color when the tag references a level.

**Interaction**:
- Accept: card animates collapsed (200ms), shows a small green ✓ inline, marks the bullet as "applied" in the parent resume view. Toast: "Applied. 13 suggestions remaining."
- Edit: card expands to inline editor with the suggested text pre-filled. User edits; on save, treated as a Modify event (logged separately for the learning loop).
- Skip: card collapses immediately, no animation flourish (skipping should feel friction-free). Logged as Reject. Optional one-tap "Why?" follow-up: [Wrong tone] [Too generic] [Not relevant] [Just don't like it] — captures the rejection signal that powers the learning loop.

**Accessibility**:
- Each card is a `<section>` with `aria-labelledby` pointing to the H3 title.
- Action buttons have descriptive `aria-label`s ("Accept suggestion 2 of 14: Led an 8-person…").
- Keyboard: `J` next, `K` previous, `A` accept, `E` edit, `X` skip — power-user keys for users running through 30 suggestions.

### 3.2 Match-Level Chip / Pill

The four-level taxonomy needs a single, instantly-recognizable chip. Consistency across resume analysis, JD breakdown, dashboard, B2B aggregate views.

```tsx
<MatchChip level="strong">Strong match</MatchChip>
// renders: rounded-full px-2.5 py-0.5 text-xs font-medium
//         bg-emerald-50 text-emerald-700 border border-emerald-200
```

Variants for all four levels. Component is shadcn `Badge` with custom variant prop. Same chip used in:
- Resume analysis page (per-bullet level indicator)
- JD breakdown ("matches 8 strong, 4 transferable, 3 addressable, 2 fundamental")
- Dashboard analytics ("your applications by match level")
- B2B cohort page ("most common Fundamental gaps in your cohort")

### 3.3 Empty States

Empty states are where most SaaS products lose users. KeyStone has empty states everywhere: no applications logged yet, no suggestions accepted yet, no second JD analyzed yet, no Pro subscription yet.

**Empty-state pattern** (shadcn `Card` + `Button` + custom illustration):

```
        [ small custom line illustration — about 96px ]
                  (NO mascot. NO emoji. NO 3D render.)
                  (a single-color line drawing — file folder, paper, pen)

                  No applications logged yet

      KeyStone tracks your applications so you can see what's working.
       Every time you download a tailored resume, we'll ask if you're
                       submitting it to that company.

                       [ Analyse a job →  ]
```

Tone: encouraging, specific, action-oriented. NEVER:
- "Nothing to see here" (dismissive)
- "Looks like you haven't done X" (slightly accusatory)
- A sad-mascot illustration (childish for a professional tool)

DO:
- "Your X will appear here once you Y" (forward-looking)
- One concrete next action.
- Illustration: spot illustrations only, single-line, 1-color (`brand-primary-300`). Recommend procuring or commissioning a small set (8–10) rather than using emoji or stock.

### 3.4 Form Inputs (Onboarding, Edit States)

shadcn `Input`, `Textarea`, `Select`, `Form`. Two project-specific patterns:

**JD URL input** — needs a custom variant: large height (h-14), mono font for the URL text once pasted, a subtle "Paste URL or drop in JD text" placeholder, and a built-in switch icon to toggle to text-paste mode. This is the highest-friction input in the entire product; design it like Stripe's payment input — confidence-inspiring, instantly responsive on paste.

**Resume drop zone** — full-width drop zone with a clear file-format hint, max-size hint, and an instant preview of the parsed content (file name + page count + word count) on success. On parse failure, the zone smoothly transforms into a textarea labelled "Paste your resume text here" — NO error state shown unless the user explicitly retries the upload. Per Analysis 21: "if URL parse fails, silently offer text-paste fallback (no error state shown)" applies equally to resume parsing.

### 3.5 Navigation

**App shell**: Sidebar nav (shadcn `Sidebar` block — appears in shadcn/ui blocks).
- Logo top-left
- Nav items: Analyse a Job, My Resumes, Applications, Insights (Pro), Settings
- Bottom: account chip, plan indicator (Free / Pro), upgrade affordance if Free
- Collapsible to icon-only on smaller widths

**Mobile**: bottom tab bar with the three primary surfaces (Analyse, Applications, Insights). The brief notes "most SG users check on mobile first, even if they apply on desktop" — so the mobile experience can't be a diminished version. It's the entry point.

### 3.6 Toast / Notification

shadcn `Sonner`. Specific tone rules:
- Success: short, confident — "Suggestion applied." not "Great! Your suggestion has been successfully applied!"
- Info: actionable — "5 applications pending. Update in 30 seconds →" with a click target.
- No emoji in toasts. Ever. This is a professional tool.

### 3.7 Modal / Dialog (Paywall, Important Decisions)

shadcn `Dialog`. The paywall dialog is the most important modal in the product — see Analysis 27 (VP coherence) for placement, but the design rules:

- Title in H2 (Inter 600), not display serif (the paywall is functional, not marketing).
- Single primary CTA, single secondary action.
- Price stated clearly in the body (SGD 19/mo or SGD 180/yr) with tax-clarity microcopy.
- NO countdown timer. NO "limited offer." NO scarcity manipulation. SG buyers (especially PMET) read those as scammy and lose trust instantly.

### 3.8 Data Display (Dashboards, B2B Cohort Views)

**Charts**: Recharts or Tremor (both compose well with shadcn). Use sparingly. Specific rules:
- Line charts for trends (response rate over time): single line, brand-primary, no gridlines, only Y-axis labels at min/max/current.
- Bar charts for distributions (applications by match level): use the four match-level colors — visual coherence with the rest of the product.
- NEVER pie charts. They are unreadable at SG dashboard sizes and look amateur to a procurement reviewer.

**Tables** (B2B admin, application lists): shadcn `Table`. Tabular-nums on every numeric column. Sortable headers. Sticky header on scroll. Empty state per § 3.3.

---

## Part 4 — Voice and Tone

The voice doctrine: **"Senior SG colleague who has seen 5,000 resumes and tells you the truth quickly."** Not a friend. Not a coach with a clipboard. Not a chatbot. A peer with informed opinions.

### 4.1 Voice Pillars

| Pillar | Means | Looks like | Does not look like |
|---|---|---|---|
| **Specific** | Cites the JD, the company type, the bullet | "This GLC values quantified leadership; your bullet says 'responsible for' which reads ambiguous in SG public sector context." | "Your bullet could be stronger. Consider adding metrics." |
| **Direct** | No softeners or hedges around the actual recommendation | "You don't have 5 years SaaS experience. We're flagging this honestly rather than rewriting around it." | "It seems like you might possibly want to perhaps consider that you may not fully meet…" |
| **Calm** | Does not perform excitement or surprise | "Suggestion applied. 13 to go." | "🎉 Awesome! Great choice! You're crushing it!" |
| **Useful** | Every sentence carries information | "Phone screening for GLC roles usually opens with a competency framework question — Leadership or Customer Focus. Your story bank has two relevant entries." | "Get ready to nail your interview!" |
| **SG-aware** | References real SG context where relevant | "MNCs in Singapore — especially regional HQs — read 'NS' as 'two-year leadership crash course' if you frame it that way." | "Your military service can be valuable in business contexts." |

### 4.2 Per-Persona Tonal Variations

The brief calls out per-persona tone variation. Implement as **subtle copy variants in the activation flow and onboarding**, not a settings toggle. Persona is inferred from the questionnaire ("what are you looking for?") at signup.

**Fresh grad** (energetic but not childish):
- Onboarding: "First job hunt is a numbers game — let's make every application count."
- Empty state: "You've got time and energy. Let's spend it on jobs you actually want."
- Suggestion accepted: "Nice. 13 to go."

**Mid-career switcher** (peer-level, respectful of experience):
- Onboarding: "Your experience is real — the question is how to position it for a different industry. Let's start there."
- Empty state: "Switching industries is mostly a translation problem. We'll handle the translation."
- Suggestion accepted: "Applied. Reframing this as transferable rather than rewriting it."

**PMET** (empowering, never pitying — this is the most sensitive persona):
- Onboarding: "You've built deep expertise. The market reads resumes differently than it did when you last looked. Let's bridge that gap."
- Empty state: "Your next role is out there. Let's get your resume in front of it."
- Suggestion accepted: "Applied. This rewording reads like the senior leader you are."

**Universal rule**: NEVER reference age, retrenchment, NS, or industry-departure in any negative framing. The tonal target for PMET is "this product respects you" — every line has to clear that bar.

### 4.3 Error and Failure States

Never blame the user. Never expose internals. Always offer the next action.

| Bad | Good |
|---|---|
| "URL parse failed." | "We couldn't read this job posting. Paste the text here instead — works just as well." |
| "Resume too large (max 5MB)." | "This file is over 5MB. Try exporting from Word as PDF, or paste the text directly." |
| "Payment failed: card_declined." | "Your bank declined this card. Try another card, or contact your bank." |
| "An error occurred." | "Something went wrong on our end. Try again, or [contact us](mailto:hello@keystone.sg)." |
| "Login required." | "Sign in to save your work." (with a "Why?" link explaining the trial state) |

### 4.4 AI-Generated Content Rules

The AI writes the suggestions. The AI does NOT write rationales in flowery first-person. Constrain the output:
- Rationale: 1 sentence, max 25 words, references the JD requirement OR the company-type convention.
- Tone: confident assertion, not "I think" or "we recommend."
- Banned phrases (block at LLM-prompt level): "I'm an AI", "as an AI assistant", "I'd be happy to", "great question", "it's important to note", "in conclusion", any emoji, any em-dash flourishes that pretend to be human.

The voice rule for AI output is the same as human-written copy: a senior SG colleague would not write "I'd be happy to suggest…" — they'd say what they think.

### 4.5 Microcopy Patterns

**Buttons**: verb-led, 1-3 words. "Analyse a job" not "Get started." "Apply suggestion" not "OK." "Skip this one" not "Skip."

**Tooltips**: full sentences with periods, ≤14 words. "We mark this as 'transferable' when your experience adjacent but not direct."

**Form labels**: short and concrete. "Resume (PDF or DOCX)" not "Please upload your CV file."

**Confirmation modals**: state the consequence clearly. "Delete this resume? This won't affect applications you've already submitted." not "Are you sure?"

---

## Part 5 — Motion and Interaction

Motion should feel **fast and inevitable**, not playful. Frame budget: 60fps on a mid-range Android (the SG mobile reality).

### 5.1 Timing Tokens

| Token | Duration | Easing | Usage |
|---|---|---|---|
| `motion-instant` | 80ms | linear | Hover state, focus ring |
| `motion-fast` | 160ms | ease-out | Toast appearance, suggestion-accept collapse |
| `motion-base` | 240ms | ease-out | Modal open, tab switch |
| `motion-slow` | 360ms | spring(stiffness=180, damping=22) | Dashboard chart enter, page transition |

Never longer than 360ms. Resume tailoring is an efficiency tool; long animations make it feel slow.

### 5.2 Loading States — Critical for the Activation Flow

Per Analysis 21, the analysis-wait stage (1:30 — 2:30 in the activation flow) is where most users drop off. Design implications:

- **<10s wait**: skeleton state of the suggestion card (shimmer at low contrast, NOT a spinner). Users perceive content "loading in" rather than "system thinking."
- **10-30s wait**: progressive disclosure — show "✓ Parsed JD" then "✓ Identified GLC employer type" then "⟳ Generating suggestions" with a single SG market insight as a sidebar (per Analysis 21). The sidebar insight rotates through a curated set of 30 short SG hiring observations — provides genuine value during the wait.
- **>30s wait**: surface partial results immediately. Show resume analysis (which finished first) while suggestions stream in. Streaming generation > batched generation for perceived speed.
- **Never** show a percentage progress bar unless it's accurate. A fake progress bar destroys trust the moment it stalls.

---

## Part 6 — Iconography

shadcn defaults to Lucide. Stay there. Specific rules:

- 16px in chips, 20px in buttons, 24px in nav, 32px in feature cards, 96px max in empty states.
- Stroke width: 1.5 (Lucide default). Do not mix stroke weights.
- Color: inherit from text by default; only the brand mark and match-level dot use color. Avoid colored icons in body content — they create visual noise that competes with the match-level system.

NEVER use:
- Emoji as icons
- Filled glyphs mixed with outlined glyphs (Lucide is all outlined)
- "AI sparkle" iconography (✨, 🪄, 🤖) — undermines the "senior colleague" voice
- Animated icons except in the global loading state

---

## Part 7 — Implementation Notes for /implement

When the design system reaches `/implement`, the deliverables should be:

1. **Tailwind config** with all color tokens, the type scale, the motion tokens.
2. **shadcn/ui base install** + the project-specific component variants (`MatchChip`, `SuggestionCard`, `DropZone`, `JDInput`, `EmptyState`).
3. **A single `app/globals.css`** holding the CSS variables for the color tokens (light + dark mode).
4. **A Storybook (or Ladle, lighter) instance** per component for the founder + design partner review cycle. Worth the day of setup; saves weeks of "wait does it look right" arguments.
5. **A copy-deck file** (`docs/copy/voice-and-tone.md` or equivalent) with the per-persona variants, the banned-phrase list, and the AI-output style guard.

DO NOT:
- Build a custom component library from scratch.
- Use a UI kit other than shadcn (Mantine, MUI, Chakra) — they don't compose well with the Tailwind-first approach already chosen, and switching costs a week minimum.
- Skip the motion tokens — defining them upfront prevents 50 ad-hoc `transition-all duration-200` everywhere that age into inconsistency.

---

## Summary

The design system in three principles:

1. **Trust through restraint.** No mascots, no sparkles, no theatrical AI flourish. The product earns trust by being the calm professional in a market full of loud generic SaaS.
2. **The four-level color system carries the value prop.** Get plum-not-red right and Fundamental Gap stops feeling punitive — which is the difference between users completing the flow and users closing the tab.
3. **Voice is a feature, not a polish item.** "Senior SG colleague" is the pitch; if the UI copy reads "I'd be happy to help!" the pitch dies on contact. Ship the voice rules with the components.
