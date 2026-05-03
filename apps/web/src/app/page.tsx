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
  const [product, setProduct] = useState<"seeker" | "recruiter">("seeker");

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
              <a href="#features" className="text-sm text-gray-600 hover:text-gray-900">功能</a>
              <a href="#pricing" className="text-sm text-gray-600 hover:text-gray-900">定价</a>
              <Link
                href="/sign-in"
                className="text-sm font-medium text-gray-600 hover:text-gray-900 px-3 py-2"
              >
                登入
              </Link>
              <Link
                href="/sign-up"
                className="bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition"
              >
                开始使用
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
            新加坡首个AI简历优化平台
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 leading-tight mb-6">
            让<span className="bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-500 bg-clip-text text-transparent">每一份简历</span>
            <br />精准击中目标职位
          </h1>
          <p className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            KeyStone运用人工智能技术，自动分析你的简历与职位描述的匹配度，提供针对性优化建议，助你在新加坡就业市场脱颖而出。
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href={product === "seeker" ? "/app" : "/recruiter"}
              className="px-8 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition shadow-lg shadow-indigo-200 flex items-center justify-center gap-2"
            >
              {product === "seeker" ? "求职者入口" : "招聘者入口"}
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              href="/demo"
              className="px-8 py-4 bg-white hover:bg-gray-50 text-gray-900 font-semibold rounded-xl border-2 border-gray-200 transition flex items-center justify-center gap-2"
            >
              观看演示
            </Link>
          </div>
        </div>
      </section>

      {/* Role Selection Cards */}
      <section className="pb-20 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="grid md:grid-cols-2 gap-8">
            {/* Job Seeker Card */}
            <button
              onClick={() => setProduct("seeker")}
              className="group bg-white rounded-2xl p-8 border-2 border-gray-200 hover:border-indigo-300 transition text-left hover:shadow-xl hover:-translate-y-1"
            >
              <div className="w-14 h-14 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition">
                <Users className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">求职者</h3>
              <p className="text-gray-600 mb-6">粘贴任何职位链接，AI自动分析你的简历匹配度，获得针对性优化建议</p>
              <ul className="space-y-3 text-sm text-gray-600">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  职位URL智能分析
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  技能匹配度评估
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  个性化优化建议
                </li>
              </ul>
            </button>

            {/* Recruiter Card */}
            <button
              onClick={() => setProduct("recruiter")}
              className="group bg-white rounded-2xl p-8 border-2 border-gray-200 hover:border-amber-300 transition text-left hover:shadow-xl hover:-translate-y-1"
            >
              <div className="w-14 h-14 bg-gradient-to-br from-amber-500 to-orange-600 rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 transition">
                <FileText className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-3">招聘者 / 猎头</h3>
              <p className="text-gray-600 mb-6">AI一键生成专业职位描述，多角色协作，简化招聘流程</p>
              <ul className="space-y-3 text-sm text-gray-600">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  AI生成专业JD
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  一键分享链接
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-500" />
                  团队协作管理
                </li>
              </ul>
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">为什么选择 KeyStone？</h2>
            <p className="text-gray-600 text-lg">专为新加坡就业市场打造的AI解决方案</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6 rounded-xl border border-gray-200 hover:border-indigo-200 hover:shadow-lg transition">
              <div className="w-16 h-16 bg-indigo-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Zap className="w-8 h-8 text-indigo-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">极速分析</h3>
              <p className="text-gray-600">30秒内完成简历与职位的深度分析，即时获取匹配报告</p>
            </div>
            <div className="text-center p-6 rounded-xl border border-gray-200 hover:border-green-200 hover:shadow-lg transition">
              <div className="w-16 h-16 bg-green-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Lock className="w-8 h-8 text-green-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">隐私保护</h3>
              <p className="text-gray-600">你的简历数据仅存储在新加坡数据中心，符合PDPA标准</p>
            </div>
            <div className="text-center p-6 rounded-xl border border-gray-200 hover:border-purple-200 hover:shadow-lg transition">
              <div className="w-16 h-16 bg-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-6">
                <Brain className="w-8 h-8 text-purple-600" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-3">AI驱动</h3>
              <p className="text-gray-600">基于GPT-4o大模型，持续学习最新招聘趋势和市场需求</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 px-4">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">简单透明的定价</h2>
            <p className="text-gray-600 text-lg">免费开始，按需升级</p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {/* Free */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:-translate-y-2 transition">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">免费版</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">$0</span>
                <span className="text-gray-500">/月</span>
              </div>
              <p className="text-gray-600 mb-6">适合个人求职者入门</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  每月10次职位分析
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  基础匹配度评分
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  申请历史追踪
                </li>
              </ul>
              <button className="w-full py-3 border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 transition">
                免费开始
              </button>
            </div>

            {/* Pro */}
            <div className="bg-white rounded-2xl p-8 border-2 border-indigo-600 relative hover:-translate-y-2 transition">
              <div className="absolute top-0 right-0 bg-indigo-600 text-white text-xs font-semibold px-3 py-1 rounded-bl-lg">最受欢迎</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">专业版</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">$19</span>
                <span className="text-gray-500">/月</span>
              </div>
              <p className="text-gray-600 mb-6">适合认真求职的专业人士</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  无限职位分析
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  详细技能分析报告
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  简历优化建议
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  优先客服支持
                </li>
              </ul>
              <button className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded-xl transition">
                升级到专业版
              </button>
            </div>

            {/* Team */}
            <div className="bg-white rounded-2xl p-8 border border-gray-200 hover:-translate-y-2 transition">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">团队版</h3>
              <div className="mb-6">
                <span className="text-4xl font-bold text-gray-900">$49</span>
                <span className="text-gray-500">/月</span>
              </div>
              <p className="text-gray-600 mb-6">适合猎头和招聘团队</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  无限JD生成
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  团队协作功能
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  自定义模板
                </li>
                <li className="flex items-center gap-3 text-sm text-gray-600">
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  API访问权限
                </li>
              </ul>
              <button className="w-full py-3 border-2 border-gray-300 text-gray-700 font-semibold rounded-xl hover:bg-gray-50 transition">
                联系销售
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
              <span className="text-sm">符合PDPA标准</span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              <span className="text-sm">专为新加坡市场</span>
            </div>
            <div className="flex items-center gap-2">
              <Lock className="w-5 h-5" />
              <span className="text-sm">数据留在新加坡</span>
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
              <a href="#" className="hover:text-white transition">关于我们</a>
              <a href="#" className="hover:text-white transition">隐私政策</a>
              <a href="#" className="hover:text-white transition">服务条款</a>
              <a href="#" className="hover:text-white transition">联系我们</a>
            </div>
            <p className="text-sm text-gray-500">© 2026 KeyStone. 新加坡制造。</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
