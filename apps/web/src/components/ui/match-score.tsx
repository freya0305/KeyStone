"use client";

import { cn } from "@/lib/utils";

interface MatchScoreProps {
  score: number;
  size?: "sm" | "md" | "lg";
  showLabel?: boolean;
  label?: string;
  description?: string;
  className?: string;
}

export function MatchScore({
  score,
  size = "md",
  showLabel = true,
  label,
  description,
  className,
}: MatchScoreProps) {
  const sizes = {
    sm: { svg: "w-20 h-20", text: "text-xl", circle: 44, stroke: 8 },
    md: { svg: "w-32 h-32", text: "text-3xl", circle: 56, stroke: 10 },
    lg: { svg: "w-40 h-40", text: "text-4xl", circle: 68, stroke: 12 },
  };

  const { svg, text, circle, stroke } = sizes[size];
  const radius = circle;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const getColor = () => {
    if (score >= 75) return "stroke-green-500";
    if (score >= 60) return "stroke-amber-500";
    return "stroke-red-500";
  };

  const getDefaultLabel = () => {
    if (score >= 75) return "Good match!";
    if (score >= 60) return "Review suggested";
    return "Low match";
  };

  return (
    <div className={cn("flex items-center gap-4", className)}>
      <div className={cn("relative", svg)}>
        <svg className={cn("w-full h-full transform -rotate-90", svg)} viewBox="0 0 128 128">
          <circle
            cx="64"
            cy="64"
            r={radius}
            stroke="#e5e7eb"
            strokeWidth={stroke}
            fill="none"
          />
          <circle
            cx="64"
            cy="64"
            r={radius}
            className={getColor()}
            strokeWidth={stroke}
            fill="none"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            style={{ transition: "stroke-dashoffset 0.5s ease-out" }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className={cn("font-bold text-gray-900", text)}>{score}%</span>
        </div>
      </div>
      {showLabel && (
        <div className="flex-1">
          <p className="font-medium text-gray-900">
            {label || getDefaultLabel()}
          </p>
          {description && (
            <p className="text-sm text-gray-500 mt-0.5">{description}</p>
          )}
        </div>
      )}
    </div>
  );
}
