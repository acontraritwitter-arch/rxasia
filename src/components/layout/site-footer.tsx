import Link from "next/link";
import { navLinks, site } from "@/lib/content";
import { cn } from "@/lib/cn";

export function SiteFooter() {
  return (
    <footer
      className={cn(
        "border-t border-glass-stroke/60 py-12 md:py-14",
        "dark:relative dark:z-[1] dark:bg-canvas",
        "light:border-white/10 light:bg-[#0a0510]",
      )}
    >
      <div className="mx-auto grid max-w-7xl grid-cols-12 gap-10 px-4 sm:gap-12 sm:px-6 lg:px-8">
        <div className="col-span-12 md:col-span-5 lg:col-span-4">
          <p className="text-xs font-semibold uppercase tracking-widest text-brand">Contact us</p>
          <a
            href={`mailto:${site.contactEmail}`}
            className={cn(
              "mt-4 block break-all text-base font-medium text-ink underline-offset-4 transition-colors duration-150 ease-out hover:text-brand hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60",
              "light:text-[#f4f0f8] light:hover:text-brand-hover",
            )}
          >
            {site.contactEmail}
          </a>
          <p
            className={cn(
              "mt-4 break-words text-sm font-normal leading-relaxed text-ink-muted",
              "light:text-white/70",
            )}
          >
            {site.address}
          </p>
        </div>

        <div className="col-span-12 sm:col-span-6 md:col-span-4 lg:col-span-4">
          <p
            className={cn(
              "text-xs font-semibold uppercase tracking-widest text-ink-muted",
              "light:text-white/50",
            )}
          >
            Explore
          </p>
          <nav aria-label="Footer" className="mt-4">
            <ul className="grid gap-1 sm:grid-cols-2 sm:gap-x-8 lg:grid-cols-1">
              {navLinks.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={cn(
                      "inline-flex min-h-11 items-center text-sm font-medium capitalize text-ink-muted transition-colors duration-150 ease-out hover:text-ink focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60",
                      "light:text-white/70 light:hover:text-[#f4f0f8]",
                    )}
                  >
                    {item.label.charAt(0) + item.label.slice(1).toLowerCase()}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>

        <div className="col-span-12 sm:col-span-6 md:col-span-3 lg:col-span-4 lg:text-right">
          <p className={cn("text-sm font-semibold text-ink", "light:text-[#f4f0f8]")}>
            <span className={cn("text-ink", "light:text-[#f4f0f8]")}>RX</span>
            <span className="text-brand">Asia</span>
          </p>
          <p
            className={cn(
              "mt-3 max-w-xs text-sm font-normal leading-relaxed text-ink-muted lg:ml-auto",
              "light:text-white/70",
            )}
          >
            {site.tagline}
          </p>
        </div>
      </div>
    </footer>
  );
}
