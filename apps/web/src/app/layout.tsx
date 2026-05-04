import type { Metadata } from "next"
import { ClerkProvider } from "@clerk/nextjs"
import { Inter, Fraunces } from "next/font/google"
import { PostHogProvider } from "@/components/PostHogProvider"
import { Toaster } from "@/components/ui/toaster"
import "./globals.css"

// Inter Variable for body text - loaded with CJK subsets
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
})

// Fraunces (Instrument Serif alternative) for headings
const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
  display: "swap",
})

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
    <html lang="en" className={`${inter.variable} ${fraunces.variable}`}>
      <body className="font-sans antialiased">
        <ClerkProvider>
          <PostHogProvider>
            <Toaster />
            {children}
          </PostHogProvider>
        </ClerkProvider>
      </body>
    </html>
  )
}
