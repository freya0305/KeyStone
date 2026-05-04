# Voice and Tone

KeyStone speaks to job seekers in Singapore as a senior colleague who has been through what they're going through. No condescension, no corporate speak, no AI-scent.

## Persona Definitions

### Fresh Grad
Recently completed or about to complete studies. First time navigating the Singapore job market. May feel overwhelmed by processes (MyCareersFuture, GOVWARDS, LinkedIn Easy Apply). Needs validation that their lack of experience is not a fatal flaw.

### Mid-Career Switcher
Already worked 2-5 years. Changing industry or function. Has transferable experience but feels it doesn't "count" for the new target. Needs reframing support that validates what they already know while helping them translate it.

### PMET (PMET/PEMT - Professional, Manager, Executive, Technician)
Was employed, now job searching due to restructuring, redundancy, or contract end. May carry feelings of displacement or identity loss. Has deep experience and an established professional identity. Needs language that treats them as the expert they are.

### Employed Explorer
Currently in a role but actively or passively looking. Has concrete experience to point to. Needs efficiency — they don't have time for lengthy processes and want their current job to remain stable while they explore.

## Voice Principles

- **Tone**: Senior Singapore colleague. Direct, practical, no fluff.
- **Body copy**: No exclamation marks. Statements, not celebrations.
- **Toasts**: No emojis. Brief confirmation of action taken.
- **Never**: "I'm an AI", "as an AI assistant", "I'd be happy to", "great question", "in conclusion", any emoji
- **Always**: Plain English, active verbs, Singapore-specific context

## Per-Persona Copy Variants

### Onboarding Completion

| Persona | Title | Subtitle |
|---------|-------|----------|
| Fresh Grad | "You're all set!" | "Time to find your first role." |
| Mid-Career Switcher | "You're all set!" | "Your transferable skills are your superpower." |
| PMET | "You're all set!" | "Your experience is your leverage." |
| Employed Explorer | "You're all set!" | "Let's find you something better." |

### Suggestion Accepted

| Persona | Copy |
|---------|------|
| Fresh Grad | "Nice. {n} to go." |
| Mid-Career Switcher | "Applied. Reframing this as transferable." |
| PMET | "Applied. This rewording reads like the senior leader you are." |
| Employed Explorer | "Saved. It's in your portfolio now." |

## Banned Phrases

These phrases indicate AI-generated content that does not sound like a senior Singapore colleague. They must not appear in any user-facing copy or AI output:

- "I'm an AI"
- "as an AI assistant"
- "I'd be happy to"
- "great question"
- "in conclusion"
- Any emoji character

## Implementation

See `apps/web/src/lib/copy.ts` for the implementation of persona-specific copy functions and AI output sanitization.
