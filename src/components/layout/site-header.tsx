"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { CaretRight, List, X } from "@phosphor-icons/react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { useFocusTrap } from "@/hooks/use-focus-trap";
import { HeaderIndustriesMenu } from "@/components/layout/header-industries-menu";
import { navLinks, site } from "@/lib/content";
import { cn } from "@/lib/cn";

const INDUSTRIES_SECTION_HREF = "#industries";

const ICON_SIZE = 24;
const ICON_WEIGHT = "regular" as const;

export function SiteHeader() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const toggleRef = useRef<HTMLButtonElement>(null);
  const reduce = useReducedMotion();

  useFocusTrap(menuRef, open, () => setOpen(false));

  const wasOpenRef = useRef(false);

  useEffect(() => {
    if (open) {
      wasOpenRef.current = true;
      document.body.style.overflow = "hidden";
      return () => {
        document.body.style.overflow = "";
      };
    }

    if (wasOpenRef.current) {
      toggleRef.current?.focus();
      wasOpenRef.current = false;
    }

    document.body.style.overflow = "";
    return undefined;
  }, [open]);

  return (
    <header className="fixed top-0 z-50 w-full text-gray-900 dark:text-white">
      <div className="border-b border-gray-100 bg-white shadow-sm dark:border-white/10 dark:bg-black/40 dark:shadow-none dark:backdrop-blur-md">
        <div className="mx-auto flex h-14 max-w-7xl items-center justify-between gap-3 px-4 sm:px-6 lg:h-16 lg:px-8">
          <Link
            href="/"
            aria-label={`${site.name} — home`}
            className="group flex shrink-0 items-baseline gap-0.5 text-lg font-semibold tracking-tight focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-black/40"
            onClick={() => {
              setOpen(false);
              if (pathname === "/") {
                window.scrollTo({ top: 0, behavior: "smooth" });
              }
            }}
          >
            <span className="text-gray-900 dark:text-white">RX</span>
            <span className="text-brand transition-colors duration-150 ease-out group-hover:text-brand-hover">
              Asia
            </span>
          </Link>

          <div className="hidden items-center gap-4 lg:flex lg:gap-6">
            <Button href="#contact" variant="ghost" className="gap-2 pr-5 pl-3">
              <span
                aria-hidden
                className="flex size-8 items-center justify-center rounded-full bg-brand text-canvas"
              >
                <CaretRight size={16} weight="bold" />
              </span>
              Contact us
            </Button>
            <nav aria-label="Primary">
              <ul className="flex items-center gap-6">
                {navLinks.map((item) =>
                  item.href === INDUSTRIES_SECTION_HREF ? (
                    <HeaderIndustriesMenu key={item.href} variant="desktop" />
                  ) : (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        className="inline-flex min-h-11 items-center text-xs font-medium uppercase tracking-widest text-gray-600 transition-colors duration-150 ease-out hover:text-gray-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:text-gray-300 dark:hover:text-white dark:focus-visible:ring-offset-black/40"
                      >
                        {item.label}
                      </Link>
                    </li>
                  ),
                )}
              </ul>
            </nav>
            <ThemeToggle />
          </div>

          <div className="flex items-center gap-2 lg:hidden">
            <button
              ref={toggleRef}
              type="button"
              className="flex size-11 cursor-pointer items-center justify-center rounded-full border border-gray-200 text-gray-900 transition-colors duration-150 ease-out hover:bg-gray-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 focus-visible:ring-offset-2 focus-visible:ring-offset-white active:scale-[0.97] dark:border-white/10 dark:text-white dark:hover:bg-white/5 dark:focus-visible:ring-offset-black/40"
              aria-expanded={open}
              aria-controls="mobile-menu"
              onClick={() => setOpen((v) => !v)}
            >
              <span className="sr-only">{open ? "Close menu" : "Open menu"}</span>
              <AnimatePresence mode="wait" initial={false}>
                {open ? (
                  <motion.span
                    key="close"
                    initial={reduce ? false : { opacity: 0, rotate: -90 }}
                    animate={{ opacity: 1, rotate: 0 }}
                    exit={{ opacity: 0, rotate: 90 }}
                    transition={{ duration: 0.15 }}
                  >
                    <X size={ICON_SIZE} weight={ICON_WEIGHT} aria-hidden />
                  </motion.span>
                ) : (
                  <motion.span
                    key="open"
                    initial={reduce ? false : { opacity: 0, rotate: 90 }}
                    animate={{ opacity: 1, rotate: 0 }}
                    exit={{ opacity: 0, rotate: -90 }}
                    transition={{ duration: 0.15 }}
                  >
                    <List size={ICON_SIZE} weight={ICON_WEIGHT} aria-hidden />
                  </motion.span>
                )}
              </AnimatePresence>
            </button>
            <ThemeToggle />
          </div>
        </div>
      </div>

      <AnimatePresence>
        {open ? (
          <motion.div
            ref={menuRef}
            id="mobile-menu"
            role="dialog"
            aria-modal="true"
            aria-label="Mobile navigation"
            initial={reduce ? false : { opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
            className={cn(
              "border-t border-gray-100 bg-white lg:hidden dark:border-white/10 dark:bg-black/40 dark:backdrop-blur-md",
            )}
          >
            <nav aria-label="Mobile" className="mx-auto max-w-7xl px-4 py-6 sm:px-6">
              <ul className="flex flex-col gap-2">
                {navLinks.map((item) =>
                  item.href === INDUSTRIES_SECTION_HREF ? (
                    <HeaderIndustriesMenu
                      key={item.href}
                      variant="mobile"
                      onNavigate={() => setOpen(false)}
                    />
                  ) : (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        className="flex min-h-11 items-center text-sm font-medium uppercase tracking-widest text-gray-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 dark:text-gray-200"
                        onClick={() => setOpen(false)}
                      >
                        {item.label}
                      </Link>
                    </li>
                  ),
                )}
                <li className="pt-2">
                  <Link
                    href="#contact"
                    className="inline-flex min-h-12 w-full items-center justify-center rounded-full bg-brand px-6 text-sm font-semibold text-canvas shadow-cta transition-[transform,box-shadow] duration-150 ease-out hover:shadow-[0_16px_40px_rgba(242,101,34,0.42)] active:scale-[0.97] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-black/40"
                    onClick={() => setOpen(false)}
                  >
                    Contact us
                  </Link>
                </li>
              </ul>
            </nav>
          </motion.div>
        ) : null}
      </AnimatePresence>

      <p className="sr-only">{site.tagline}</p>
    </header>
  );
}
