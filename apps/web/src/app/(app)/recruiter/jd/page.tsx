"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { recruiterApi } from "@/lib/api-client";
import { Loader2, Copy, CheckCircle2 } from "lucide-react";

const SENIORITY_OPTIONS = ["junior", "mid", "senior", "lead"];

export default function JDGeneratorPage() {
  const { getToken } = useAuth();
  const [title, setTitle] = useState("");
  const [company, setCompany] = useState("");
  const [seniority, setSeniority] = useState("mid");
  const [skills, setSkills] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedJd, setGeneratedJd] = useState<string | null>(null);
  const [jdId, setJdId] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !company.trim() || !skills.trim()) return;

    setLoading(true);
    setError(null);
    setGeneratedJd(null);

    try {
      const token = await getToken();
      if (!token) throw new Error("Not authenticated");

      const data = await recruiterApi.generateJD(token, {
        title,
        company,
        seniority,
        skills: skills.split(",").map((s) => s.trim()).filter(Boolean),
      });
      setGeneratedJd(data.content);
      setJdId(data.jd_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Generation failed");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (generatedJd) {
      await navigator.clipboard.writeText(generatedJd);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">JD Generator</h1>
        <p className="text-slate-600 mt-1">
          Create professional job descriptions with AI
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle>Job Details</CardTitle>
            <CardDescription>
              Enter the details for your job description
            </CardDescription>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleGenerate} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="title">Job Title</Label>
                <Input
                  id="title"
                  placeholder="e.g., Senior Software Engineer"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="company">Company Name</Label>
                <Input
                  id="company"
                  placeholder="e.g., TechCorp Pte Ltd"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <Label>Seniority Level</Label>
                <div className="flex flex-wrap gap-2">
                  {SENIORITY_OPTIONS.map((level) => (
                    <button
                      key={level}
                      type="button"
                      onClick={() => setSeniority(level)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        seniority === level
                          ? "bg-indigo-600 text-white"
                          : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                      }`}
                    >
                      {level.charAt(0).toUpperCase() + level.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="skills">Required Skills</Label>
                <Input
                  id="skills"
                  placeholder="e.g., Python, AWS, Docker (comma separated)"
                  value={skills}
                  onChange={(e) => setSkills(e.target.value)}
                  required
                />
              </div>

              <Button type="submit" className="w-full" disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    Generating...
                  </>
                ) : (
                  "Generate JD"
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Generated JD */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <div>
              <CardTitle>Generated Description</CardTitle>
              <CardDescription>Your AI-generated job description</CardDescription>
            </div>
            {generatedJd && (
              <Button variant="outline" size="sm" onClick={handleCopy}>
                {copied ? (
                  <>
                    <CheckCircle2 className="w-4 h-4 mr-2" />
                    Copied
                  </>
                ) : (
                  <>
                    <Copy className="w-4 h-4 mr-2" />
                    Copy
                  </>
                )}
              </Button>
            )}
          </CardHeader>
          <CardContent>
            {generatedJd ? (
              <div className="prose prose-sm max-w-none">
                <pre className="whitespace-pre-wrap text-sm text-slate-700 font-sans bg-slate-50 p-4 rounded-lg border border-slate-200">
                  {generatedJd}
                </pre>
                {jdId && (
                  <div className="mt-4 flex items-center gap-2">
                    <Badge>ID: {jdId}</Badge>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-12 text-center">
                <div className="w-16 h-16 bg-slate-100 rounded-xl flex items-center justify-center mb-4">
                  <span className="text-3xl">📝</span>
                </div>
                <p className="text-slate-500">Generated job description will appear here</p>
                <p className="text-sm text-slate-400 mt-1">
                  Fill in the form and click Generate
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
