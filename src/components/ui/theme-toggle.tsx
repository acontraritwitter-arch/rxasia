"use client";

import { Moon, Sun } from "@phosphor-icons/react";
import { useTheme } from "@/components/providers/theme-provider";

const ICON_SIZE = 24;
const ICON_WEIGHT = "regular" as const;

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      type="button"
      onClick={toggleTheme}
      className="flex size-11 cursor-pointer items-center justify-center rounded-full border border-gray-200 text-gray-900 transition-colors duration-150 ease-out hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 focus-visible:ring-offset-2 focus-visible:ring-offset-white active:scale-[0.97] dark:border-white/10 dark:text-white dark:hover:bg-white/5 dark:focus-visible:ring-offset-black/40"
      aria-label={theme === "dark" ? "Switch to light theme" : "Switch to dark theme"}
    >
      {theme === "dark" ? (
        <Sun size={ICON_SIZE} weight={ICON_WEIGHT} aria-hidden />
      ) : (
        <Moon size={ICON_SIZE} weight={ICON_WEIGHT} aria-hidden />
      )}
    </button>
  );
}
