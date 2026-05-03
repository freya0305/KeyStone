"use client";

import * as React from "react";
import { clsx } from "clsx";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "destructive";
  size?: "sm" | "md" | "lg";
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={clsx(
          "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
          {
            "bg-indigo-600 text-white hover:bg-indigo-700 focus-visible:ring-indigo-600":
              variant === "primary",
            "bg-slate-100 text-slate-900 hover:bg-slate-200 focus-visible:ring-slate-400":
              variant === "secondary",
            "border border-slate-300 bg-transparent hover:bg-slate-50 focus-visible:ring-slate-400":
              variant === "outline",
            "bg-transparent hover:bg-slate-100 focus-visible:ring-slate-400":
              variant === "ghost",
            "bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-600":
              variant === "destructive",
          },
          {
            "h-8 px-3 text-sm": size === "sm",
            "h-10 px-4 text-sm": size === "md",
            "h-12 px-6 text-base": size === "lg",
          },
          className
        )}
        {...props}
      />
    );
  }
);
Button.displayName = "Button";
