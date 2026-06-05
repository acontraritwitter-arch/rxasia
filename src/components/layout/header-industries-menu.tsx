"use client";

import Link from "next/link";
import { CaretDown } from "@phosphor-icons/react";
import { useEffect, useId, useRef, useState } from "react";
import { industryItems } from "@/lib/content";
import { cn } from "@/lib/cn";

const navLinkClass =
  "inline-flex min-h-11 items-center gap-1 text-xs font-medium uppercase tracking-widest text-gray-600 transition-colors duration-150 ease-out hover:text-gray-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:text-gray-300 dark:hover:text-white dark:focus-visible:ring-offset-black/40";

const dropdownPanelClass = cn(
  "absolute right-0 top-[calc(100%+0.25rem)] z-tooltip min-w-[11rem] rounded-glass border border-gray-200 bg-white py-2 shadow-md",
  "dark:border-white/10 dark:bg-zinc-950/95 dark:backdrop-blur-md",
);

const dropdownItemClass =
  "block px-4 py-2.5 text-left text-sm font-medium text-gray-800 transition-colors hover:bg-gray-50 hover:text-brand dark:text-gray-200 dark:hover:bg-white/5 dark:hover:text-white";

type HeaderIndustriesMenuProps = {
  variant: "desktop" | "mobile";
  onNavigate?: () => void;
};

export function HeaderIndustriesMenu({ variant, onNavigate }: HeaderIndustriesMenuProps) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLLIElement>(null);
  const menuId = useId();

  useEffect(() => {
    if (!open || variant !== "desktop") return undefined;

    const handlePointerDown = (event: MouseEvent) => {
      if (!rootRef.current?.contains(event.target as Node)) {
        setOpen(false);
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };

    document.addEventListener("mousedown", handlePointerDown);
    document.addEventListener("keydown", handleEscape);
    return () => {
      document.removeEventListener("mousedown", handlePointerDown);
      document.removeEventListener("keydown", handleEscape);
    };
  }, [open, variant]);

  const close = () => {
    setOpen(false);
    onNavigate?.();
  };

  if (variant === "mobile") {
    return (
      <li>
        <Link
          href="/#industries"
          className="flex min-h-11 items-center text-sm font-medium uppercase tracking-widest text-gray-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 dark:text-gray-200"
          onClick={close}
        >
          INDUSTRIES
        </Link>
        <ul className="mt-1 flex flex-col gap-0.5 border-l border-gray-200 pl-4 dark:border-white/10">
          {industryItems.map((industry) => (
            <li key={industry.slug}>
              <Link
                href={`/${industry.slug}`}
                className="flex min-h-10 items-center text-sm font-medium text-gray-600 transition-colors hover:text-brand dark:text-gray-300 dark:hover:text-white"
                onClick={close}
              >
                {industry.name}
              </Link>
            </li>
          ))}
        </ul>
      </li>
    );
  }

  return (
    <li className="relative" ref={rootRef}>
      <button
        type="button"
        className={navLinkClass}
        aria-expanded={open}
        aria-haspopup="menu"
        aria-controls={menuId}
        onClick={() => setOpen((value) => !value)}
      >
        INDUSTRIES
        <CaretDown
          size={14}
          weight="bold"
          className={cn("transition-transform duration-150", open && "rotate-180")}
          aria-hidden
        />
      </button>
      {open ? (
        <ul id={menuId} role="menu" className={dropdownPanelClass}>
          {industryItems.map((industry) => (
            <li key={industry.slug} role="none">
              <Link
                href={`/${industry.slug}`}
                role="menuitem"
                className={dropdownItemClass}
                onClick={() => setOpen(false)}
              >
                {industry.name}
              </Link>
            </li>
          ))}
        </ul>
      ) : null}
    </li>
  );
}
