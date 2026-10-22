import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        sand: { DEFAULT: "hsl(var(--sand))", deep: "hsl(var(--sand-deep))" },
        surface: "hsl(var(--surface))",
        ink: { DEFAULT: "hsl(var(--ink))", soft: "hsl(var(--ink-soft))" },
        line: "hsl(var(--line))",
        teal: { DEFAULT: "hsl(var(--teal))", dark: "hsl(var(--teal-dark))", wash: "hsl(var(--teal-wash))" },
        amber: { DEFAULT: "hsl(var(--amber))", wash: "hsl(var(--amber-wash))", ink: "hsl(var(--amber-ink))" },
        coral: { DEFAULT: "hsl(var(--coral))", wash: "hsl(var(--coral-wash))", ink: "hsl(var(--coral-ink))" },
      },
      fontFamily: {
        sans: ['"Atkinson Hyperlegible"', "system-ui", "sans-serif"],
        data: ['"Inter Variable"', "Inter", "system-ui", "sans-serif"],
      },
      borderRadius: { card: "1.25rem", control: "0.875rem" },
      boxShadow: {
        card: "0 1px 2px hsl(var(--ink) / 0.06), 0 6px 20px -8px hsl(var(--ink) / 0.12)",
        lift: "0 10px 30px -10px hsl(var(--ink) / 0.25)",
      },
      minHeight: { tap: "44px", "tap-elder": "64px" },
      minWidth: { tap: "44px", "tap-elder": "64px" },
    },
  },
  plugins: [],
} satisfies Config;
