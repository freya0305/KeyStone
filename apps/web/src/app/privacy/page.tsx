"use client"

import Link from "next/link"

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">KS</span>
            </div>
            <span className="font-semibold text-xl">KeyStone</span>
          </Link>
          <Link href="/sign-in" className="text-sm text-gray-600 hover:text-gray-900">
            Sign in
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-16 max-w-3xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Privacy Policy</h1>

        <div className="prose prose-gray max-w-none space-y-8">
          {/* Introduction */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Introduction</h2>
            <p className="text-gray-600">
              KeyStone is a resume tailoring service operated by KeyStone Pte. Ltd. (registered in Singapore).
              This Privacy Policy explains how we collect, use, and protect your personal data in accordance
              with Singapore&apos;s Personal Data Protection Act (PDPA) 2012.
            </p>
          </section>

          {/* Data We Collect */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Data We Collect</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li><strong>Account information</strong> — name, email address</li>
              <li><strong>Resume content</strong> — uploaded by you</li>
              <li><strong>Job descriptions</strong> — uploaded or pasted by you</li>
              <li><strong>Application tracking data</strong> — employers, roles, status</li>
              <li><strong>Consent preferences</strong> — your choices about how we use your data</li>
            </ul>
          </section>

          {/* How We Use Your Data */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">How We Use Your Data</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>Resume parsing and AI analysis</li>
              <li>Job description analysis</li>
              <li>Generating tailoring suggestions</li>
              <li>Application tracking and outcome logging</li>
              <li>Service improvement (aggregated, anonymized)</li>
            </ul>
          </section>

          {/* AI Processing */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">AI Processing</h2>
            <p className="text-gray-600">
              Your resume and job descriptions are sent to Anthropic&apos;s Claude API for analysis.
            </p>
            <p className="text-gray-600 mt-3">
              Anthropic is configured to retain zero data — your content is not stored or used for AI training.
            </p>
            <p className="text-gray-600 mt-3">
              All Claude API calls are processed in data centers located in Asia Pacific (Tokyo/Singapore).
            </p>
          </section>

          {/* Data Residency */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Data Residency</h2>
            <p className="text-gray-600">
              All personal data is stored on servers located in Singapore (AWS ap-southeast-1).
            </p>
            <p className="text-gray-600 mt-3">
              We do not transfer your personal data outside Singapore.
            </p>
          </section>

          {/* Data Retention */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Data Retention</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li><strong>Resume data</strong> — retained until you delete your account or request deletion</li>
              <li><strong>Application tracking data</strong> — retained for 2 years after last activity</li>
              <li><strong>AI processing logs</strong> — retained for 90 days</li>
            </ul>
          </section>

          {/* Your Rights */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Your Rights (PDPA)</h2>
            <p className="text-gray-600 mb-4">Under PDPA, you have the right to:</p>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>Access your personal data</li>
              <li>Correct inaccurate personal data</li>
              <li>Withdraw consent (where applicable)</li>
              <li>Request data export (Settings &rarr; Export all my data)</li>
              <li>Request deletion (Settings &rarr; Delete account)</li>
            </ul>
          </section>

          {/* Consent Types */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Consent Types We Collect</h2>
            <div className="space-y-3">
              {[
                { name: "Registration", required: true, desc: "Required to create and maintain your account." },
                { name: "Storage", required: true, desc: "Store your resume and application data so we can provide job matching services." },
                { name: "AI Processing", required: true, desc: "Send your resume and job descriptions to Claude API for analysis." },
                { name: "B2B Sharing", required: false, desc: "Allow recruiters to view anonymized application statistics (no personal data shared)." },
                { name: "Outcome Tracking", required: true, desc: "Track application outcomes to improve suggestions over time." },
                { name: "Marketing", required: false, desc: "Receive newsletters and promotional emails about KeyStone." },
                { name: "AI Training", required: false, desc: "Allow anonymized feedback to improve AI model performance." },
              ].map(consent => (
                <div key={consent.name} className="flex items-start gap-3">
                  <span className={`mt-0.5 w-5 h-5 rounded flex items-center justify-center flex-shrink-0 ${
                    consent.required ? "bg-blue-100 text-blue-600" : "bg-gray-100 text-gray-500"
                  }`}>
                    <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <div>
                    <span className="font-medium text-gray-900">{consent.name}</span>
                    {consent.required && (
                      <span className="ml-2 text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">Required</span>
                    )}
                    <p className="text-sm text-gray-500 mt-0.5">{consent.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* Cookies */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Cookies</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>We use <strong>essential cookies</strong> for authentication (Clerk).</li>
              <li>We use <strong>analytics cookies</strong> (PostHog) to understand how users navigate the service — no personal data is shared.</li>
              <li>We do <strong>not</strong> use advertising cookies.</li>
            </ul>
          </section>

          {/* Contact */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Contact</h2>
            <p className="text-gray-600">
              For PDPA-related requests:{" "}
              <a href="mailto:privacy@keystone.sg" className="text-blue-600 hover:underline">
                privacy@keystone.sg
              </a>
            </p>
            <p className="text-gray-600 mt-3">
              <strong>DPO:</strong> Data Protection Officer, KeyStone Pte. Ltd., Singapore
            </p>
          </section>
        </div>

        <div className="mt-12 pt-8 border-t">
          <Link href="/trust" className="text-blue-600 hover:underline">
            &larr; Back to Trust & Privacy
          </Link>
        </div>

        <p className="text-sm text-gray-400 mt-8">Last updated: May 2026</p>
      </div>
    </div>
  )
}
