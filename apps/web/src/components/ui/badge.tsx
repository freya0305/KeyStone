"use client";

import * as React from "react";
import { clsx } from "clsx";

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "secondary" | "success" | "warning" | "destructive";
}

export const Badge = React.forwardRef<HTMLDivElement, BadgeProps>(
  ({ className, variant = "default", ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={clsx(
          "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium",
          {
            "bg-indigo-100 text-indigo-800": variant === "default",
            "bg-slate-100 text-slate-800": variant === "secondary",
            "bg-green-100 text-green-800": variant === "success",
            "bg-amber-100 text-amber-800": variant === "warning",
            "bg-red-100 text-red-800": variant === "destructive",
          },
          className
        )}
        {...props}
      />
    );
  }
);
Badge.displayName = "Badge";
