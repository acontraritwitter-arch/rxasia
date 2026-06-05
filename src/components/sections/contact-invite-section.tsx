import { CaretRight } from "@phosphor-icons/react/dist/ssr";
import { GlassInput } from "@/components/ui/glass-input";
import { Reveal } from "@/components/ui/reveal";
import { cn } from "@/lib/cn";

export function ContactInviteSection() {
  return (
    <section
      id="contact"
      aria-labelledby="contact-invite-heading"
      className="relative z-[1] border-t border-gray-200/50 bg-white py-16 md:py-24 dark:border-white/5 dark:bg-[#0a0510]"
    >
      <div className="mx-auto grid max-w-7xl grid-cols-1 items-center gap-12 px-4 sm:px-6 lg:grid-cols-2 lg:gap-8 lg:px-8">
        <Reveal>
          <p className="text-xs font-semibold uppercase tracking-[0.28em] text-brand">Get in touch</p>
          <h2
            id="contact-invite-heading"
            className="mt-4 text-display-md font-semibold text-balance text-ink"
          >
            Don&apos;t be a stranger!
          </h2>
          <p className="mt-4 max-w-[42ch] text-base font-normal leading-relaxed text-ink-muted">
            Leave your work email. We typically reply within two business days.
          </p>
        </Reveal>

        <Reveal delay={0.06}>
          <form className="flex w-full flex-col" noValidate>
            <label
              htmlFor="contact-email"
              className="mb-2 block text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400"
            >
              Work email
            </label>
            <div className="flex gap-4">
              <GlassInput
                id="contact-email"
                name="email"
                type="email"
                placeholder="name@company.kz"
                autoComplete="email"
                className="min-h-12 flex-1"
              />
              <button
                type="submit"
                className={cn(
                  "flex min-h-12 shrink-0 cursor-pointer items-center justify-center gap-2 rounded-full bg-brand px-6 text-canvas shadow-cta transition-[transform,box-shadow] duration-200 ease-out",
                  "hover:bg-brand-hover hover:shadow-[0_16px_40px_rgba(242,101,34,0.42)] active:scale-[0.97]",
                  "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 focus-visible:ring-offset-2 focus-visible:ring-offset-white dark:focus-visible:ring-offset-[#0a0510]",
                )}
                aria-label="Submit email"
              >
                <span className="text-sm font-semibold">Send</span>
                <CaretRight size={20} weight="bold" aria-hidden />
              </button>
            </div>
          </form>
        </Reveal>
      </div>
    </section>
  );
}
