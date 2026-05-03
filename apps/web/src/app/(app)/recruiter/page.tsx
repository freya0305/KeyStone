"use client";

import { useState, useEffect } from "react";
import { useAuth } from "@clerk/nextjs";
import Link from "next/link";
import { FileText, Link as LinkIcon, TrendingUp, ArrowRight } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { recruiterApi } from "@/lib/api-client";

export default function RecruiterDashboard() {
  const { getToken } = useAuth();
  const [stats, setStats] = useState({ total_jds: 0, share_links: 0, active_links: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchDashboard() {
      try {
        const token = await getToken();
        if (token) {
          const data = await recruiterApi.getDashboard(token);
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

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">Recruiter Dashboard</h1>
        <p className="text-slate-600 mt-1">Manage your job descriptions and team</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600">Job Descriptions</p>
                <p className="text-3xl font-bold text-slate-900 mt-1">{stats.total_jds}</p>
              </div>
              <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center">
                <FileText className="w-6 h-6 text-indigo-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600">Share Links</p>
                <p className="text-3xl font-bold text-slate-900 mt-1">{stats.share_links}</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
                <LinkIcon className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-slate-600">Active Links</p>
                <p className="text-3xl font-bold text-slate-900 mt-1">{stats.active_links}</p>
              </div>
              <div className="w-12 h-12 bg-amber-100 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-amber-600" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardContent className="pt-6">
            <h3 className="font-semibold text-slate-900 mb-2">Generate Job Description</h3>
            <p className="text-sm text-slate-600 mb-4">
              Create AI-powered job descriptions in seconds
            </p>
            <Button asChild>
              <Link href="/app/recruiter/jd" className="flex items-center gap-2">
                Create JD <ArrowRight className="w-4 h-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <h3 className="font-semibold text-slate-900 mb-2">Manage Team</h3>
            <p className="text-sm text-slate-600 mb-4">
              Invite team members to collaborate
            </p>
            <Button asChild variant="outline">
              <Link href="/app/recruiter/team" className="flex items-center gap-2">
                Manage Team <ArrowRight className="w-4 h-4" />
              </Link>
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
