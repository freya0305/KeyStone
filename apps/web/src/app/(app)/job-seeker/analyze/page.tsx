"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { jobSeekerApi } from "@/lib/api-client";
import { Loader2, AlertCircle, CheckCircle2 } from "lucide-react";

export default function AnalyzeJobPage() {
  const { getToken } = useAuth();
  const [jobUrl, setJobUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ analysis_id: string; match_level: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!jobUrl.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const token = await getToken();
      if (!token) throw new Error("Not authenticated");

      const data = await jobSeekerApi.analyzeJob(token, { job_url: jobUrl });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Analyze Job Posting</h1>
        <p className="text-slate-600 mt-1">
          Paste a job posting URL to get AI-powered resume suggestions
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Job URL</CardTitle>
          <CardDescription>
            Enter a job posting URL from LinkedIn, JobsDB, or any other job site
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="job-url">Job Posting URL</Label>
              <Input
                id="job-url"
                type="url"
                placeholder="https://www.linkedin.com/jobs/..."
                value={jobUrl}
                onChange={(e) => setJobUrl(e.target.value)}
                required
              />
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin mr-2" />
                  Analyzing...
                </>
              ) : (
                "Analyze Job"
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="flex items-center gap-3 pt-6">
            <AlertCircle className="w-5 h-5 text-red-600" />
            <p className="text-red-700">{error}</p>
          </CardContent>
        </Card>
      )}

      {result && (
        <Card className="border-green-200 bg-green-50">
          <CardContent className="flex items-center gap-3 pt-6">
            <CheckCircle2 className="w-5 h-5 text-green-600" />
            <div>
              <p className="font-medium text-green-900">Analysis Complete</p>
              <p className="text-sm text-green-700">
                Match level: <span className="font-semibold">{result.match_level}</span>
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
