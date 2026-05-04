"use client"

type MatchLevel = 'strong' | 'transferable' | 'addressable' | 'fundamental'

interface MatchChipProps {
  level: MatchLevel
  children: React.ReactNode
}

const MATCH_STYLES: Record<MatchLevel, { bg: string; text: string; border: string }> = {
  strong: {
    bg: 'bg-emerald-50 dark:bg-emerald-950',
    text: 'text-emerald-700 dark:text-emerald-300',
    border: 'border-emerald-200 dark:border-emerald-800',
  },
  transferable: {
    bg: 'bg-amber-50 dark:bg-amber-950',
    text: 'text-amber-700 dark:text-amber-300',
    border: 'border-amber-200 dark:border-amber-800',
  },
  addressable: {
    bg: 'bg-orange-50 dark:bg-orange-950',
    text: 'text-orange-700 dark:text-orange-300',
    border: 'border-orange-200 dark:border-orange-800',
  },
  fundamental: {
    bg: 'bg-purple-50 dark:bg-purple-950',
    text: 'text-purple-700 dark:text-purple-300',
    border: 'border-purple-200 dark:border-purple-800',
  },
}

export function MatchChip({ level, children }: MatchChipProps) {
  const styles = MATCH_STYLES[level]

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${styles.bg} ${styles.text} ${styles.border}`}
    >
      {children}
    </span>
  )
}

export function MatchLevelDot({ level }: { level: MatchLevel }) {
  const dotColors: Record<MatchLevel, string> = {
    strong: 'bg-emerald-500',
    transferable: 'bg-amber-500',
    addressable: 'bg-orange-500',
    fundamental: 'bg-purple-500',
  }

  return (
    <span
      className={`inline-block w-2 h-2 rounded-full ${dotColors[level]}`}
      title={level}
    />
  )
}
