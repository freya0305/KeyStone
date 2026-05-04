import { auth } from "@clerk/nextjs"
import { redirect } from "next/navigation"
import Link from "next/link"

export default function RecruiterLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const { userId } = auth()

  if (!userId) {
    redirect("/sign-in?redirect_url=/recruiter")
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Recruiter Header */}
      <header className="bg-white border-b sticky top-0 z-50">
        <div className="container mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <Link href="/recruiter" className="flex items-center gap-2">
              <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">KS</span>
              </div>
              <span className="font-semibold text-lg">KeyStone</span>
              <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded">Recruiter</span>
            </Link>
            <nav className="hidden md:flex items-center gap-1">
              <Link
                href="/recruiter"
                className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md"
              >
                Dashboard
              </Link>
              <Link
                href="/recruiter/jd"
                className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md"
              >
                Job Descriptions
              </Link>
              <Link
                href="/recruiter/templates"
                className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md"
              >
                Templates
              </Link>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <Link
              href="/app"
              className="px-3 py-1.5 text-sm border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Job Seeker
            </Link>
            <Link
              href="/recruiter/settings"
              className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md"
            >
              Settings
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}
