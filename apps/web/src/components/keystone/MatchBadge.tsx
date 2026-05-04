"use client"

import { cn } from "@/lib/utils"

type MatchLevel = "strong" | "transferable" | "addressable" | "fundamental"

interface MatchBadgeProps {
  level: MatchLevel
  children: React.ReactNode
  className?: string
  size?: "sm" | "md" | "lg"
}

const MATCH_STYLES: Record<MatchLevel, { bg: string; text: string; border: string }> = {
  strong: {
    bg: "bg-match-strong-tint dark:bg-match-strong-tint",
    text: "text-match-strong dark:text-match-strong",
    border: "border-match-strong/20 dark:border-match-strong/40",
  },
  transferable: {
    bg: "bg-match-transferable-tint dark:bg-match-transferable-tint",
    text: "text-match-transferable dark:text-match-transferable",
    border: "border-match-transferable/20 dark:border-match-transferable/40",
  },
  addressable: {
    bg: "bg-match-addressable-tint dark:bg-match-addressable-tint",
    text: "text-match-addressable dark:text-match-addressable",
    border: "border-match-addressable/20 dark:border-match-addressable/40",
  },
  fundamental: {
    bg: "bg-match-fundamental-tint dark:bg-match-fundamental-tint",
    text: "text-match-fundamental dark:text-match-fundamental",
    border: "border-match-fundamental/20 dark:border-match-fundamental/40",
  },
}

const SIZE_STYLES = {
  sm: "px-2 py-0.5 text-xs",
  md: "px-2.5 py-0.5 text-sm",
  lg: "px-3 py-1 text-sm",
}

export function MatchBadge({
  level,
  children,
  className,
  size = "md",
}: MatchBadgeProps) {
  const styles = MATCH_STYLES[level]

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full font-medium border",
        styles.bg,
        styles.text,
        styles.border,
        SIZE_STYLES[size],
        className
      )}
    >
      {children}
    </span>
  )
}

export function MatchBadgeDot({ level, className }: { level: MatchLevel; className?: string }) {
  const dotColors: Record<MatchLevel, string> = {
    strong: "bg-match-strong",
    transferable: "bg-match-transferable",
    addressable: "bg-match-addressable",
    fundamental: "bg-match-fundamental",
  }

  return (
    <span
      className={cn("inline-block w-2 h-2 rounded-full", dotColors[level], className)}
      title={level}
    />
  )
}

// Helper to get match level label
export function getMatchLevelLabel(level: MatchLevel): string {
  const labels: Record<MatchLevel, string> = {
    strong: "Strong Match",
    transferable: "Transferable",
    addressable: "Addressable",
    fundamental: "Fundamental",
  }
  return labels[level]
}
