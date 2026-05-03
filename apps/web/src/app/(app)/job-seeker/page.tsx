"use client";

import { useAuth } from "@clerk/nextjs";
import { useState, useEffect } from "react";
import Link from "next/link";
import { clsx } from "clsx";
import { FileText, Upload, Plus, ArrowRight, CheckCircle2, Clock } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { StatusPill } from "@/components/ui/status-pill";
import { jobSeekerApi } from "@/lib/api-client";

interface RecentAnalysis {
  id: string;
  role: string;
  company: string;
  matchScore: number;
  suggestionsAccepted: number;
  totalSuggestions: number;
  status: "reviewed" | "pending" | "draft";
  analyzedAt: string;
}

const mockRecentAnalyses: RecentAnalysis[] = [
  {
    id: "1",
    role: "Senior Software Engineer",
    company: "DBS Bank",
    matchScore: 78,
    suggestionsAccepted: 5,
    totalSuggestions: 8,
    status: "reviewed",
    analyzedAt: "3 hours ago",
  },
  {
    id: "2",
    role: "Product Manager",
    company: "Grab",
    matchScore: 62,
    suggestionsAccepted: 3,
    totalSuggestions: 6,
    status: "pending",
    analyzedAt: "Yesterday",
  },
  {
    id: "3",
    role: "Data Scientist",
    company: "GovTech",
    matchScore: 81,
    suggestionsAccepted: 12,
    totalSuggestions: 14,
    status: "reviewed",
    analyzedAt: "2 days ago",
  },
];

export default function JobSeekerDashboard() {
  const { getToken, user } = useAuth();
  const [stats, setStats] = useState({ total_applications: 0, active_jobs: 0, matches: 0 });
  const [loading, setLoading] = useState(true);
  const [recentAnalyses] = useState<RecentAnalysis[]>(mockRecentAnalyses);

  useEffect(() => {
    async function fetchDashboard() {
      try {
        const token = await getToken();
        if (token) {
          const data = await jobSeekerApi.getDashboard(token);
          setStats(data);
        }
      } catch (error) {
        console.error("Failed to fetch dashboard:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchDashboard();
  }, [getToken]);

  const firstName = user?.firstName || "there";

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Welcome back, {firstName}</h1>
        <p className="text-gray-600 mt-1">Tailor your resume for each job application</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-5">
          <p className="text-sm text-gray-500">Resumes</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">3</p>
        </Card>

        <Card className="p-5">
          <p className="text-sm text-gray-500">Analyzed</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">12</p>
        </Card>

        <Card className="p-5">
          <p className="text-sm text-gray-500">Avg Match</p>
          <p className="text-2xl font-bold text-green-600 mt-1">72%</p>
        </Card>

        <Card className="p-5">
          <p className="text-sm text-gray-500">Free Analyses</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">8</p>
          <p className="text-xs text-indigo-600 mt-1">of 10 remaining</p>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Link
          href="/app/job-seeker/analyze"
          className="bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl p-6 flex items-center gap-4 transition shadow-lg shadow-indigo-200"
        >
          <div className="w-14 h-14 bg-white/20 rounded-xl flex items-center justify-center">
            <FileText className="w-8 h-8" />
          </div>
          <div className="text-left">
            <p className="font-semibold text-lg">Analyze My Resume</p>
            <p className="text-indigo-100 text-sm">Compare against any job posting</p>
          </div>
        </Link>

        <button className="bg-white hover:bg-gray-50 border-2 border-gray-200 rounded-xl p-6 flex items-center gap-4 transition text-left w-full">
          <div className="w-14 h-14 bg-amber-50 rounded-xl flex items-center justify-center">
            <Upload className="w-8 h-8 text-amber-600" />
          </div>
          <div>
            <p className="font-semibold text-lg text-gray-900">Upload Resume</p>
            <p className="text-gray-500 text-sm">Add a new resume version</p>
          </div>
        </button>
      </div>

      {/* Recent Analyses */}
      <Card className="overflow-hidden">
        <CardHeader className="border-b border-gray-200 flex-row justify-between items-center">
          <CardTitle>Recent Analyses</CardTitle>
          <Link href="/app/job-seeker/history" className="text-sm text-indigo-600 hover:text-indigo-700 font-medium">
            View All
          </Link>
        </CardHeader>
        <div className="divide-y divide-gray-100">
          {recentAnalyses.map((analysis) => (
            <Link
              key={analysis.id}
              href={`/app/job-seeker/analyze?analysis=${analysis.id}`}
              className="px-6 py-4 flex items-center gap-4 hover:bg-gray-50 transition cursor-pointer"
            >
              <div className="flex-1">
                <p className="font-medium text-gray-900">
                  {analysis.role} → {analysis.company}
                </p>
                <p className="text-sm text-gray-500 mt-0.5">Analyzed {analysis.analyzedAt}</p>
              </div>
              <div className="flex items-center gap-4">
                <div className="text-right">
                  <p className="text-sm font-semibold text-green-600">{analysis.matchScore}%</p>
                  <p className="text-xs text-gray-500">match</p>
                </div>
                <StatusPill
                  status={analysis.status === "reviewed" ? "good" : "review"}
                  label={analysis.status === "reviewed" ? "Reviewed" : "Pending"}
                />
              </div>
            </Link>
          ))}
        </div>
      </Card>

      {/* Activity Section */}
      <div>
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Your activity</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className="p-5">
            <p className="text-sm text-gray-500">Response rate</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">25%</p>
            <p className="text-xs text-gray-500 mt-1">1 / 4 applied</p>
          </Card>
          <Card className="p-5">
            <p className="text-sm text-gray-500">Suggestion accept rate</p>
            <p className="text-2xl font-bold text-gray-900 mt-1">78%</p>
            <p className="text-xs text-gray-500 mt-1">20 / 28 suggestions</p>
          </Card>
        </div>
      </div>
    </div>
  );
}
