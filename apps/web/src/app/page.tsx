"use client";

import { useState } from "react";
import Link from "next/link";
import {
  FileText,
  Users,
  TrendingUp,
  Shield,
  CheckCircle,
  ArrowRight,
  Sparkles,
} from "lucide-react";

export default function LandingPage() {
  const [product, setProduct] = useState<"seeker" | "recruiter">("seeker");

  return (
    <div className="min-h-screen bg-gradient-to-b from-teal-50 to-white">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                  <FileText className="w-5 h-5 text-white" />
                </div>
                <span className="font-bold text-xl text-gray-900">KeyStone</span>
              </div>

              {/* Product Switcher */}
              <div className="product-switch">
                <button
                  onClick={() => setProduct("seeker")}
                  className={`product-btn ${product === "seeker" ? "active" : "inactive"}`}
                >
                  <span className="hidden sm:inline">For Job Seekers</span>
                  <span className="sm:hidden">Seeker</span>
                </button>
                <button
                  onClick={() => setProduct("recruiter")}
                  className={`product-btn ${product === "recruiter" ? "active" : "inactive"}`}
                >
                  <span className="hidden sm:inline">For Recruiters</span>
                  <span className="sm:hidden">Recruiter</span>
                </button>
              </div>
            </div>

            <div className="flex items-center gap-4">
              <Link
                href="/sign-in"
                className="text-sm font-medium text-gray-600 hover:text-gray-900 px-3 py-2"
              >
                Sign In
              </Link>
              <Link
                href="/sign-up"
                className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 bg-indigo-100 text-indigo-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
            <Sparkles className="w-4 h-4" />
            Built for Singapore Job Market
          </div>
          <h1 className="text-5xl font-bold text-gray-900 mb-6 leading-tight">
            {product === "seeker" ? (
              <>
                Land Your Dream Job with
                <span className="text-indigo-600"> AI-Powered</span> Resume Tailoring
              </>
            ) : (
              <>
                Create Professional Job Descriptions
                <span className="text-indigo-600"> 10x Faster</span>
              </>
            )}
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            {product === "seeker"
              ? "Paste a job posting. Get a resume tailored for that role, that company, this market. In under a minute."
              : "Generate polished, comprehensive job descriptions that attract the right candidates. Powered by AI trained on Singapore hiring data."}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href={product === "seeker" ? "/app" : "/recruiter"}
              className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-4 rounded-xl transition flex items-center justify-center gap-2 shadow-lg shadow-indigo-200"
            >
              {product === "seeker" ? "Start Analyzing Resumes" : "Create Your First JD"}
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/demo"
              className="bg-white hover:bg-gray-50 text-gray-700 font-semibold px-8 py-4 rounded-xl border-2 border-gray-200 transition"
            >
              Watch Demo
            </Link>
          </div>
        </div>

        {/* Preview Card */}
        <div className="mt-16 bg-white rounded-2xl shadow-xl shadow-gray-200/50 overflow-hidden border border-gray-200">
          <div className="bg-gradient-to-r from-indigo-600 to-teal-600 px-8 py-4">
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-red-400" />
              <div className="w-3 h-3 rounded-full bg-amber-400" />
              <div className="w-3 h-3 rounded-full bg-green-400" />
            </div>
          </div>
          <div className="p-8 bg-gradient-to-b from-gray-50 to-white">
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <div className="bg-white rounded-xl p-6 border border-gray-200 mb-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="font-semibold text-gray-900">Match Score</h3>
                    <span className="text-3xl font-bold text-green-600">78%</span>
                  </div>
                  <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div className="h-full bg-green-500 rounded-full" style={{ width: "78%" }} />
                  </div>
                </div>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
                    <span className="text-gray-700">Python</span>
                    <span className="text-green-700 font-medium text-sm">Strong Match</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-amber-50 rounded-lg border border-amber-200">
                    <span className="text-gray-700">AWS</span>
                    <span className="text-amber-700 font-medium text-sm">Medium Match</span>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-red-50 rounded-lg border border-red-200">
                    <span className="text-gray-700">Machine Learning</span>
                    <span className="text-red-700 font-medium text-sm">Missing</span>
                  </div>
                </div>
              </div>
              <div className="space-y-4">
                <div className="bg-amber-50 rounded-xl p-5 border border-amber-200">
                  <div className="flex items-start gap-3">
                    <span className="text-amber-500 mt-0.5">💡</span>
                    <div>
                      <p className="font-medium text-gray-900">Add &quot;Machine Learning&quot; to Skills</p>
                      <p className="text-sm text-gray-600 mt-1">
                        This keyword appears 3 times in the JD but is missing from your resume.
                      </p>
                    </div>
                  </div>
                </div>
                <div className="bg-amber-50 rounded-xl p-5 border border-amber-200">
                  <div className="flex items-start gap-3">
                    <span className="text-amber-500 mt-0.5">💡</span>
                    <div>
                      <p className="font-medium text-gray-900">Quantify your leadership</p>
                      <p className="text-sm text-gray-600 mt-1">
                        The JD emphasizes leadership at scale. Add numbers to your impact.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Everything you need to land the job
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 rounded-xl border border-gray-200 hover:border-indigo-200 hover:shadow-md transition">
              <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mb-4">
                <TrendingUp className="w-6 h-6 text-indigo-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">AI-Powered Matching</h3>
              <p className="text-gray-600">
                Get instant match scores and actionable suggestions calibrated on Singapore hiring data.
              </p>
            </div>
            <div className="p-6 rounded-xl border border-gray-200 hover:border-indigo-200 hover:shadow-md transition">
              <div className="w-12 h-12 bg-teal-100 rounded-xl flex items-center justify-center mb-4">
                <FileText className="w-6 h-6 text-teal-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Smart Suggestions</h3>
              <p className="text-gray-600">
                Line-by-line recommendations to tailor your resume for each application.
              </p>
            </div>
            <div className="p-6 rounded-xl border border-gray-200 hover:border-indigo-200 hover:shadow-md transition">
              <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center mb-4">
                <CheckCircle className="w-6 h-6 text-amber-600" />
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Outcome Tracking</h3>
              <p className="text-gray-600">
                Track your applications through every stage and learn what works.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* For Recruiters */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 mb-6">
                For Recruiters: Create JDs That Convert
              </h2>
              <ul className="space-y-4">
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-600">
                    AI-generated job descriptions in seconds, not hours
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-600">
                    Templates customized for Singapore market
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-600">
                    Track views and engagement on your listings
                  </span>
                </li>
                <li className="flex items-start gap-3">
                  <CheckCircle className="w-6 h-6 text-green-500 flex-shrink-0 mt-0.5" />
                  <span className="text-gray-600">
                    Maintain consistency across your hiring pipeline
                  </span>
                </li>
              </ul>
              <Link
                href="/recruiter"
                className="inline-flex items-center gap-2 text-indigo-600 font-semibold mt-6 hover:text-indigo-700"
              >
                Try JD Generator <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Job Title</label>
                  <input
                    type="text"
                    value="Senior Software Engineer"
                    className="w-full px-4 py-2.5 border border-gray-300 rounded-lg bg-gray-50"
                    readOnly
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Company</label>
                  <input
                    type="text"
                    value="TechCorp Pte Ltd"
                    className="w-full px-4 py-2.5 border border-gray-300 rounded-lg bg-gray-50"
                    readOnly
                  />
                </div>
                <div className="flex flex-wrap gap-2">
                  <span className="px-3 py-1 rounded-full text-sm bg-indigo-50 text-indigo-700">Python</span>
                  <span className="px-3 py-1 rounded-full text-sm bg-indigo-50 text-indigo-700">AWS</span>
                  <span className="px-3 py-1 rounded-full text-sm bg-indigo-50 text-indigo-700">Docker</span>
                </div>
                <div className="pt-4 border-t border-gray-200">
                  <p className="text-sm text-gray-500">Preview generated in 1.2s</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap justify-center gap-8 items-center text-gray-400">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5" />
              <span className="text-sm">PDPA Compliant</span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              <span className="text-sm">Built for Singapore</span>
            </div>
            <div className="flex items-center gap-2">
              <CheckCircle className="w-5 h-5" />
              <span className="text-sm">Data stays in Singapore</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-gray-900">KeyStone</span>
            </div>
            <p className="text-sm text-gray-500">
              © 2026 KeyStone. Built for Singapore job seekers.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
