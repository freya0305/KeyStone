# UX Audit: KeyStone Landing Page + Role Selection Flow

## Audit Summary

| Dimension | Verdict | Severity |
|---|---|---|
| Visual Hierarchy | MARGINAL | P2 |
| Role Selection UX | MARGINAL | P2 |
| Pricing Section | PASS | P3 |
| Mobile-First | PASS | P3 |
| Information Architecture | MARGINAL | P2 |
| Interaction Details | FAIL | P1 |
| Design System Alignment | FAIL | P1 |
| Accessibility | FAIL | P1 |

---

## 1. Visual Hierarchy

**Verdict: MARGINAL (P2)**

### Finding 1: Hero CTA is clear but the role toggle creates a confusing two-action first impression

**Mockup lines 67-74** -- Two equal-weight buttons ("求职者入口" / "招聘者入口") share the hero section with the badge headline. Both are styled identically (same size, same weight, equal visual prominence). A user arriving for the first time sees two primary actions with no clear first step.

**Spec M8.1** says the hero CTA should be a single action: `[Try it on one job -- free]` with a sub-CTA `[See how it works]`. The role split is not part of the hero CTA in the spec.

**Recommendation**: Make the Job Seeker path primary (full indigo fill) and the Recruiter path secondary (outlined). The current mockup uses `border-2 border-gray-200` for both, making them appear equal. Alternatively, show only the Job Seeker CTA in the hero and surface the Recruiter path below the fold.

### Finding 2: Role cards below the hero duplicate the hero role buttons

**Mockup lines 86-140** -- The role selection cards are a second occurrence of the same choice the user just made in the hero. The user who clicked "求职者入口" now sees the same "求职者" card again. This creates a double-take moment: "did my click work? Why am I being asked again?"

**Mockup JS lines 736-748** -- `selectRole()` is called from both the hero buttons AND the role cards. The card selection is redundant for users who entered through the hero.

**Recommendation**: Remove the role cards section entirely, or convert it to a "Learn more about each path" expandable section. The hero-to-app-shell transition already handles role selection.

### Finding 3: Features section has no visual anchor directing users downward

**Mockup lines 144-175** -- Three equal-weight feature cards in a row. No connecting line, no numbering, no directional cue. The user reads three items and has no signal about sequence or priority.

**Recommendation**: Add a step number (01 / 02 / 03) above each feature, or a connecting line, to visually encode the "how it works" sequence that M8.1 specifies should exist.

---

## 2. Role Selection UX

**Verdict: MARGINAL (P2)**

### Finding 4: Role selection is a single binary toggle with no meaningful downstream difference in the mockup

**Mockup line 19** -- `let currentRole = null` -- the role only affects the app shell's nav tabs and content. The landing page itself does not change based on role. A user who selects "Recruiter" still sees the same features section, same pricing section, same footer. The role choice only matters after entering the app shell.

**Spec M8.1** specifies different paths for job seeker vs recruiter, but does not require the landing page to差异化. However, the role badge color change (indigo for seeker, amber for recruiter in **mockup lines 737-738, 743-744**) is the only visual differentiation.

**Assessment**: The UX is understandable but shallow. The role selection feels performative because it does not change the landing page experience. This is a P3 concern rather than P2 -- the architecture is sound, only the depth of differentiation is weak.

### Finding 5: "Watch Demo" CTA has no destination

**Mockup line 76** -- `<button onclick="selectRole('seeker')">` shows "Watch Demo" as a secondary CTA but it routes to `selectRole('seeker')`, not to a demo video or walkthrough. **Implementation line 76-80** has a similar "Watch Demo" button pointing to `/demo`.

**Spec M8.1** does not specify a demo video. However, a "Watch Demo" label without a demo is misleading. Users who click it expecting a video will be confused.

**Recommendation**: Either remove the "Watch Demo" label or implement the demo destination. If no demo exists yet, rename to "See Example Analysis" and show a sample analysis inline.

---

## 3. Pricing Section

**Verdict: PASS (P3)**

### Finding 6: Pro tier differentiation is correct

Both **mockup lines 206-235** and **implementation lines 213-241** correctly differentiate Pro with:
- indigo border (2px solid #6366f1)
- "Most Popular" badge in top-right corner
- Indigo CTA button (vs gray outlined for Free and Team)

This matches M8.1's requirement for clear Pro differentiation.

### Finding 7: CTA hierarchy is correct

| Tier | CTA Label (Mockup) | CTA Label (Implementation) | Style |
|---|---|---|---|
| Free | 免费开始 | Get Started Free | Gray outlined |
| Pro | 升级到专业版 | Upgrade to Pro | Indigo filled |
| Team | 联系销售 | Contact Sales | Gray outlined |

The Free CTA says "Get Started Free" not "Upgrade" -- correct for a free tier. The Pro CTA says "Upgrade" -- correct for a tier above free.

**Minor**: The mockup uses Chinese CTAs and the implementation uses English. This is an internationalization inconsistency that should be resolved when i18n is implemented.

### Finding 8: Feature lists are scannable

Both mockup and implementation use `flex items-center gap-3` with green check icons. The text is a single line per item, which is correct for scannability. Font size is `text-sm` which is appropriate.

---

## 4. Mobile-First

**Verdict: PASS (P3)**

### Finding 9: Responsive grid breakpoints are correct

**Implementation line 88** -- `grid md:grid-cols-2` for role cards; **line 151** -- `grid md:grid-cols-3` for features. These match the single-column-on-mobile expectation.

### Finding 10: Touch targets are adequate

- Hero buttons: `px-8 py-4` -- 32px vertical padding meets the 44px minimum touch target guideline when combined with the horizontal padding.
- Role cards: `rounded-2xl p-8` -- full card is a touch target, adequate.
- Nav links in mockup: `px-3 py-2` -- acceptable for a nav item.

### Finding 11: Fixed nav on mobile

**Mockup line 24** -- `fixed top-0` nav with `z-50`. On mobile, this will overlap content scrolled beneath it. There is no `padding-top` adjustment on the body or main content to account for the fixed nav height (56px / h-14).

**Implementation line 24** -- same issue. The hero section starts at `pt-32` (128px), which appears to account for the nav, but this should be verified at 375px viewport.

---

## 5. Information Architecture

**Verdict: MARGINAL (P2)**

### Finding 12: Landing to App transition is one-way with no breadcrumb

**Mockup lines 721-730** -- `showApp()` hides the landing page and shows the app shell. There is no "back to landing" mechanism except the "退出" (exit) button in the app shell nav (**mockup line 329**). This is functional but abrupt.

**Spec M8.1** says "Gate-free CTA -- user enters the product from here without signing up." The current flow satisfies this. However, a user who enters the recruiter path and then wants to switch to the job seeker path must exit entirely and re-enter.

**Recommendation**: Add a role switcher in the app shell nav (e.g., a pill toggle "Job Seeker | Recruiter") that lets users switch paths without exiting.

### Finding 13: Missing sections from M8.1

The following M8.1-specified sections are absent from both mockup and implementation:
- **Social proof strip** (M8.1 section 2) -- "3 one-line quotes from design partners"
- **"How it works" 3-step section** (M8.1 section 3) -- "Paste your resume + a job link (30s) -- See where you match (10s) -- Review specific rewrites (60s)"
- **Singapore-specific section** (M8.1 section 4) -- "Built for how Singapore companies actually hire" with NRIC advice, NS framing, GLC vs MNC conventions
- **"Try it on one job -- free" CTA** pointing to `/analyse` without sign-up (M8.1 section 1)

These are substantial content gaps, not cosmetic ones. The landing page is missing its core value proposition sections.

---

## 6. Interaction Details

**Verdict: FAIL (P1)**

### Finding 14: Role switching in the mockup has no visible feedback

**Mockup line 67** -- The hero role buttons call `selectRole('seeker')` and `selectRole('recruiter')`. These update `currentRole` and call `showApp()`. There is no transition animation, no loading state, no confirmation that the selection was received. The screen abruptly switches to the app shell.

**Mockup lines 68-74** -- The "Watch Demo" button also calls `selectRole('seeker')`, meaning it enters the app shell with the seeker role, not a demo. This conflates two distinct actions.

### Finding 15: Navigation tab active state is unclear

**Mockup lines 751-757** -- Tab active state is set via a CSS class `active` added to `.tab-link`. The CSS rule (**mockup line 23**) sets `text-indigo-600 bg-indigo-50`. However, on the initial load of the app shell (after role selection), the dashboard tab should be active by default -- this is handled correctly in `renderNav` which defaults to `'dashboard'`. The issue is that when navigating between tabs, the previous active tab's visual state is not explicitly cleared before setting the new one.

**Implementation** -- There is no app shell implementation to audit. The landing page alone has no tab navigation.

### Finding 16: Toast notifications are functional but basic

**Mockup lines 868-874** -- The toast shows for 3 seconds with a slide-up animation. The message is passed as a string. This is adequate but has issues:
- No icon indicating toast type (success vs error vs info)
- No dismiss button
- No action button
- The toast uses `fixed bottom-4 right-4` which on mobile may overlap with the bottom tab bar if a tab bar is implemented later

### Finding 17: No loading states on async actions

**Mockup lines 795-809** -- The `analyzeJob()` function shows a spinner on the button during the 2-second simulated analysis. This is present. However, the JD Generator (**mockup lines 838-851**) and invite link generation (**mockup lines 853-860**) show no loading state -- the results appear instantly without any spinner or disabled state on the button.

**Recommendation**: Add `disabled` state + spinner to all form submission buttons.

---

## 7. Design System Alignment

**Verdict: FAIL (P1)**

### Finding 18: Brand colors are not implemented

**Spec M7.1** specifies brand colors as teal-blue:
```
brand-50: '#EFF8FA'  brand-100: '#D5ECF1'  brand-300: '#7FC4D2'
brand-500: '#1E7A8C'  brand-600: '#155E6E'  brand-700: '#0F4751'  brand-900: '#082C33'
```

**Mockup and implementation** use indigo/purple gradients throughout:
- Logo gradient: `from-indigo-600 to-purple-600` (mockup line 28, implementation line 28)
- Hero gradient text: `from-indigo-600 via-purple-600 to-pink-500` (implementation line 61)
- CTA buttons: `bg-indigo-600` (pervasive)

The spec's brand teal-blue (`#1E7A8C`) does not appear anywhere. This is a complete divergence from M7.1.

### Finding 19: Match level colors are not implemented

**Spec M7.1** defines semantic match colors:
- `match-strong`: emerald `#1F8F5F`
- `match-transferable`: amber `#C68A1A`
- `match-addressable`: orange `#D97338`
- `match-fundamental`: plum `#8B4A8B` (NOT red)

**Mockup lines 415, 422, 429** -- Match chips use `bg-green-100 text-green-700` for "strong", `bg-amber-100 text-amber-700` for "transferable". These use Tailwind defaults, not the spec's precise color values. The `match-fundamental` color is not present in the mockup.

**Implementation** does not appear to implement the match chip component at all.

### Finding 20: Font stack does not match M7.1

**Spec M7.1** specifies:
```
fontFamily.sans: ['Inter Variable', 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', 'system-ui', 'sans-serif']
```

**Mockup line 9** -- Google Fonts imports only `Inter:wght@400;500;600;700;800` -- no CJK font stack.
**Implementation** uses `next/font` which is correct per spec, but the font variable was not read from the codebase to verify the stack.

### Finding 21: Transition durations are not customized

**Spec M7.1** defines:
```
transitionDuration: 'instant': '80ms', 'fast': '160ms', 'base': '240ms', 'slow': '360ms'
```

**Mockup line 22** -- Uses `transition` (Tailwind default, ~150ms) everywhere. No custom duration classes are defined.
**Implementation** uses `transition` throughout without the custom duration tokens.

---

## 8. Accessibility

**Verdict: FAIL (P1)**

### Finding 22: Color contrast failure on role badge

**Mockup lines 313-315** -- The role badge uses `bg-indigo-100 text-indigo-700` (light indigo bg, dark indigo text). For WCAG AA, normal text requires 4.5:1 contrast. Indigo-100 (#e0e7ff) on indigo-700 (#4338ca) fails this threshold. The lighter indigo-100 background with the darker indigo-700 text does not provide sufficient contrast.

**Note**: Indigo-100 on white is fine; the issue is indigo-100 on indigo-700. For a badge with a colored background, the text should either be white (on dark enough backgrounds) or the background should be lighter.

### Finding 23: No focus indicators visible in code

Neither the mockup nor the implementation shows `:focus` styles or `focus-visible` utilities on interactive elements. The mockup uses `hover:` states but no equivalent `focus:` states. This is a critical accessibility gap for keyboard navigation.

**Mockup line 44** -- `hover:bg-indigo-700` but no corresponding `focus:ring` or `focus:outline`. The same pattern appears on all buttons and links.

### Finding 24: Interactive elements are not `<button>` or `<a>`

**Mockup line 85** -- Role cards are `<button>` elements, which is correct for clickable cards. Good.

**Mockup line 319** -- Nav tabs are rendered via JS as `<button>` elements inside a `<div>`. These should ideally be `<button role="tab">` with `role="tablist"` wrapper for ARIA tab pattern compliance.

**Mockup line 329** -- "退出" (exit) is a `<button>` but functions as a navigation element. An `<a>` tag or `<button>` with clear label would be more appropriate.

### Finding 25: Form inputs lack associated labels

**Mockup lines 447-448, 616-617, 619-620, 634-635, 687-688** -- URL inputs, text inputs, and email inputs use `placeholder` text but no `<label>` elements. Placeholders disappear when users start typing and do not meet accessibility requirements for form labels.

**Mockup lines 615-616** -- The JD Generator form has label elements (`<label class="block text-sm font-medium text-gray-700 mb-1.5">Job Title <span class="text-red-500">*</span></label>`), which is correct. But the URL input on the Analyze page does not.

### Finding 26: Semantic HTML structure is mostly correct

Both mockup and implementation use proper `<nav>`, `<main>`, `<section>`, `<footer>` landmarks. The heading hierarchy starts at `<h1>` for the main headline and descends correctly. This is a positive finding.

---

## Cross-File Consistency

### Finding 27: Mockup is bilingual (Chinese primary) but implementation is English-only

**Mockup** uses Chinese for all visible labels: "求职者入口", "招聘者入口", "功能", "定价", "免费版", "专业版". **Implementation** uses English throughout. This is an i18n gap -- if the target market is Singapore (Chinese- and English-speaking), both language versions should be available via i18n, not one file in Chinese and the implementation in English.

### Finding 28: CTA label mismatch between mockup and implementation for Free tier

| Element | Mockup | Implementation |
|---|---|---|
| Nav "Get Started" | "开始使用" (Chinese) | "Get Started" |
| Hero role button | "求职者入口" / "招聘者入口" | "Job Seeker" / "Recruiter" |
| Role card CTA (seeker) | "求职者入口" | none (card is not clickable to app) |
| Pricing Free CTA | "免费开始" | "Get Started Free" |

The CTA text is inconsistent between the two files. The mockup and implementation appear to be in different stages of internationalization.

---

## Priority Summary

### P1 (Must Fix)
1. **Brand colors**: Implement `brand-*` teal palette from M7.1. Current indigo/purple is the wrong color family.
2. **Focus indicators**: Add `focus-visible:ring` or `focus:outline` to all interactive elements.
3. **Missing landing page sections**: Add social proof strip, "How it works" 3-step, Singapore-specific section per M8.1.
4. **Color contrast on role badge**: indigo-100 on indigo-700 fails WCAG AA.
5. **Form labels**: Add `<label>` elements to all form inputs (Analyze page URL input specifically lacks one).

### P2 (Should Fix)
6. **Redundant role cards**: Remove the role cards below hero; they duplicate the hero role buttons.
7. **Role switcher in app shell**: Let users switch between seeker/recruiter without exiting.
8. **Watch Demo destination**: Either implement the demo or remove/relabel the button.
9. **"Try it on one job -- free" CTA**: Should point to `/analyse` without requiring sign-up per M8.1.
10. **No loading state on JD Generator and invite form**: Add spinner + disabled during submission.

### P3 (Nice to Fix)
11. **Match level colors**: Use spec values from M7.1 for match-strong/transferable/addressable/fundamental chips.
12. **Custom transition durations**: Define `instant/fast/base/slow` per M7.1.
13. **CJK font stack**: Add PingFang SC / Microsoft YaHei / Noto Sans SC to font-family.
14. **Toast improvements**: Add type icon, dismiss button.
15. **ARIA tab pattern**: Add `role="tablist"` and `role="tab"` to nav tabs.
