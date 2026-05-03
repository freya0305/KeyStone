"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { jobSeekerApi } from "@/lib/api-client";
import { ExternalLink, Clock } from "lucide-react";

export default function HistoryPage() {
  const { getToken } = useAuth();
  const [history, setHistory] = useState<Array<{ id: string; job_url: string; created_at: string; match_level: string }>>([]);
  const [loading, setLoading] = useState(true);

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

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Analysis History</h1>
        <p className="text-slate-600 mt-1">View all your past job analyses</p>
      </div>

      {history.length === 0 ? (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <Clock className="w-12 h-12 text-slate-300 mb-4" />
            <p className="text-slate-500">No analyses yet</p>
            <p className="text-sm text-slate-400 mt-1">
              Start by analyzing a job posting
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-4">
          {history.map((item) => (
            <Card key={item.id}>
              <CardContent className="flex items-center justify-between py-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3">
                    <a
                      href={item.job_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm font-medium text-indigo-600 hover:text-indigo-700 truncate flex items-center gap-1"
                    >
                      <ExternalLink className="w-4 h-4 flex-shrink-0" />
                      {item.job_url}
                    </a>
                    <Badge
                      variant={
                        item.match_level === "strong"
                          ? "success"
                          : item.match_level === "transferable"
                          ? "warning"
                          : "default"
                      }
                    >
                      {item.match_level}
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">
                    {new Date(item.created_at).toLocaleDateString("en-SG", {
                      year: "numeric",
                      month: "short",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
