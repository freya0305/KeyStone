# KeyStone Design System

## Overview

KeyStone uses a custom design system built on Tailwind CSS with shadcn/ui components. The system emphasizes a warm, professional aesthetic using a stone (warm gray) palette with teal-blue brand accents.

## Color Tokens

### Brand Primary

The brand primary color is **Teal-Blue** (`#1E7A8C`).

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| `brand-50` | `#EFF8FA` | (auto) | Subtle backgrounds |
| `brand-100` | `#D5ECF1` | (auto) | Light tinted backgrounds |
| `brand-300` | `#7FC4D2` | (auto) | Borders, icons |
| `brand-500` | `#1E7A8C` | (auto) | Primary actions, links |
| `brand-600` | `#155E6E` | (auto) | Hover states |
| `brand-700` | `#0F4751` | (auto) | Active states |
| `brand-900` | `#082C33` | (auto) | High contrast text |

### Neutral Palette (Stone)

We use **Stone** (warm gray) instead of cool gray for a warmer, more professional feel.

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|-------|
| `stone-50` | `#FAFAF7` | (auto) | Page backgrounds |
| `stone-100` | `#F5F5F2` | (auto) | Card backgrounds |
| `stone-200` | `#E7E5E4` | (auto) | Borders |
| `stone-300` | `#D6D3D1` | (auto) | Disabled states |
| `stone-400` | `#A8A29E` | (auto) | Placeholder text |
| `stone-500` | `#78716C` | (auto) | Secondary text |
| `stone-600` | `#57534E` | (auto) | Body text |
| `stone-700` | `#44403C` | (auto) | Headings |
| `stone-800` | `#292524` | (auto) | Dark mode body |
| `stone-900` | `#1C1917` | (auto) | Dark mode headings |
| `stone-950` | `#0C0A09` | (auto) | Dark mode backgrounds |

### Match Level Colors

Match levels indicate how well a skill or qualification matches a job requirement.

| Level | Color | Hex | Usage |
|-------|-------|-----|-------|
| **Strong** | Emerald | `#1F8F5F` | Perfect match for the role |
| **Transferable** | Amber | `#C68A1A` | Can be applied with some adaptation |
| **Addressable** | Orange | `#D97338` | Needs training to apply |
| **Fundamental** | Purple | `#8B4A8B` | Foundational requirement |

#### Match Color Tints

Each match level has a corresponding tint color for badges and backgrounds:

| Level | Tint | Hex |
|-------|------|-----|
| Strong | `match-strong-tint` | `#E6F4EE` |
| Transferable | `match-transferable-tint` | `#FBF3DF` |
| Addressable | `match-addressable-tint` | `#FCEBDD` |
| Fundamental | `match-fundamental-tint` | `#F2E6F2` |

## Typography

### Font Families

| Role | Font | Fallback |
|------|------|----------|
| **Body** | Inter Variable | PingFang SC, Microsoft YaHei, system-ui |
| **Headings** | Fraunces | Instrument Serif, Georgia, serif |
| **Code** | JetBrains Mono | Fira Code, Consolas, monospace |

### Usage

```tsx
// Headings use font-display
<h1 className="font-display text-stone-900 dark:text-stone-50">
  Job Application Tracker
</h1>

// Body text uses font-sans
<p className="font-sans text-stone-600 dark:text-stone-300">
  Track your job applications and get AI-powered insights.
</p>

// Code uses font-mono
<code className="font-mono text-sm bg-stone-100 dark:bg-stone-800">
  POST /api/applications
</code>
```

## Motion Tokens

Motion tokens provide consistent animation timings across the application.

| Token | Duration | Usage |
|-------|----------|-------|
| `instant` | 80ms | Micro-interactions (toggles, checkboxes) |
| `fast` | 160ms | Quick feedback (buttons, hovers) |
| `base` | 240ms | Standard transitions (modals, dropdowns) |
| `slow` | 360ms | Emphasis transitions (page elements) |

### Usage

```tsx
<button
  className="transition-all duration-base hover:scale-105"
>
  Hover me
</button>
```

## Component Usage

### MatchBadge

Display match levels with proper color coding.

```tsx
import { MatchBadge, MatchBadgeDot } from "@/components/keystone/MatchBadge"

// Badge with label
<MatchBadge level="strong">Python (5 years)</MatchBadge>

// Dot indicator
<span className="flex items-center gap-2">
  <MatchBadgeDot level="transferable" />
  JavaScript
</span>

// Sizes
<MatchBadge level="addressable" size="sm">Beginner</MatchBadge>
<MatchBadge level="fundamental" size="md">Fundamental</MatchBadge>
```

### ProGate / PaywallBanner

Gate content behind Pro subscription.

```tsx
import { PaywallBanner } from "@/components/keystone/ProGate"

<PaywallBanner section="ATS Optimization" count={12} />
```

### AutoCloseBanner

Show auto-closed applications for review.

```tsx
import { AutoCloseBanner } from "@/components/keystone/AutoCloseBanner"

<AutoCloseBanner
  applications={autoClosedApps}
  onCorrect={(ids) => handleCorrect(ids)}
  onDismiss={() => handleDismiss()}
/>
```

### DropZone

File upload for resumes.

```tsx
import { DropZone } from "@/components/keystone/DropZone"

<DropZone
  onFile={(file, resumeId) => handleFile(file, resumeId)}
  onText={() => setShowTextInput(true)}
  onUploadSuccess={(result) => handleSuccess(result)}
/>
```

### shadcn/ui Components

#### Button

```tsx
import { Button } from "@/components/ui/button"

// Variants
<Button variant="default">Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Destructive</Button>

// Sizes
<Button size="sm">Small</Button>
<Button size="default">Default</Button>
<Button size="lg">Large</Button>
<Button size="icon">Icon</Button>
```

#### Card

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card"

<Card>
  <CardHeader>
    <CardTitle>Application Status</CardTitle>
    <CardDescription>Track your job applications</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card content here</p>
  </CardContent>
  <CardFooter>
    <Button>View Details</Button>
  </CardFooter>
</Card>
```

#### Input

```tsx
import { Input } from "@/components/ui/input"

<Input type="email" placeholder="Enter your email" />
<Input type="text" placeholder="Job title" />
```

#### Badge

```tsx
import { Badge } from "@/components/ui/badge"

// Match level variants
<Badge variant="strong">Strong Match</Badge>
<Badge variant="transferable">Transferable</Badge>
<Badge variant="addressable">Addressable</Badge>
<Badge variant="fundamental">Fundamental</Badge>

// Standard variants
<Badge variant="default">Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Destructive</Badge>
<Badge variant="outline">Outline</Badge>
```

## Dark Mode

The design system supports dark mode via Tailwind's `class` strategy. Dark mode colors are defined using CSS variables in `globals.css`.

### Usage

```tsx
// Using Tailwind dark: prefix
<div className="bg-stone-50 dark:bg-stone-900">
  <p className="text-stone-900 dark:text-stone-50">Adapts to dark mode</p>
</div>

// Using design system colors (already dark-mode aware)
<div className="bg-brand-50 dark:bg-brand-900/20">
  Brand color adapts automatically
</div>
```

## Responsive Design

The design system is mobile-first. Breakpoints:

| Breakpoint | Min Width | Usage |
|------------|-----------|-------|
| `sm` | 640px | Large phones |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktops |
| `2xl` | 1400px | Large screens |

## CSS Variables Reference

```css
/* Background & Foreground */
--background: hsl(0 0% 100%);
--foreground: hsl(20 14.3% 30.7%);

/* Primary */
--primary: hsl(189 47% 32%);
--primary-foreground: hsl(0 0% 100%);

/* Secondary */
--secondary: hsl(30 6.7% 96.5%);
--secondary-foreground: hsl(20 14.3% 30.7%);

/* Match Colors */
--match-strong: #1F8F5F;
--match-transferable: #C68A1A;
--match-addressable: #D97338;
--match-fundamental: #8B4A8B;

/* Motion */
--motion-instant: 80ms;
--motion-fast: 160ms;
--motion-base: 240ms;
--motion-slow: 360ms;
```

## File Structure

```
apps/web/
├── src/
│   ├── app/
│   │   ├── globals.css          # Design tokens & base styles
│   │   └── layout.tsx            # Font loading
│   ├── components/
│   │   ├── ui/                   # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   └── badge.tsx
│   │   └── keystone/             # KeyStone-specific components
│   │       ├── MatchBadge.tsx
│   │       ├── MatchChip.tsx
│   │       ├── ProGate.tsx
│   │       ├── AutoCloseBanner.tsx
│   │       ├── BatchUpdateModal.tsx
│   │       └── DropZone.tsx
│   └── lib/
│       └── utils.ts              # cn() utility for class merging
├── tailwind.config.ts           # Tailwind configuration with design tokens
└── components.json               # shadcn/ui configuration
```
