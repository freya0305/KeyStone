"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
  FileText,
  LayoutDashboard,
  History,
  Briefcase,
  PlusCircle,
  FileStack,
  Settings,
  HelpCircle,
  LogOut,
  ChevronDown,
  User,
} from "lucide-react";

interface NavItemProps {
  href: string;
  icon: React.ReactNode;
  label: string;
  isActive?: boolean;
}

function NavItem({ href, icon, label, isActive }: NavItemProps) {
  return (
    <Link
      href={href}
      className={cn(
        "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
        isActive
          ? "bg-indigo-50 text-indigo-600"
          : "text-gray-600 hover:text-gray-900 hover:bg-gray-100"
      )}
    >
      {icon}
      {label}
    </Link>
  );
}

interface AppShellProps {
  children: React.ReactNode;
  userName?: string;
  userPlan?: string;
}

export function AppShell({
  children,
  userName = "Alex Tan",
  userPlan = "Free Plan",
}: AppShellProps) {
  const pathname = usePathname();
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);

  // Determine product context from pathname
  const isRecruiter = pathname?.startsWith("/recruiter");
  const product = isRecruiter ? "recruiter" : "job-seeker";

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            {/* Left side */}
            <div className="flex items-center gap-6">
              <Link href="/" className="flex items-center gap-2">
                <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <span className="font-bold text-xl text-gray-900">KeyStone</span>
              </Link>

              {/* Product Switcher */}
              <div className="product-switch">
                <Link
                  href="/app"
                  className={cn(
                    "product-btn",
                    !isRecruiter ? "active" : "inactive"
                  )}
                >
                  <span className="hidden sm:inline">For Job Seekers</span>
                  <span className="sm:hidden">Seeker</span>
                </Link>
                <Link
                  href="/recruiter"
                  className={cn(
                    "product-btn",
                    isRecruiter ? "active" : "inactive"
                  )}
                >
                  <span className="hidden sm:inline">For Recruiters</span>
                  <span className="sm:hidden">Recruiter</span>
                </Link>
              </div>

              {/* Nav Links */}
              <div className="hidden md:flex items-center gap-1">
                {product === "job-seeker" ? (
                  <>
                    <NavItem
                      href="/app"
                      icon={<LayoutDashboard className="w-4 h-4" />}
                      label="Dashboard"
                      isActive={pathname === "/app"}
                    />
                    <NavItem
                      href="/app/analyze"
                      icon={<FileStack className="w-4 h-4" />}
                      label="Analyze"
                      isActive={pathname === "/app/analyze"}
                    />
                    <NavItem
                      href="/app/history"
                      icon={<History className="w-4 h-4" />}
                      label="History"
                      isActive={pathname === "/app/history"}
                    />
                  </>
                ) : (
                  <>
                    <NavItem
                      href="/recruiter"
                      icon={<LayoutDashboard className="w-4 h-4" />}
                      label="Dashboard"
                      isActive={pathname === "/recruiter"}
                    />
                    <NavItem
                      href="/recruiter/generate"
                      icon={<PlusCircle className="w-4 h-4" />}
                      label="New JD"
                      isActive={pathname === "/recruiter/generate"}
                    />
                    <NavItem
                      href="/recruiter/templates"
                      icon={<Briefcase className="w-4 h-4" />}
                      label="Templates"
                      isActive={pathname === "/recruiter/templates"}
                    />
                  </>
                )}
              </div>
            </div>

            {/* Right side */}
            <div className="flex items-center gap-4">
              <div className="relative">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2"
                >
                  <div className="hidden sm:block text-right">
                    <p className="text-sm font-medium text-gray-900">{userName}</p>
                    <p className="text-xs text-gray-500">{userPlan}</p>
                  </div>
                  <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold">
                    {userName
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </div>
                  <ChevronDown className="w-4 h-4 text-gray-400" />
                </button>

                {showUserMenu && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-200 py-2">
                    <div className="px-4 py-2 border-b border-gray-100">
                      <p className="text-sm font-medium text-gray-900">{userName}</p>
                      <p className="text-xs text-gray-500">{userPlan}</p>
                    </div>
                    <div className="py-1">
                      <Link
                        href="/app/settings"
                        className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                      >
                        <Settings className="w-4 h-4" />
                        Settings
                      </Link>
                      <Link
                        href="/help"
                        className="flex items-center gap-3 px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                      >
                        <HelpCircle className="w-4 h-4" />
                        Help
                      </Link>
                    </div>
                    <div className="border-t border-gray-100 pt-1">
                      <button className="flex items-center gap-3 px-4 py-2 text-sm text-red-600 hover:bg-red-50 w-full">
                        <LogOut className="w-4 h-4" />
                        Sign Out
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Mobile menu */}
        {showMobileMenu && (
          <div className="md:hidden border-t border-gray-200 bg-white px-4 py-3">
            <div className="flex flex-col gap-2">
              {product === "job-seeker" ? (
                <>
                  <Link
                    href="/app"
                    className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  >
                    <LayoutDashboard className="w-4 h-4" />
                    Dashboard
                  </Link>
                  <Link
                    href="/app/analyze"
                    className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  >
                    <FileStack className="w-4 h-4" />
                    Analyze
                  </Link>
                  <Link
                    href="/app/history"
                    className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  >
                    <History className="w-4 h-4" />
                    History
                  </Link>
                </>
              ) : (
                <>
                  <Link
                    href="/recruiter"
                    className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  >
                    <LayoutDashboard className="w-4 h-4" />
                    Dashboard
                  </Link>
                  <Link
                    href="/recruiter/generate"
                    className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  >
                    <PlusCircle className="w-4 h-4" />
                    New JD
                  </Link>
                  <Link
                    href="/recruiter/templates"
                    className="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:text-gray-900 hover:bg-gray-100"
                  >
                    <Briefcase className="w-4 h-4" />
                    Templates
                  </Link>
                </>
              )}
            </div>
          </div>
        )}
      </nav>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>
    </div>
  );
}
