import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "bg-primary": "#090d1a",
        "bg-secondary": "#0d1120",
        "bg-card": "#111827",
        border: "#1f2d45",
        "accent-cyan": "#00d4ff",
        "accent-amber": "#ffb300",
        "accent-green": "#00ff88",
        "accent-red": "#ff4d6d",
        "text-primary": "#e2e8f0",
        "text-muted": "#64748b",
      },
      fontFamily: {
        mono: ["JetBrains Mono", "monospace"],
        heading: ["Syne", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
