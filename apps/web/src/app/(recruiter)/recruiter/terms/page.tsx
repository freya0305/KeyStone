'use client';

import Link from 'next/link';

export default function RecruiterTermsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">KS</span>
            </div>
            <span className="font-semibold text-xl">KeyStone</span>
            <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded">
              Recruiter
            </span>
          </Link>
          <Link href="/recruiter" className="text-sm text-gray-600 hover:text-gray-900">
            Dashboard
          </Link>
        </div>
      </header>

      <div className="container mx-auto px-4 py-16 max-w-3xl">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Recruiter Terms of Service</h1>

        <div className="prose prose-gray max-w-none space-y-8">
          {/* No AI Training */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">No AI Training</h2>
            <p className="text-gray-600">
              <strong>
                KeyStone will not use recruiter-uploaded Job Descriptions (JDs) or company data to
                train or improve AI models.
              </strong>{' '}
              Your JDs, company information, and any data you upload to KeyStone are used
              exclusively to provide and improve the KeyStone service for your organisation.
            </p>
            <p className="text-gray-600 mt-3">
              This commitment applies to all tiers of service, including free, Agency Team, Agency
              Pro, and Agency Enterprise plans.
            </p>
          </section>

          {/* PDPA Compliance */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">PDPA Compliance</h2>
            <p className="text-gray-600">
              KeyStone is committed to compliance with the Personal Data Protection Act 2012 (PDPA)
              of Singapore. We collect, use, and disclose personal data only as necessary to deliver
              the KeyStone service.
            </p>
            <ul className="list-disc pl-5 space-y-2 text-gray-600 mt-3">
              <li>
                We do not sell or share your personal data with third parties for marketing
                purposes.
              </li>
              <li>All personal data is stored on servers located in Singapore.</li>
              <li>
                You may request access to or correction of your personal data at any time by
                contacting{' '}
                <a href="mailto:support@keystone.com" className="text-blue-600 hover:underline">
                  support@keystone.com
                </a>
                .
              </li>
              <li>
                NRIC numbers and other national identification numbers are automatically detected
                and masked in all stored data.
              </li>
            </ul>
          </section>

          {/* Data Handling for Recruiters */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">
              Data Handling for Recruiters
            </h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>
                You retain full ownership of all Job Descriptions, company data, and hiring content
                you upload.
              </li>
              <li>
                KeyStone uses your uploaded JDs solely to generate and improve JD analysis and
                generation features within your organisation&apos;s account.
              </li>
              <li>
                Uploaded JDs are not shared with other organisations or accessible to job seeker
                users.
              </li>
              <li>
                You may delete your account and all associated data at any time via Settings &rarr;
                Delete Account. Data deletion is completed within 30 days of account closure.
              </li>
              <li>
                A backup of your data is retained for up to 90 days after account deletion for legal
                and regulatory compliance purposes.
              </li>
            </ul>
          </section>

          {/* Acceptable Use */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Acceptable Use</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>Do not upload false, misleading, or discriminatory job descriptions.</li>
              <li>
                Do not use KeyStone to process personal data outside the scope of recruitment
                activities.
              </li>
              <li>
                Do not attempt to extract or repurpose KeyStone-generated content for use outside
                the platform in a commercial manner that violates our intellectual property rights.
              </li>
              <li>
                You are responsible for ensuring that your use of KeyStone complies with all
                applicable employment laws and regulations in your jurisdiction.
              </li>
            </ul>
          </section>

          {/* Subscription */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Subscription</h2>
            <ul className="list-disc pl-5 space-y-2 text-gray-600">
              <li>Agency Team: SGD 79/month — 5 users, 100 JD generations/month</li>
              <li>Agency Pro: SGD 199/month — 10 users, 400 JD generations/month</li>
              <li>Agency Enterprise: SGD 449/month — unlimited users, unlimited JD generations</li>
              <li>Free tier: 10 JD generations/month, 1 user</li>
              <li>All prices exclude 9% GST.</li>
              <li>
                Cancel anytime via Settings &rarr; Manage subscription. Access is retained until the
                end of the billing period.
              </li>
            </ul>
          </section>

          {/* Refund Policy */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Refund Policy</h2>
            <p className="text-gray-600">
              We offer a 7-day money-back guarantee for new paid subscribers. If you are not
              satisfied with KeyStone within the first 7 days of your paid subscription, contact us
              at{' '}
              <a href="mailto:support@keystone.com" className="text-blue-600 hover:underline">
                support@keystone.com
              </a>{' '}
              for a full refund.
            </p>
            <ul className="list-disc pl-5 space-y-2 text-gray-600 mt-3">
              <li>Refunds are not provided for partial months after the 7-day guarantee period.</li>
              <li>No prorated refund is provided for unused time when cancelling mid-cycle.</li>
              <li>
                To request a refund within the guarantee period, email us within 7 days of your
                first payment.
              </li>
            </ul>
          </section>

          {/* Limitation of Liability */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Limitation of Liability</h2>
            <p className="text-gray-600">
              KeyStone is provided &ldquo;as is.&rdquo; We do not guarantee that JD suggestions will
              result in successful hires or any specific recruitment outcome.
            </p>
            <p className="text-gray-600 mt-3">
              We are not liable for decisions made based on KeyStone-generated content, including
              but not limited to hiring decisions, employment contracts, or compliance with
              employment laws.
            </p>
          </section>

          {/* Governing Law */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Governing Law</h2>
            <p className="text-gray-600">These terms are governed by the laws of Singapore.</p>
          </section>

          {/* Changes */}
          <section>
            <h2 className="text-xl font-semibold text-gray-900 mb-3">Changes</h2>
            <p className="text-gray-600">
              We may update these terms. Continued use of KeyStone after changes constitutes
              acceptance of the revised terms.
            </p>
          </section>
        </div>

        <div className="mt-12 pt-8 border-t">
          <Link href="/recruiter" className="text-blue-600 hover:underline">
            &larr; Back to Recruiter Dashboard
          </Link>
        </div>

        <p className="text-sm text-gray-400 mt-8">Last updated: May 2026</p>
      </div>
    </div>
  );
}
