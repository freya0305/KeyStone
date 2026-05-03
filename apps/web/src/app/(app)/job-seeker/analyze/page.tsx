"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import { useSearchParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { MatchScore } from "@/components/ui/match-score";
import { jobSeekerApi } from "@/lib/api-client";
import { Loader2, AlertCircle, CheckCircle2, Plus, Minus, ArrowRight, FileText } from "lucide-react";
import Link from "next/link";

interface Suggestion {
  id: string;
  type: "add" | "remove" | "modify";
  category: string;
  original: string;
  suggested: string;
  reason: string;
  accepted?: boolean;
}

interface AnalysisResult {
  analysis_id: string;
  match_score: number;
  match_level: string;
  job_title: string;
  company: string;
  missing_skills: string[];
  matching_skills: string[];
  suggestions: Suggestion[];
  analyzed_at: string;
}

export default function AnalyzeJobPage() {
  const { getToken } = useAuth();
  const searchParams = useSearchParams();
  const [jobUrl, setJobUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);

  useEffect(() => {
    const analysisId = searchParams.get("analysis");
    if (analysisId) {
      loadAnalysis(analysisId);
    }
  }, [searchParams]);

  async function loadAnalysis(analysisId: string) {
    setLoading(true);
    try {
      const token = await getToken();
      if (!token) throw new Error("Not authenticated");
      const data = await jobSeekerApi.getAnalysis(token, analysisId);
      setResult(data);
      setSuggestions(data.suggestions || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load analysis");
    } finally {
      setLoading(false);
    }
  }

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
      setSuggestions(data.suggestions || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  const toggleSuggestion = (id: string) => {
    setSuggestions((prev) =>
      prev.map((s) => (s.id === id ? { ...s, accepted: !s.accepted } : s))
    );
  };

  const acceptedCount = suggestions.filter((s) => s.accepted).length;

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Analyze Job Posting</h1>
        <p className="text-gray-600 mt-1">
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
        <div className="space-y-6">
          {/* Match Score Card */}
          <Card>
            <CardContent className="pt-6">
              <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
                <MatchScore
                  score={result.match_score}
                  size="lg"
                  label={result.match_level === "good" ? "Good Match" : result.match_level === "review" ? "Needs Review" : "Low Match"}
                  description={`${result.job_title} at ${result.company}`}
                />
                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <FileText className="w-4 h-4" />
                    <span>Analyzed {result.analyzed_at}</span>
                  </div>
                  <div className="flex gap-2">
                    <Badge variant="outline">{result.job_title}</Badge>
                    <Badge variant="outline">{result.company}</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Skills Analysis */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-base">Matching Skills</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {result.matching_skills.map((skill) => (
                    <Badge key={skill} className="bg-green-100 text-green-700 hover:bg-green-100">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-base">Missing Skills</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {result.missing_skills.map((skill) => (
                    <Badge key={skill} className="bg-amber-100 text-amber-700 hover:bg-amber-100">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Suggestions */}
          <Card>
            <CardHeader className="flex-row justify-between items-center">
              <div>
                <CardTitle>Resume Suggestions</CardTitle>
                <CardDescription>
                  {acceptedCount} of {suggestions.length} suggestions accepted
                </CardDescription>
              </div>
              <Button asChild>
                <Link href={`/app/job-seeker/history?analysis=${result.analysis_id}`}>
                  View History <ArrowRight className="w-4 h-4 ml-2" />
                </Link>
              </Button>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {suggestions.map((suggestion) => (
                  <div
                    key={suggestion.id}
                    className={`p-4 rounded-xl border-2 transition-all ${
                      suggestion.accepted
                        ? "border-green-200 bg-green-50"
                        : "border-gray-200 bg-white hover:border-gray-300"
                    }`}
                  >
                    <div className="flex items-start gap-4">
                      <button
                        onClick={() => toggleSuggestion(suggestion.id)}
                        className={`mt-1 w-6 h-6 rounded-md flex items-center justify-center transition-colors ${
                          suggestion.accepted
                            ? "bg-green-500 text-white"
                            : "bg-gray-100 text-gray-400 hover:bg-gray-200"
                        }`}
                      >
                        {suggestion.accepted ? (
                          <CheckCircle2 className="w-4 h-4" />
                        ) : (
                          <Plus className="w-4 h-4" />
                        )}
                      </button>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1">
                          <Badge
                            variant="outline"
                            className={`text-xs ${
                              suggestion.type === "add"
                                ? "border-green-300 text-green-600"
                                : suggestion.type === "remove"
                                ? "border-red-300 text-red-600"
                                : "border-amber-300 text-amber-600"
                            }`}
                          >
                            {suggestion.type === "add"
                              ? "Add"
                              : suggestion.type === "remove"
                              ? "Remove"
                              : "Modify"}{" "}
                            {suggestion.category}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{suggestion.reason}</p>
                        <div className="flex items-center gap-2 text-sm">
                          {suggestion.type !== "add" && (
                            <span className="text-gray-400 line-through">{suggestion.original}</span>
                          )}
                          {suggestion.type !== "remove" && (
                            <ArrowRight className="w-3 h-3 text-gray-400" />
                          )}
                          {suggestion.type !== "remove" && (
                            <span className="text-gray-900 font-medium">{suggestion.suggested}</span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
