"use client"

import Link from "next/link"

export default function TermsPage() {
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
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Terms of Service</h1>

        <div className="prose prose-gray max-w-none space-y-8">
          {/* Agreement */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Agreement</h2>
            <p className="text-gray-600">
              By using KeyStone, you agree to these Terms of Service.
            </p>
          </section>

          {/* Use of Service */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Use of Service</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>You must be 18 years or older to use KeyStone.</li>
              <li>You are responsible for keeping your account credentials secure.</li>
              <li>You agree not to use KeyStone for any illegal purposes.</li>
            </ul>
          </section>

          {/* AI-Generated Content */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">AI-Generated Content</h2>
            <p className="text-gray-600">
              KeyStone provides AI-generated resume suggestions. These are tools to assist your job search,
              not professional career advice.
            </p>
            <p className="text-gray-600 mt-3">
              We do not guarantee that AI suggestions will result in job interviews or offers.
            </p>
            <p className="text-gray-600 mt-3">
              You are responsible for reviewing and approving any resume changes before submission.
            </p>
          </section>

          {/* Your Content */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Your Content</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>You retain all rights to your resume and application data.</li>
              <li>You grant us a limited license to process your data for the purpose of providing the KeyStone service.</li>
              <li>We do not claim ownership of your resume content.</li>
            </ul>
          </section>

          {/* Acceptable Use */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Acceptable Use</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>Do not upload false, misleading, or fraudulent information.</li>
              <li>Do not use KeyStone to spam employers.</li>
              <li>Do not attempt to extract AI-generated content for use outside the platform in a commercial manner.</li>
            </ul>
          </section>

          {/* Limitation of Liability */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Limitation of Liability</h2>
            <p className="text-gray-600">
              KeyStone is provided &ldquo;as is.&rdquo; We do not guarantee job placement or specific outcomes.
            </p>
            <p className="text-gray-600 mt-3">
              We are not liable for decisions made based on AI suggestions.
            </p>
          </section>

          {/* Subscription */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Subscription</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>Pro subscriptions are billed monthly (SGD 19/month) or annually (SGD 190/year).</li>
              <li>Cancel anytime via Settings &rarr; Manage subscription.</li>
              <li>Refunds are not provided for partial months.</li>
            </ul>
          </section>

          {/* Governing Law */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Governing Law</h2>
            <p className="text-gray-600">
              These terms are governed by the laws of Singapore.
            </p>
          </section>

          {/* Changes */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Changes</h2>
            <p className="text-gray-600">
              We may update these terms. Continued use after changes constitutes acceptance.
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
