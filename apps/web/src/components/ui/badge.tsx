import * as React from "react"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80",
        secondary:
          "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive:
          "border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/80",
        outline: "text-foreground",
        // Match level variants
        strong:
          "border-transparent bg-match-strong-tint text-match-strong dark:bg-match-strong-tint dark:text-match-strong",
        transferable:
          "border-transparent bg-match-transferable-tint text-match-transferable dark:bg-match-transferable-tint dark:text-match-transferable",
        addressable:
          "border-transparent bg-match-addressable-tint text-match-addressable dark:bg-match-addressable-tint dark:text-match-addressable",
        fundamental:
          "border-transparent bg-match-fundamental-tint text-match-fundamental dark:bg-match-fundamental-tint dark:text-match-fundamental",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  )
}

export { Badge, badgeVariants }
