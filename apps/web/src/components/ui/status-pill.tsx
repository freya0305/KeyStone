import { cn } from "@/lib/utils";

type StatusType =
  | "good"
  | "great"
  | "review"
  | "pending"
  | "low"
  | "draft"
  | "applied"
  | "response"
  | "interview"
  | "final"
  | "active"
  | "inactive";

interface StatusPillProps {
  status: StatusType;
  label?: string;
  className?: string;
}

const statusConfig: Record<
  StatusType,
  { bg: string; text: string; dot: string; defaultLabel: string }
> = {
  good: {
    bg: "bg-green-100",
    text: "text-green-700",
    dot: "bg-green-500",
    defaultLabel: "Good",
  },
  great: {
    bg: "bg-green-100",
    text: "text-green-700",
    dot: "bg-green-500",
    defaultLabel: "Great",
  },
  review: {
    bg: "bg-amber-100",
    text: "text-amber-700",
    dot: "bg-amber-500",
    defaultLabel: "Review",
  },
  pending: {
    bg: "bg-amber-100",
    text: "text-amber-700",
    dot: "bg-amber-500",
    defaultLabel: "Pending",
  },
  low: {
    bg: "bg-red-100",
    text: "text-red-700",
    dot: "bg-red-500",
    defaultLabel: "Low",
  },
  draft: {
    bg: "bg-gray-100",
    text: "text-gray-600",
    dot: "bg-gray-400",
    defaultLabel: "Draft",
  },
  applied: {
    bg: "bg-blue-100",
    text: "text-blue-700",
    dot: "bg-blue-500",
    defaultLabel: "Applied",
  },
  response: {
    bg: "bg-amber-100",
    text: "text-amber-700",
    dot: "bg-amber-500",
    defaultLabel: "Response",
  },
  interview: {
    bg: "bg-teal-100",
    text: "text-teal-700",
    dot: "bg-teal-500",
    defaultLabel: "Interview",
  },
  final: {
    bg: "bg-green-100",
    text: "text-green-700",
    dot: "bg-green-500",
    defaultLabel: "Final",
  },
  active: {
    bg: "bg-green-100",
    text: "text-green-700",
    dot: "bg-green-500",
    defaultLabel: "Active",
  },
  inactive: {
    bg: "bg-gray-100",
    text: "text-gray-500",
    dot: "bg-gray-400",
    defaultLabel: "Inactive",
  },
};

export function StatusPill({ status, label, className }: StatusPillProps) {
  const config = statusConfig[status];

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium",
        config.bg,
        config.text,
        className
      )}
    >
      <span className={cn("w-1.5 h-1.5 rounded-full", config.dot)} />
      {label || config.defaultLabel}
    </span>
  );
}
