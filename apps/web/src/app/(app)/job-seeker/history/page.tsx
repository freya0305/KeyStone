"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { StatusPill } from "@/components/ui/status-pill";
import { jobSeekerApi } from "@/lib/api-client";
import { ExternalLink, Clock, FileText, Filter, ArrowRight } from "lucide-react";
import { clsx } from "clsx";

interface HistoryItem {
  id: string;
  job_title: string;
  company: string;
  job_url: string;
  match_score: number;
  match_level: string;
  status: "reviewed" | "pending" | "draft";
  created_at: string;
  suggestions_accepted: number;
  total_suggestions: number;
}

const TABS = ["All", "Reviewed", "Pending", "Draft"] as const;
type Tab = (typeof TABS)[number];

export default function HistoryPage() {
  const { getToken } = useAuth();
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<Tab>("All");

  useEffect(() => {
    async function fetchHistory() {
      try {
        const token = await getToken();
        if (token) {
          const data = await jobSeekerApi.getHistory(token);
          setHistory(data);
        }
      } catch (error) {
        console.error("Failed to fetch history:", error);
      } finally {
        setLoading(false);
      }
    }
    fetchHistory();
  }, [getToken]);

  const filteredHistory =
    activeTab === "All"
      ? history
      : history.filter((item) => item.status === activeTab.toLowerCase());

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analysis History</h1>
          <p className="text-gray-600 mt-1">View all your past job analyses</p>
        </div>
        <Button asChild>
          <Link href="/app/job-seeker/analyze">
            <FileText className="w-4 h-4 mr-2" />
            New Analysis
          </Link>
        </Button>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-1 border-b border-gray-200">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={clsx(
              "px-4 py-2.5 text-sm font-medium transition-colors relative",
              activeTab === tab
                ? "text-indigo-600"
                : "text-gray-500 hover:text-gray-700"
            )}
          >
            {tab}
            {activeTab === tab && (
              <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-indigo-600" />
            )}
            {tab !== "All" && (
              <span className="ml-1.5 text-xs text-gray-400">
                ({history.filter((h) => h.status === tab.toLowerCase()).length})
              </span>
            )}
          </button>
        ))}
      </div>

      {filteredHistory.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Clock className="w-12 h-12 text-gray-300 mb-4" />
            <p className="text-gray-500">
              {activeTab === "All" ? "No analyses yet" : `No ${activeTab.toLowerCase()} analyses`}
            </p>
            <p className="text-sm text-gray-400 mt-1">
              {activeTab === "All"
                ? "Start by analyzing a job posting"
                : `You have no analyses in ${activeTab.toLowerCase()} status`}
            </p>
          </CardContent>
        </Card>
      ) : (
        <Card className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200 bg-gray-50">
                  <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                    Job
                  </th>
                  <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                    Match
                  </th>
                  <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                    Suggestions
                  </th>
                  <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                    Status
                  </th>
                  <th className="text-left text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                    Date
                  </th>
                  <th className="text-right text-xs font-medium text-gray-500 uppercase tracking-wider px-6 py-3">
                    Action
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {filteredHistory.map((item) => (
                  <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                          <FileText className="w-5 h-5 text-indigo-600" />
                        </div>
                        <div>
                          <p className="font-medium text-gray-900">{item.job_title}</p>
                          <p className="text-sm text-gray-500">{item.company}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-2">
                        <div
                          className={clsx(
                            "text-lg font-bold",
                            item.match_score >= 75
                              ? "text-green-600"
                              : item.match_score >= 60
                              ? "text-amber-600"
                              : "text-red-600"
                          )}
                        >
                          {item.match_score}%
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <div className="text-sm">
                        <span className="font-medium text-gray-900">
                          {item.suggestions_accepted}
                        </span>
                        <span className="text-gray-400"> / {item.total_suggestions}</span>
                      </div>
                      <div className="w-24 h-1.5 bg-gray-200 rounded-full mt-1.5 overflow-hidden">
                        <div
                          className="h-full bg-green-500 rounded-full"
                          style={{
                            width: `${(item.suggestions_accepted / item.total_suggestions) * 100}%`,
                          }}
                        />
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <StatusPill
                        status={
                          item.status === "reviewed"
                            ? "good"
                            : item.status === "pending"
                            ? "review"
                            : "draft"
                        }
                        label={item.status.charAt(0).toUpperCase() + item.status.slice(1)}
                      />
                    </td>
                    <td className="px-6 py-4">
                      <p className="text-sm text-gray-500">
                        {new Date(item.created_at).toLocaleDateString("en-SG", {
                          year: "numeric",
                          month: "short",
                          day: "numeric",
                        })}
                      </p>
                      <p className="text-xs text-gray-400">
                        {new Date(item.created_at).toLocaleTimeString("en-SG", {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </p>
                    </td>
                    <td className="px-6 py-4 text-right">
                      <Button asChild variant="ghost" size="sm">
                        <Link href={`/app/job-seeker/analyze?analysis=${item.id}`}>
                          View <ArrowRight className="w-4 h-4 ml-1" />
                        </Link>
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      )}
    </div>
  );
}
