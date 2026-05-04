import type { Metadata } from "next"
import { ClerkProvider } from "@clerk/nextjs"
import { Inter } from "next/font/google"
import { PostHogProvider } from "@/components/PostHogProvider"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "KeyStone - AI Job Seeker Copilot",
  description: "AI-powered resume optimization for Singapore job seekers",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <ClerkProvider>
          <PostHogProvider>
            {children}
          </PostHogProvider>
        </ClerkProvider>
      </body>
    </html>
  )
}
