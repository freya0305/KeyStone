# Voice and Tone — KeyStone

## Brand Voice

**"Senior SG colleague"** — A competent, direct Singaporean professional who has seen many résumés and knows what works in the local market. Warm but not effusive. Informative without being pedantic. Honest without being harsh.

### Core Principles

1. **Be specific** — "GLC interviewers score on three dimensions" beats "interviews are subjective"
2. **Be actionable** — Every suggestion comes with the "why" so users can adapt, not just copy
3. **Respect the user's intelligence** — No hand-holding, no excessive reassurance
4. **Acknowledge context** — Singapore hiring has real quirks (NS, GLC vs MNC, education hierarchy). Don't pretend they don't exist.

### Tone by Situation

| Situation | Tone |
|---|---|
| Suggestion rationale | Direct, explanatory, collegial |
| Error message | Clear, no-blame, actionable next step |
| Empty state | Forward-looking, specific action |
| Loading state | Brief, informative, shows progress |
| Success (accept) | Brief acknowledgment, move on |
| Upsell/paywall | Honest about value, no pressure |

### Banned Phrases

```
"I'm an AI"
"as an AI assistant"
"I'd be happy to"
"great question"
"in conclusion"
any emoji in toasts or body copy
"Contact support" (without actual contact info)
```

### Singapore-Specific Voice Rules

- **NS framing**: When discussing NS-related gaps, be matter-of-fact. "Most candidates at this level face the same gap" is better than making it feel like a personal failing.
- **GLC vs MNC**: Name the employer type explicitly. "This GLC values quantified leadership" is more useful than "consider the company's culture."
- **Education hierarchy**: Be factual about degree requirements. Don't over-index on prestige — Skills and experience matter equally.

---

## Per-Persona Copy Variants

Persona is inferred from onboarding questionnaire ("what are you looking for?"). Defaults to "mid-career" if unknown.

### Fresh Grad (< 2 years experience)

**Onboarding:**
- "Nice. 13 to go."
- "Most people in your position have 3-5 of these already. Let's check which ones."

**Suggestion accepted:**
- "Good one. Keep these coming."
- "Added to your resume."

**Fundamental gap:**
- "This one's harder to fix quickly — most people at your level face it. Worth knowing, not a blocker."

### Mid-Career (2-10 years)

**Onboarding:**
- "Applied. Let's see where you match and where you don't."
- "You've got experience — let's find where it maps."

**Suggestion accepted:**
- "Applied. Reframing this as transferable."
- "Good catch. That reframe works."

**Fundamental gap:**
- "This is a longer-term play — most candidates at your level have the same gap."

### PMET (10+ years, senior roles)

**Onboarding:**
- "Applied. This rewording reads like the senior leader you are."
- "Let's make sure your experience speaks at the right level."

**Suggestion accepted:**
- "Applied."
- "Senior-level language confirmed."

**Fundamental gap:**
- "These gaps are normal at your level — hiring committees expect to see how you address them."

---

## Component Copy Rules

### Buttons

| Context | Copy |
|---|---|
| Primary CTA | "Continue" / "Save" / "Apply" — specific to action |
| Secondary | "Back" / "Cancel" |
| Destructive | "Delete" / "Remove" — no confirmation in label |
| Paywall | "Upgrade to Pro" |

### Empty States

**DO:**
- "Your applications will appear here once you start applying."
- "No suggestions yet — paste a job URL above to get started."

**DON'T:**
- "Nothing to see here"
- "You're all set!" (when nothing exists)
- Any mascot or cartoon

### Error States

**DO:**
- "We couldn't read this file. Try a different format or paste the text directly."
- "Analysis timed out. Your results are still loading — check back in a moment."

**DON'T:**
- "An error occurred" (no context)
- "Please try again later" (no specific guidance)

### Loading Messages

Rotate through these during long analyses:
- "Parsing job description..."
- "Identifying key requirements..."
- "Comparing with your experience..."
- "Generating match suggestions..."
- "GLC interviewers typically score on Leadership, Customer Focus, and Innovation — three distinct dimensions."

---

## Implementation

The banned phrase filter is implemented in `lib/copy-filter.ts`. It:
1. Logs a warning when banned phrases are detected
2. Strips the phrase and displays the remaining content
3. Does NOT block or error — just sanitizes output

```typescript
// lib/copy-filter.ts
export function filterBannedPhrases(text: string): { cleaned: string; hadBanned: boolean } {
  const banned = [
    "I'm an AI",
    "as an AI assistant",
    "I'd be happy to",
    "great question",
    "in conclusion",
  ]

  let cleaned = text
  let hadBanned = false

  for (const phrase of banned) {
    if (cleaned.includes(phrase)) {
      cleaned = cleaned.replace(phrase, "")
      hadBanned = true
      console.warn(`[copy-filter] Banned phrase removed: "${phrase}"`)
    }
  }

  // Also strip emoji
  cleaned = cleaned.replace(/[\p{Emoji_Presentation}]/gu, "")

  return { cleaned: cleaned.trim(), hadBanned }
}
```

---

## WCAG Accessibility

- All text must pass 4.5:1 contrast ratio (AA)
- Interactive elements must have visible focus states
- Buttons must have descriptive labels — "Continue" not "Click here"
- Error messages must be programmatically associated with inputs
