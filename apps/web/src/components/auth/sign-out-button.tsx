"use client";

import { SignOutButton as ClerkSignOutButton } from "@clerk/nextjs";
import { LogOut } from "lucide-react";

export function SignOutButton() {
  return (
    <ClerkSignOutButton>
      <button
        className="flex items-center gap-2 px-3 py-2 text-sm text-slate-600 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-colors"
      >
        <LogOut className="w-4 h-4" />
      </button>
    </ClerkSignOutButton>
  );
}
