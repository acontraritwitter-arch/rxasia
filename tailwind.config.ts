import type { Config } from "tailwindcss";

/** App Router lives under `src/` — mirror `./app/**` as `./src/app/**` for Tailwind content scanning. */
const config: Config = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/lib/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],  theme: {
    extend: {
      colors: {
        canvas: {
          DEFAULT: "var(--color-canvas)",
          elevated: "var(--color-canvas-elevated)",
          muted: "var(--color-canvas-muted)",
        },
        brand: {
          DEFAULT: "var(--color-accent)",
          hover: "var(--color-accent-hover)",
          muted: "var(--color-accent-muted)",
        },
        ink: {
          DEFAULT: "var(--color-text-primary)",
          muted: "var(--color-text-secondary)",
          faint: "var(--color-text-faint)",
        },
        glass: {
          stroke: "var(--color-border-glass)",
          highlight: "var(--color-surface-glass)",
        },
      },
      fontFamily: {
        sans: ["var(--font-montserrat)", "sans-serif"],
      },
      fontSize: {
        "display-lg": [
          "clamp(2.5rem, 5vw, 4rem)",
          { lineHeight: "1.05", letterSpacing: "-0.03em" },
        ],
        "display-md": [
          "clamp(1.75rem, 3vw, 2.75rem)",
          { lineHeight: "1.1", letterSpacing: "-0.02em" },
        ],
      },
      spacing: {
        section: "clamp(2.5rem, 6vw, 4rem)",
      },
      boxShadow: {
        glass: "var(--shadow-glass)",
        cta: "var(--shadow-cta)",
      },
      borderRadius: {
        glass: "var(--radius-card)",
      },
      transitionTimingFunction: {
        out: "cubic-bezier(0.16, 1, 0.3, 1)",
      },
      zIndex: {
        nav: "40",
        overlay: "50",
        tooltip: "60",
      },
    },
  },
  plugins: [],
};

export default config;
