import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        // Stone palette (warm gray - NOT cool gray)
        stone: {
          50: "hsl(30 6.7% 97%)",
          100: "hsl(30 5.9% 95%)",
          200: "hsl(30 5.9% 90.4%)",
          300: "hsl(30 4.7% 82.9%)",
          400: "hsl(30 3.7% 64.9%)",
          500: "hsl(30 5.2% 50.2%)",
          600: "hsl(30 5.6% 41%)",
          700: "hsl(30 8.9% 30%)",
          800: "hsl(30 9.8% 21.6%)",
          900: "hsl(30 14.3% 17.5%)",
          950: "hsl(30 14.3% 8.9%)",
        },
        // Brand primary (teal-blue)
        brand: {
          50: "#EFF8FA",
          100: "#D5ECF1",
          200: "#ADE0E6",
          300: "#7FC4D2",
          400: "#4FA8BE",
          500: "#1E7A8C",
          600: "#155E6E",
          700: "#0F4751",
          800: "#0A3037",
          900: "#082C33",
        },
        // Match levels
        "match-strong": "hsl(var(--match-strong))",
        "match-transferable": "hsl(var(--match-transferable))",
        "match-addressable": "hsl(var(--match-addressable))",
        "match-fundamental": "hsl(var(--match-fundamental))",
        // Match tints
        "match-strong-tint": "hsl(var(--match-strong-tint))",
        "match-transferable-tint": "hsl(var(--match-transferable-tint))",
        "match-addressable-tint": "hsl(var(--match-addressable-tint))",
        "match-fundamental-tint": "hsl(var(--match-fundamental-tint))",
      },
      fontFamily: {
        // Inter Variable for body with CJK fallback
        sans: [
          "Inter Variable",
          "Inter",
          "PingFang SC",
          "Microsoft YaHei",
          "Hiragino Sans",
          "Noto Sans SC",
          "Noto Sans JP",
          "system-ui",
          "sans-serif",
        ],
        // JetBrains Mono for code
        mono: [
          "JetBrains Mono",
          "Fira Code",
          "Consolas",
          "monospace",
        ],
        // Fraunces (Instrument Serif alternative) for headings
        display: [
          "Fraunces",
          "Instrument Serif",
          "Georgia",
          "serif",
        ],
      },
      transitionDuration: {
        instant: "80ms",
        fast: "160ms",
        base: "240ms",
        slow: "360ms",
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config
