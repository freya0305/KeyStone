import type { Metadata } from "next";
import { ClerkProvider } from "@clerk/nextjs";
import "./globals.css";

export const metadata: Metadata = {
  title: "KeyStone - AI Resume Optimization for Job Seekers",
  description: "Tailor your resume for each job application with AI-powered suggestions",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className="bg-gray-50 min-h-screen">{children}</body>
      </html>
    </ClerkProvider>
  );
}
