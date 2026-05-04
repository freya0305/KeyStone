import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">KS</span>
            </div>
            <span className="font-semibold text-xl">KeyStone</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <Link href="/how-it-works" className="text-sm text-gray-600 hover:text-gray-900">
              How it works
            </Link>
            <Link href="/pricing" className="text-sm text-gray-600 hover:text-gray-900">
              Pricing
            </Link>
            <Link href="/try" className="text-sm text-gray-600 hover:text-gray-900">
              Try free
            </Link>
            <Link
              href="/sign-in"
              className="text-sm text-gray-600 hover:text-gray-900"
            >
              Sign in
            </Link>
            <Link
              href="/sign-up"
              className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors"
            >
              Get started
            </Link>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
          Land your dream job in Singapore
          <br />
          <span className="text-blue-600">with AI-powered precision</span>
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto mb-8">
          Upload your resume, paste a job posting, and get personalized suggestions
          tailored to each role. Built for Singapore&apos;s unique hiring landscape.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            href="/analyse"
            className="px-8 py-4 bg-blue-600 text-white text-lg rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try for free
          </Link>
          <Link
            href="/recruiter"
            className="px-8 py-4 bg-white border border-gray-300 text-gray-700 text-lg rounded-lg hover:bg-gray-50 transition-colors"
          >
            For recruiters →
          </Link>
        </div>
        <p className="mt-4 text-sm text-gray-500">
          Free tier: 3 matches/month • No credit card required
        </p>
      </section>

      {/* Features */}
      <section className="container mx-auto px-4 py-16">
        <h2 className="text-2xl font-bold text-center mb-12">
          Everything you need to stand out
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="font-semibold text-lg mb-2">Resume Tailoring</h3>
            <p className="text-gray-600 text-sm">
              Get line-by-line suggestions specific to each job. Accept, reject, or modify each recommendation.
            </p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 className="font-semibold text-lg mb-2">Four-Level Match</h3>
            <p className="text-gray-600 text-sm">
              See how you match each requirement: Strong, Transferable, Addressable, or Fundamental gap.
            </p>
          </div>
          <div className="bg-white p-6 rounded-xl shadow-sm border">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <h3 className="font-semibold text-lg mb-2">Outcome Tracking</h3>
            <p className="text-gray-600 text-sm">
              Track every application. See your callback rate improve as you refine your approach.
            </p>
          </div>
        </div>
      </section>

      {/* Singapore-specific */}
      <section className="bg-gray-50 py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-2xl font-bold text-center mb-8">
            Built for Singapore
          </h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-3xl mx-auto">
            <div className="flex gap-4">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold mb-1">NS & GLC Context</h3>
                <p className="text-sm text-gray-600">
                  Smart framing advice for National Service, GLC vs MNC cultures, and local qualifications.
                </p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <div>
                <h3 className="font-semibold mb-1">PDPA Compliant</h3>
                <p className="text-sm text-gray-600">
                  Your data stays in Singapore. NRIC detection. Granular consent controls.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Preview */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-2xl font-bold text-center mb-8">
            Simple, transparent pricing
          </h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-2xl mx-auto">
            {/* Free */}
            <div className="bg-white p-6 rounded-xl border">
              <div className="text-sm font-medium text-gray-500 mb-2">Free</div>
              <div className="text-4xl font-bold text-gray-900 mb-4">
                $0<span className="text-lg font-normal text-gray-500">/month</span>
              </div>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start gap-2 text-sm">
                  <span className="text-match-strong">✓</span>
                  <span>3 job analyses per month</span>
                </li>
                <li className="flex items-start gap-2 text-sm">
                  <span className="text-match-strong">✓</span>
                  <span>Four-level match analysis</span>
                </li>
                <li className="flex items-start gap-2 text-sm">
                  <span className="text-match-strong">✓</span>
                  <span>Basic suggestions</span>
                </li>
              </ul>
              <Link
                href="/analyse"
                className="block w-full py-2 text-center border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Start free
              </Link>
            </div>

            {/* Pro */}
            <div className="bg-brand-50 p-6 rounded-xl border-2 border-brand-500">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-brand-700">Pro</span>
                <span className="text-xs bg-brand-500 text-white px-2 py-0.5 rounded">Recommended</span>
              </div>
              <div className="text-4xl font-bold text-gray-900 mb-4">
                SGD 19<span className="text-lg font-normal text-gray-500">/month</span>
              </div>
              <ul className="space-y-3 mb-6">
                <li className="flex items-start gap-2 text-sm">
                  <span className="text-match-strong">✓</span>
                  <span>Unlimited job analyses</span>
                </li>
                <li className="flex items-start gap-2 text-sm">
                  <span className="text-match-strong">✓</span>
                  <span>Export tailored resume (PDF/DOCX)</span>
                </li>
                <li className="flex items-start gap-2 text-sm">
                  <span className="text-match-strong">✓</span>
                  <span>Application tracking</span>
                </li>
                <li className="flex items-start gap-2 text-sm">
                  <span className="text-match-strong">✓</span>
                  <span>Singapore market insights</span>
                </li>
              </ul>
              <Link
                href="/pricing"
                className="block w-full py-2 text-center bg-brand-500 text-white rounded-lg hover:bg-brand-600 transition-colors"
              >
                Upgrade to Pro
              </Link>
            </div>
          </div>
          <p className="text-center text-sm text-gray-500 mt-6">
            Start free — no credit card required
          </p>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 bg-blue-600 rounded flex items-center justify-center">
                <span className="text-white font-bold text-xs">KS</span>
              </div>
              <span className="text-sm text-gray-500">KeyStone</span>
            </div>
            <nav className="flex gap-6 text-sm text-gray-500">
              <Link href="/privacy" className="hover:text-gray-700">Privacy</Link>
              <Link href="/terms" className="hover:text-gray-700">Terms</Link>
              <Link href="/trust" className="hover:text-gray-700">Trust</Link>
            </nav>
          </div>
        </div>
      </footer>
    </div>
  )
}
