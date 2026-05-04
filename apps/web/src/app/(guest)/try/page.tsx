import Link from "next/link"

export default function TryPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Simple Header */}
      <header className="border-b bg-white/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">KS</span>
            </div>
            <span className="font-semibold text-xl">KeyStone</span>
          </div>
          <Link href="/sign-in" className="text-sm text-gray-600 hover:text-gray-900">
            Sign in
          </Link>
        </div>
      </header>

      {/* Guest Flow */}
      <section className="container mx-auto px-4 py-16 max-w-2xl">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Try KeyStone for free
          </h1>
          <p className="text-gray-600">
            Upload your resume, paste a job description, and get personalized suggestions.
            No account required for your first try.
          </p>
        </div>

        {/* Step by Step */}
        <div className="space-y-6">
          <div className="bg-white border rounded-xl p-6">
            <div className="flex gap-4">
              <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
                1
              </div>
              <div className="flex-1">
                <h3 className="font-semibold mb-2">Paste a job description</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Copy from MyCareersFuture, JobStreet, or any job posting.
                </p>
                <textarea
                  className="w-full h-32 px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Paste job description here..."
                />
              </div>
            </div>
          </div>

          <div className="bg-white border rounded-xl p-6">
            <div className="flex gap-4">
              <div className="w-8 h-8 bg-gray-200 text-gray-600 rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
                2
              </div>
              <div className="flex-1">
                <h3 className="font-semibold mb-2">Upload your resume (optional)</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Get more accurate suggestions when we can see your actual experience.
                </p>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 cursor-pointer transition-colors">
                  <div className="text-gray-400 text-2xl mb-2">📄</div>
                  <p className="text-sm text-gray-600">Drop a PDF or DOCX, or click to browse</p>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white border rounded-xl p-6">
            <div className="flex gap-4">
              <div className="w-8 h-8 bg-gray-200 text-gray-600 rounded-full flex items-center justify-center flex-shrink-0 font-semibold">
                3
              </div>
              <div className="flex-1">
                <h3 className="font-semibold mb-2">Get AI suggestions</h3>
                <p className="text-sm text-gray-600">
                  See line-by-line suggestions tailored to this specific job.
                  Accept what resonates, modify what needs adjusting.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div className="mt-8 text-center">
          <Link
            href="/analyse"
            className="inline-block px-8 py-4 bg-brand-500 text-white text-lg rounded-lg hover:bg-brand-600 transition-colors"
          >
            Analyze my resume against this job →
          </Link>
          <p className="mt-4 text-sm text-gray-500">
            After 3 free suggestions, sign up to continue.
          </p>
        </div>
      </section>
    </div>
  )
}
