import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/layout/site-footer";
import { IndustryHero } from "@/components/industry/industry-hero";
import { Reveal } from "@/components/ui/reveal";
import { SectionEyebrow } from "@/components/ui/section-eyebrow";
import { Button } from "@/components/ui/button";
import { GlassPanel, glassPanelPaddingClassName } from "@/components/ui/glass-panel";
import { rxFleetPage } from "@/lib/products/rx-fleet-content";
import { publicMediaUrl } from "@/lib/public-asset";
import { cn } from "@/lib/cn";

const fleetHeroVideoSrc = publicMediaUrl("media/fleet-bg.mp4");

export const metadata: Metadata = {
  title: `${rxFleetPage.meta.title} | RXAsia`,
  description: rxFleetPage.meta.description,
};

const sectionPad = "py-12 md:py-16";
const sectionHeadGap = "mb-8 md:mb-10";

const panelClass = cn(glassPanelPaddingClassName, "h-full");

export default function RxFleetPage() {
  const { hero, overview, provenResults, modules, deployment, cta } = rxFleetPage;

  return (
    <main id="main">
      <IndustryHero
        eyebrow={hero.eyebrow}
        title={hero.title}
        titleGradientPhrase="optimization"
        videoSrc={fleetHeroVideoSrc}
      />

      <section className={cn(sectionPad, "bg-canvas-elevated")}>
        <div className="mx-auto max-w-7xl px-4 text-left sm:px-6 lg:px-8">
          <Reveal className="max-w-3xl">
            <SectionEyebrow className="text-gray-900 dark:text-white">
              {overview.eyebrow}
            </SectionEyebrow>
            <p className="mt-6 text-lg font-semibold leading-relaxed text-ink">
              {overview.lead}
            </p>
            <p className="mt-4 text-lg font-normal leading-relaxed text-ink-muted">
              {overview.body}
            </p>
          </Reveal>
        </div>
      </section>

      <section className={sectionPad}>
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Reveal className={sectionHeadGap}>
            <SectionEyebrow>{provenResults.eyebrow}</SectionEyebrow>
          </Reveal>
          <ul className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {provenResults.items.map((item, index) => (
              <Reveal key={item.label} delay={index * 0.04}>
                <GlassPanel className="flex h-full flex-col justify-between p-8">
                  <p className="font-mono text-4xl font-semibold tabular-nums text-brand md:text-5xl">
                    {item.value}
                  </p>
                  <p className="mt-4 text-sm font-medium leading-relaxed text-ink-muted">
                    {item.label}
                  </p>
                </GlassPanel>
              </Reveal>
            ))}
          </ul>
        </div>
      </section>

      {modules.map((module, moduleIndex) => (
        <section
          key={module.id}
          className={cn(
            sectionPad,
            moduleIndex % 2 === 0 ? "bg-canvas-elevated" : undefined,
          )}
        >
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <Reveal className={sectionHeadGap}>
              <SectionEyebrow
                className={moduleIndex % 2 === 0 ? "text-gray-900 dark:text-white" : undefined}
              >
                {module.eyebrow}
              </SectionEyebrow>
              <h2 className="mt-4 text-display-md font-semibold text-ink">{module.title}</h2>
              <p className="mt-4 max-w-3xl text-base font-normal leading-relaxed text-ink-muted">
                {module.functionality}
              </p>
            </Reveal>

            {"featureEyebrow" in module && module.featureEyebrow ? (
              <p className="mb-4 text-xs font-semibold uppercase tracking-[0.28em] text-brand">
                {module.featureEyebrow}
              </p>
            ) : null}

            <ul className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              {module.features.map((feature, index) => (
                <Reveal key={feature} delay={index * 0.03}>
                  <GlassPanel
                    as="li"
                    className={cn(panelClass, "text-sm font-normal leading-relaxed text-ink-muted")}
                  >
                    {feature}
                  </GlassPanel>
                </Reveal>
              ))}
            </ul>

            {module.metrics && module.metrics.length > 0 ? (
              <div className="mt-10">
                {"metricsEyebrow" in module && module.metricsEyebrow ? (
                  <p className="mb-4 text-xs font-semibold uppercase tracking-[0.28em] text-brand">
                    {module.metricsEyebrow}
                  </p>
                ) : null}
                <ul className="grid grid-cols-1 gap-4 sm:grid-cols-3">
                  {module.metrics.map((metric, index) => (
                    <Reveal key={metric.label} delay={index * 0.04}>
                      <GlassPanel className="flex h-full flex-col justify-between p-8 text-center">
                        <p className="font-mono text-3xl font-semibold tabular-nums text-brand md:text-4xl">
                          {metric.value}
                        </p>
                        <p className="mt-2 text-sm font-medium leading-relaxed text-ink-muted">
                          {metric.label}
                        </p>
                      </GlassPanel>
                    </Reveal>
                  ))}
                </ul>
              </div>
            ) : null}
          </div>
        </section>
      ))}

      <section className={cn(sectionPad, "bg-canvas-elevated")}>
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Reveal className={sectionHeadGap}>
            <SectionEyebrow className="text-gray-900 dark:text-white">
              {deployment.eyebrow}
            </SectionEyebrow>
            <h2 className="mt-4 text-display-md font-semibold text-ink">{deployment.title}</h2>
            <p className="mt-4 max-w-3xl text-base font-normal leading-relaxed text-ink-muted">
              {deployment.body}
            </p>
          </Reveal>
          <ul className="grid grid-cols-1 gap-4 md:grid-cols-3">
            {deployment.tiers.map((tier, index) => (
              <Reveal key={tier.name} delay={index * 0.05}>
                <GlassPanel as="li" className={panelClass}>
                  <h3 className="text-lg font-semibold text-ink">{tier.name}</h3>
                  <p className="mt-3 text-sm font-normal leading-relaxed text-ink-muted">
                    {tier.description}
                  </p>
                </GlassPanel>
              </Reveal>
            ))}
          </ul>
        </div>
      </section>

      <section className={sectionPad}>
        <div className="mx-auto max-w-3xl px-4 text-center sm:px-6 lg:px-8">
          <Reveal>
            <h2 className="text-display-md font-semibold text-ink">{cta.title}</h2>
            <p className="mt-4 text-base font-normal leading-relaxed text-ink-muted">
              {cta.body}
            </p>
            <div className="mt-8 flex justify-center">
              <Button href={cta.href} variant="solid">
                {cta.button}
              </Button>
            </div>
          </Reveal>
        </div>
      </section>

      <section className="border-t border-glass-stroke/60 py-10 md:py-12 dark:border-white/10">
        <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <Link
            href="/"
            className="text-sm font-medium text-brand transition-colors hover:text-brand-hover"
          >
            ← Back to home
          </Link>
        </div>
      </section>
      <SiteFooter />
    </main>
  );
}
