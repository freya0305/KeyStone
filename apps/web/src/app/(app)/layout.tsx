"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useUser } from "@clerk/nextjs";
import { clsx } from "clsx";
import {
  LayoutDashboard,
  FileText,
  History,
  Users,
  FileEdit,
  LogOut,
} from "lucide-react";
import { SignOutButton } from "@/components/auth/sign-out-button";

const jobSeekerNav = [
  { href: "/app/job-seeker", label: "Dashboard", icon: LayoutDashboard },
  { href: "/app/job-seeker/analyze", label: "Analyze Job", icon: FileText },
  { href: "/app/job-seeker/history", label: "History", icon: History },
];

const recruiterNav = [
  { href: "/app/recruiter", label: "Dashboard", icon: LayoutDashboard },
  { href: "/app/recruiter/jd", label: "JD Generator", icon: FileEdit },
  { href: "/app/recruiter/team", label: "Team", icon: Users },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { user, isLoaded } = useUser();

  if (!isLoaded) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  const isRecruiter = user?.publicMetadata?.userType === "recruiter";
  const navItems = isRecruiter ? recruiterNav : jobSeekerNav;

  return (
    <div className="min-h-screen bg-slate-50">
      {/* Top Navigation */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center gap-8">
              <Link href="/app" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <span className="font-bold text-xl text-slate-900">KeyStone</span>
              </Link>

              {/* Nav Links */}
              <nav className="hidden md:flex items-center gap-1">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  const isActive = pathname === item.href;
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      className={clsx(
                        "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors",
                        isActive
                          ? "bg-indigo-50 text-indigo-700"
                          : "text-slate-600 hover:bg-slate-100"
                      )}
                    >
                      <Icon className="w-4 h-4" />
                      {item.label}
                    </Link>
                  );
                })}
              </nav>
            </div>

            {/* User Menu */}
            <div className="flex items-center gap-4">
              <div className="text-sm text-right">
                <p className="font-medium text-slate-900">{user?.fullName}</p>
                <p className="text-slate-500 text-xs">
                  {isRecruiter ? "Recruiter" : "Job Seeker"}
                </p>
              </div>
              <SignOutButton />
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
