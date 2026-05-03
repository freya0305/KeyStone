"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { b2bApi } from "@/lib/api-client";
import { Loader2, Mail, Link as LinkIcon, Copy, CheckCircle2 } from "lucide-react";

export default function TeamPage() {
  const { getToken } = useAuth();
  const [email, setEmail] = useState("");
  const [accessLevel, setAccessLevel] = useState("MEMBER");
  const [loading, setLoading] = useState(false);
  const [inviteUrl, setInviteUrl] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleInvite = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return;

    setLoading(true);
    setError(null);
    setInviteUrl(null);

    try {
      const token = await getToken();
      if (!token) throw new Error("Not authenticated");

      const data = await b2bApi.generateInvite(token, { email, access_level: accessLevel });
      setInviteUrl(data.invite_url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to generate invite");
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = async () => {
    if (inviteUrl) {
      await navigator.clipboard.writeText(inviteUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Team Management</h1>
        <p className="text-slate-600 mt-1">Invite team members to your organization</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Invite Team Member</CardTitle>
          <CardDescription>
            Send an invitation link to add a new team member
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleInvite} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email Address</Label>
              <Input
                id="email"
                type="email"
                placeholder="colleague@company.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label>Access Level</Label>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => setAccessLevel("ADMIN")}
                  className={`flex-1 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    accessLevel === "ADMIN"
                      ? "bg-indigo-600 text-white"
                      : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }`}
                >
                  Admin
                </button>
                <button
                  type="button"
                  onClick={() => setAccessLevel("MEMBER")}
                  className={`flex-1 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    accessLevel === "MEMBER"
                      ? "bg-indigo-600 text-white"
                      : "bg-slate-100 text-slate-600 hover:bg-slate-200"
                  }`}
                >
                  Member
                </button>
              </div>
            </div>

            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin mr-2" />
                  Generating...
                </>
              ) : (
                <>
                  <Mail className="w-4 h-4 mr-2" />
                  Generate Invite Link
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>

      {inviteUrl && (
        <Card className="border-green-200 bg-green-50">
          <CardHeader>
            <CardTitle className="text-green-900 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5" />
              Invite Link Generated
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-sm text-green-700">
              Share this link with your team member. The link expires in 72 hours.
            </p>
            <div className="flex gap-2">
              <Input value={inviteUrl} readOnly className="bg-white" />
              <Button variant="outline" onClick={handleCopy}>
                {copied ? <CheckCircle2 className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="text-red-700 pt-6">{error}</CardContent>
        </Card>
      )}
    </div>
  );
}
