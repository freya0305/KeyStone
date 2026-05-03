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
  Zap,
  Lock,
  Brain,
} from "lucide-react";

export default function LandingPage() {
  const [product, setProduct] = useState<"seeker">("seeker");

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="fixed top-0 w-full bg-white/80 backdrop-blur-md border-b border-gray-200 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-xl text-gray-900">KeyStone</span>
            </div>
            <div className="flex items-center gap-6">
              <a href="#features" className="text-sm text-gray-600 hover:text-gray-900">Features</a>
              <a href="#pricing" className="text-sm text-gray-600 hover:text-gray-900">Pricing</a>
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
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 bg-indigo-100 text-indigo-700 px-4 py-1.5 rounded-full text-sm font-medium mb-6">
            <Sparkles className="w-4 h-4" />
            Singapore&apos;s First AI Resume Optimization Platform
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight mb-6">
            Let <span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 bg-clip-text text-transparent">Every Resume</span>
            <br />Precisely Hit Your Target Role
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            KeyStone uses AI to analyze your resume against job descriptions, providing targeted suggestions to help you stand out in Singapore&apos;s job market.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/app"
              className="px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition shadow-lg shadow-indigo-200 flex items-center justify-center gap-2"
            >
              Get Started Free
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/demo"
              className="px-8 py-4 bg-white hover:bg-gray-50 text-gray-900 font-semibold rounded-xl border-2 border-gray-200 transition flex items-center justify-center gap-2"
            >
              Watch Demo
            </Link>
          </div>
        </div>
      </section>

      {/* Role Selection Cards */}
      <section className="pb-20 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="grid md:grid-cols-1 gap-8 max-w-2xl mx-auto">
            {/* Job Seeker Card */}
            <div className="group bg-white rounded-2xl p-8 border-2 border-gray-200 hover:border-indigo-300 transition text-left hover:shadow-xl hover:-translate-y-1">
              <div className="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition">
                <Users className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">Job Seeker</h3>
              <p className="text-gray-600 mb-6">Paste any job URL, AI analyzes your resume match, and provides targeted improvement suggestions</p>
              <ul className="space-y-3 text-sm text-gray-600">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  Smart job URL analysis
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  Skills match evaluation
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  Personalized suggestions
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Why Choose KeyStone?</h2>
            <p className="text-gray-600 text-lg">AI solutions built for Singapore&apos;s job market</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 rounded-xl border border-gray-200 hover:border-indigo-200 hover:shadow-lg transition">
              <div className="w-16 h-16 bg-indigo-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Zap className="w-8 h-8 text-indigo-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Lightning Fast</h3>
              <p className="text-gray-600">Get in-depth resume-job analysis in 30 seconds with instant match reports</p>
            </div>
            <div className="text-center p-6 rounded-xl border border-gray-200 hover:border-green-200 hover:shadow-lg transition">
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Lock className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">Privacy Protected</h3>
              <p className="text-gray-600">Your resume data stored in Singapore data centers, PDPA compliant</p>
            </div>
            <div className="text-center p-6 rounded-xl border border-gray-200 hover:border-purple-200 hover:shadow-lg transition">
              <div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Brain className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">AI-Powered</h3>
              <p className="text-gray-600">Powered by Claude, continuously learning latest hiring trends</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">Simple, Transparent Pricing</h2>
            <p className="text-gray-600 text-lg">Start free, upgrade as needed</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Free */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:-translate-y-2 transition">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Free</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">$0</span>
                <span className="text-gray-500">/month</span>
              </div>
              <p className="text-gray-600 mb-6">Perfect for job seekers getting started</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  3 job analyses per month
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  Basic match scoring
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  Application history tracking
                </li>
              </ul>
              <button className="w-full py-3 border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 transition">
                Get Started Free
              </button>
            </div>

            {/* Basic */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:-translate-y-2 transition">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Basic</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">SGD 9</span>
                <span className="text-gray-500">/month</span>
              </div>
              <p className="text-gray-600 mb-6">For active job seekers</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  20 job analyses per month
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  Detailed skills analysis
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  Resume improvement tips
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  Priority email support
                </li>
              </ul>
              <button className="w-full py-3 border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 transition">
                Upgrade to Basic
              </button>
            </div>

            {/* Pro */}
            <div className="bg-white rounded-2xl p-8 border-2 border-indigo-600 relative hover:-translate-y-2 transition">
              <div className="absolute top-0 right-0 bg-indigo-600 text-white text-xs font-semibold px-3 py-1 rounded-bl-lg">Most Popular</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Pro</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">SGD 12</span>
                <span className="text-gray-500">/month</span>
              </div>
              <p className="text-gray-600 mb-6">For serious professionals</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  Unlimited job analyses
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  Detailed skills analysis
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  Resume improvement tips
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  Priority support
                </li>
              </ul>
              <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition">
                Upgrade to Pro
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="bg-gray-100 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap justify-center gap-8 items-center text-gray-500">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5" />
              <span className="text-sm">PDPA Compliant</span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              <span className="text-sm">Built for Singapore</span>
            </div>
            <div className="flex items-center gap-2">
              <Lock className="w-5 h-5" />
              <span className="text-sm">Data Stays in Singapore</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-gradient-to-br from-indigo-600 to-purple-600 rounded-lg flex items-center justify-center">
                <FileText className="w-5 h-5 text-white" />
              </div>
              <span className="font-bold text-lg">KeyStone</span>
            </div>
            <div className="flex gap-8 text-sm text-gray-400">
              <a href="#" className="hover:text-white transition">About Us</a>
              <a href="#" className="hover:text-white transition">Privacy Policy</a>
              <a href="#" className="hover:text-white transition">Terms of Service</a>
              <a href="#" className="hover:text-white transition">Contact</a>
            </div>
            <p className="text-sm text-gray-500">&copy; 2026 KeyStone. Made in Singapore.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
