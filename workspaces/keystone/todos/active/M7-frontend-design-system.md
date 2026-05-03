# M7 — Frontend Design System

> Depends on: M0.3 (Next.js scaffold)
> Must be done before M8 and M9. Once this lands, frontend pages build on top of it.
> Implements: workspaces/keystone/01-analysis/26-design-system-recommendations.md (full)

---

## M7.1 — Tailwind config + CSS custom properties

**What**: All design tokens as Tailwind config extensions + CSS custom properties for dynamic theming (light/dark mode).

**Tailwind config additions** (`tailwind.config.ts`):
```typescript
theme: {
  extend: {
    colors: {
      // Brand primary (teal-blue)
      'brand': {
        50: '#EFF8FA', 100: '#D5ECF1', 300: '#7FC4D2',
        500: '#1E7A8C', 600: '#155E6E', 700: '#0F4751', 900: '#082C33'
      },
      // Match levels
      'match-strong':        '#1F8F5F',  // emerald
      'match-transferable':  '#C68A1A',  // amber
      'match-addressable':   '#D97338',  // orange
      'match-fundamental':   '#8B4A8B',  // plum (NOT red)
      // Match tints (background)
      'match-strong-tint':        '#E6F4EE',
      'match-transferable-tint':  '#FBF3DF',
      'match-addressable-tint':   '#FCEBDD',
      'match-fundamental-tint':   '#F2E6F2',
    },
    fontFamily: {
      sans: ['Inter Variable', 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', 'system-ui', 'sans-serif'],
      mono: ['JetBrains Mono', 'monospace'],
      display: ['Fraunces', 'Georgia', 'serif'],
    },
    transitionDuration: {
      'instant': '80ms', 'fast': '160ms', 'base': '240ms', 'slow': '360ms'
    }
  }
}
```

**`app/globals.css`**: CSS custom properties for all tokens in both light and dark mode.

**Dark mode variables** (per Analysis 26 §1.5):
- Page surface: `#FFFFFF` → `#0E1416`
- Card surface: `#FAFAF9` → `#161E21`
- Border: `#E7E5E1` → `#2A3438`
- Match-fundamental in dark: `#B57FB5` (lifted for contrast)
- Match-transferable in dark: `#E0AD52`

**Font loading** (Next.js `next/font`):
- Inter Variable (weight 400, 500, 600) — variable font, ~60KB
- Fraunces (weight 600) — display only, loaded only on marketing pages
- JetBrains Mono (weight 400) — loaded only on pages with code/mono text

**`tabular-nums` utility class**: `font-variant-numeric: tabular-nums` — used on all numeric dashboard displays.

**Acceptance criteria**:
- `brand-500` resolves to `#1E7A8C` in any Tailwind class
- `match-fundamental` resolves to `#8B4A8B`
- Dark mode: `class="dark"` on `<html>` switches all CSS vars
- All custom fonts load without FOUT (variable font swap strategy)
- Storybook shows all color tokens in a "Design Tokens" story

**Implements**: Analysis 26 §Part 1 (Color), §Part 2 (Typography)

---

## M7.2 — shadcn/ui + custom component library

**What**: Install shadcn/ui components needed by KeyStone, plus custom project-specific components.

**shadcn/ui components to install**:
`Card`, `Button`, `Badge`, `Dialog`, `Sheet`, `Sidebar`, `Input`, `Textarea`, `Select`, `Form`, `Label`, `Separator`, `Tooltip`, `DropdownMenu`, `Toast` (Sonner), `Avatar`, `Progress`, `Tabs`, `Table`, `Skeleton`

**Custom components** (project-specific, live in `components/keystone/`):

### `<MatchChip level={} />`
Four variants: strong, transferable, addressable, fundamental.
```tsx
// Renders: rounded-full px-2.5 py-0.5 text-xs font-medium
// with correct bg-tint + text-foreground + border
<MatchChip level="fundamental">Fundamental gap</MatchChip>
```
Used in: resume analysis, JD breakdown, dashboard, B2B views. Single source of truth for four-level color system.

### `<SuggestionCard suggestion={} onAccept onReject onModify />`
Three states: expanded (default), collapsed (post-decision), editing.
- Original text: JetBrains Mono 13px on `neutral-50` bg, inset padding
- Suggested rewrite: Inter 15px, `brand-primary-50` tint with 2px left border in `brand-primary-500`
- Rationale: Inter 14px, `neutral-600`
- Action buttons: `[✓ Accept]` `[✎ Edit]` `[✗ Skip]`
- Accept: card collapses with 160ms ease-out animation
- Edit: inline editor expands (suggestion text pre-filled as starting point)
- Skip: instant collapse, optional "Why?" follow-up chip row: `[Wrong tone] [Too generic] [Not relevant] [Just don't like it]`
- Keyboard: `A` accept, `E` edit, `X` skip

### `<DropZone onFile onText />`
Resume upload component. States: idle, dragging, uploading, success, error.
- Idle: dashed border, "Drop resume here — PDF or DOCX" + "Or paste text" link
- Success: show filename + page count + word count
- Error: silently transform to text-paste textarea ("We couldn't read this file. Paste the text directly.")
- No error state shown for parse failures — silent fallback per Analysis 26 §Voice and Tone

### `<JDInput onUrl onText />`
JD input component. Large (h-14), mono font for URL text, toggle switch between URL and text mode.
- URL mode: paste-optimized, shows preview of extracted company/role on success
- Text mode: textarea with "Paste job description" placeholder
- Toggle button: "Switch to text" / "Switch to URL"

### `<EmptyState icon title description action />`
Reusable empty state template. Single-color line illustration (brand-primary-300).
- NO mascot, NO emoji, NO "Nothing to see here"
- Forward-looking copy: "Your X will appear here once you Y"
- One concrete action button

### `<LoadingInsight />`
Rotating SG hiring insight shown during analysis wait (>10 seconds). Curated set of 30 short SG market observations. Updates every 5 seconds. Copy example: "GLC interviewers typically score on Leadership, Customer Focus, and Innovation — three distinct dimensions, not one."

**Acceptance criteria**:
- All custom components have Storybook stories with all states
- `<MatchChip level="fundamental">` renders plum (#8B4A8B) — NOT red
- `<SuggestionCard>` keyboard shortcuts work (A/E/X)
- `<DropZone>` silent-fallback: malformed PDF → text area appears, no error
- WCAG AA: all text/background pairs pass 4.5:1 contrast check

**Implements**: Analysis 26 §Part 3 (Components), workspaces/keystone/03-user-flows/04-ai-interaction-patterns.md

---

## M7.3 — Navigation shell

**What**: App shell with sidebar navigation (desktop) and bottom tab bar (mobile).

**Desktop sidebar** (shadcn Sidebar block):
```
[Logo] KeyStone
─────────────────
  Analyse a Job         (primary CTA — always first)
  My Resumes
  Applications
  Insights (Pro)
─────────────────
  [User avatar]
  [Free / Pro badge]
  [Upgrade →]          (free users only)
  Settings
```

**Mobile bottom tab bar** (4 tabs, always visible):
- Analyse (home/primary)
- Applications
- Insights
- Settings (profile)

**Mobile nav rules**:
- Tab bar minimum 56px height, 48px touch targets
- Active tab: brand-500 tint + filled icon
- Upgrade prompt: inline in Settings tab (NOT a separate forced modal on every page load)

**Plan indicator**: shown in sidebar bottom corner for desktop, in Settings tab header for mobile. "Free · 2 jobs analysed" or "Pro · Renews May 19."

**Acceptance criteria**:
- Desktop: sidebar shows correct nav items based on subscription tier
- Mobile: bottom tab bar visible on all app pages
- Mobile: no forced "use desktop" messaging
- Sidebar collapses to icon-only at <1024px viewport

**Implements**: Analysis 26 §3.5 (Navigation), Analysis 24 §Part 5 (Mobile vs Desktop)

---

## M7.4 — Copy deck + voice rules

**What**: Document and implement the voice and tone system. Code-level enforcement where possible.

**Deliverables**:
- `docs/copy/voice-and-tone.md`: per-persona copy variants, banned phrases, AI output style guard
- AI output post-processing utility: strips banned phrases from Claude outputs before display
  - Banned: "I'm an AI", "as an AI assistant", "I'd be happy to", "great question", "in conclusion", any emoji
  - If found: log warning (quality signal) + show suggestion without the offending phrase
- Per-persona copy variants implemented for onboarding + suggestion accepted copy:
  - Fresh grad: "Nice. 13 to go."
  - Mid-career: "Applied. Reframing this as transferable."
  - PMET: "Applied. This rewording reads like the senior leader you are."
- Persona detection: inferred from onboarding questionnaire answer ("what are you looking for?")

**Acceptance criteria**:
- Banned phrase filter catches all banned phrases in test set
- Persona-specific copy renders correctly for each persona type
- "Senior SG colleague" tone: no exclamation marks in body copy, no emojis in toasts

**Implements**: Analysis 26 §Part 4 (Voice and Tone), workspaces/keystone/03-user-flows/04-ai-interaction-patterns.md §AI Identity

