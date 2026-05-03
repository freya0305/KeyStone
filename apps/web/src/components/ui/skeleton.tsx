import { cn } from "@/lib/utils";

interface SkeletonProps {
  className?: string;
}

export function Skeleton({ className }: SkeletonProps) {
  return (
    <div
      className={cn(
        "animate-pulse bg-gray-200 rounded",
        className
      )}
    />
  );
}

export function CardSkeleton() {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5">
      <Skeleton className="h-4 w-24 mb-3" />
      <Skeleton className="h-8 w-16" />
    </div>
  );
}

export function TableRowSkeleton() {
  return (
    <div className="flex items-center gap-4 px-6 py-4 border-b border-gray-100">
      <Skeleton className="h-4 flex-1" />
      <Skeleton className="h-4 w-12" />
      <Skeleton className="h-4 w-20" />
      <Skeleton className="h-6 w-16 rounded-full" />
    </div>
  );
}

export function FormSkeleton() {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <Skeleton className="h-4 w-24 mb-4" />
        <Skeleton className="h-32 w-full rounded-lg" />
      </div>
      <div className="bg-white rounded-xl border border-gray-200 p-6">
        <Skeleton className="h-4 w-32 mb-4" />
        <Skeleton className="h-24 w-full rounded-lg" />
      </div>
      <Skeleton className="h-12 w-full rounded-lg" />
    </div>
  );
}
