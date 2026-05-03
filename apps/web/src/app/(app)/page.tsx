"use client";

import { useUser } from "@clerk/nextjs";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function AppPage() {
  const { user, isLoaded } = useUser();
  const router = useRouter();

  useEffect(() => {
    if (isLoaded && user) {
      const isRecruiter = user.publicMetadata?.userType === "recruiter";
      if (isRecruiter) {
        router.replace("/app/recruiter");
      } else {
        router.replace("/app/job-seeker");
      }
    }
  }, [isLoaded, user, router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
    </div>
  );
}
