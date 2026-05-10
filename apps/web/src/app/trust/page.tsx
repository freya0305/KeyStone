import Link from 'next/link';

export default function TrustPage() {
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
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Privacy & Trust</h1>

        <div className="prose prose-gray max-w-none space-y-8">
          {/* PDPA */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">PDPA Compliant</h2>
            <p className="text-gray-600">
              KeyStone is fully compliant with Singapore&apos;s Personal Data Protection Act (PDPA).
              We are committed to protecting your personal data and being transparent about how we
              collect, use, and store your information.
            </p>
            <p className="text-gray-600 mt-3">
              For data protection inquiries, contact our Data Protection Officer at{' '}
              <a href="mailto:dpo@keystone.com" className="text-blue-600 hover:underline">
                dpo@keystone.com
              </a>
              .
            </p>
          </section>

          {/* Data Storage */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Data Storage in Singapore</h2>
            <p className="text-gray-600">
              All resume and application data is stored on servers located in Singapore. Your data
              never leaves Singapore unless you explicitly consent to processing for AI analysis, in
              which case it is sent to Anthropic&apos;s Claude API and is not retained by them.
            </p>
          </section>

          {/* NRIC Protection */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">NRIC Protection</h2>
            <p className="text-gray-600">
              KeyStone automatically detects and masks Singapore NRIC numbers (and FIN numbers) in
              all uploaded documents. This happens before any AI processing, ensuring your identity
              numbers are never exposed to AI models or stored in plain text.
            </p>
          </section>

          {/* Consent */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Your Consent</h2>
            <p className="text-gray-600 mb-4">
              Under PDPA, you have full control over your data. KeyStone requires your consent for
              the following purposes:
            </p>
            <div className="space-y-3">
              {[
                {
                  name: 'Account Registration',
                  required: true,
                  desc: 'Required to create and maintain your account.',
                },
                {
                  name: 'Resume & Application Storage',
                  required: true,
                  desc: 'Store your data so we can provide job matching services.',
                },
                {
                  name: 'AI Processing',
                  required: true,
                  desc: 'Send to Claude API for resume and job analysis.',
                },
                {
                  name: 'Application Outcome Tracking',
                  required: true,
                  desc: 'Track outcomes to improve suggestions over time.',
                },
                {
                  name: 'Marketing Communications',
                  required: false,
                  desc: 'Receive newsletters and promotional emails.',
                },
                {
                  name: 'AI Model Improvement',
                  required: false,
                  desc: 'Allow anonymized feedback for model training.',
                },
              ].map((consent) => (
                <div key={consent.name} className="flex items-start gap-3">
                  <span
                    className={`mt-0.5 w-5 h-5 rounded flex items-center justify-center flex-shrink-0 ${
                      consent.required ? 'bg-blue-100 text-blue-600' : 'bg-gray-100 text-gray-500'
                    }`}
                  >
                    {consent.required ? (
                      <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                        <path
                          fillRule="evenodd"
                          d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                          clipRule="evenodd"
                        />
                      </svg>
                    ) : (
                      <span className="text-xs">{consent.required ? '✓' : '○'}</span>
                    )}
                  </span>
                  <div>
                    <span className="font-medium text-gray-900">{consent.name}</span>
                    {consent.required && (
                      <span className="ml-2 text-xs bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">
                        Required
                      </span>
                    )}
                    <p className="text-sm text-gray-500 mt-0.5">{consent.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </section>

          {/* AI Data */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">AI Data Handling</h2>
            <p className="text-gray-600">
              When you use AI features (resume analysis, job matching, JD generation), your data is
              sent to Anthropic&apos;s Claude API. KeyStone has a Data Processing Agreement with
              Anthropic that ensures:
            </p>
            <ul className="list-disc pl-5 mt-3 space-y-1 text-gray-600">
              <li>Your data is not used to train AI models</li>
              <li>Your data is not retained by Anthropic after processing</li>
              <li>All data is encrypted in transit (TLS)</li>
            </ul>
          </section>

          {/* Contact */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Contact Us</h2>
            <p className="text-gray-600">
              For privacy-related questions or to exercise your PDPA rights (access, correction,
              withdrawal of consent), contact our Data Protection Officer at{' '}
              <a href="mailto:privacy@keystone.sg" className="text-blue-600 hover:underline">
                privacy@keystone.sg
              </a>
              .
            </p>
          </section>
        </div>

        <div className="mt-12 pt-8 border-t">
          <Link href="/pricing" className="text-blue-600 hover:underline">
            ← Back to Pricing
          </Link>
        </div>
      </div>
    </div>
  );
}
