import type { Metadata } from "next";
import Link from "next/link";
import { SiteFooter } from "@/components/layout/site-footer";
import { IndustryHero } from "@/components/industry/industry-hero";
import { GlassPanel, glassPanelPaddingClassName } from "@/components/ui/glass-panel";
import { Reveal } from "@/components/ui/reveal";
import { SectionEyebrow } from "@/components/ui/section-eyebrow";
import { miningPage } from "@/lib/industries/mining-content";
import { publicMediaUrl } from "@/lib/public-asset";
import { cn } from "@/lib/cn";

const miningHeroVideoSrc = publicMediaUrl("media/mining-bg.mp4");

export const metadata: Metadata = {
  title: `${miningPage.meta.title} | RXAsia`,
  description: miningPage.meta.description,
};

const sectionPad = "py-12 md:py-16";
const sectionHeadGap = "mb-8 md:mb-10";

const panelClass = cn(glassPanelPaddingClassName, "h-full");

const solutionLinkClassName =
  "block h-full transition-transform duration-200 ease-out hover:-translate-y-1";

export default function MiningPage() {
  const { hero, whatWeDo, advantages, solutions, caseStudies } = miningPage;

  return (
    <main id="main">
      <IndustryHero
        eyebrow={hero.eyebrow}
        title={hero.title}
        titleGradientPhrase="bring clarity"
        videoSrc={miningHeroVideoSrc}
      />

      <section className={cn(sectionPad, "bg-canvas-elevated")}>
        <div className="mx-auto max-w-7xl px-4 text-left sm:px-6 lg:px-8">
          <Reveal className="max-w-3xl">
            <SectionEyebrow className="text-gray-900 dark:text-white">
              {whatWeDo.eyebrow}
            </SectionEyebrow>
            <p className="mt-6 text-lg font-normal leading-relaxed text-ink-muted">
              {whatWeDo.body}
            </p>
          </Reveal>
        </div>
      </section>

      <section className={sectionPad}>
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Reveal className={sectionHeadGap}>
            <SectionEyebrow>{advantages.eyebrow}</SectionEyebrow>
            <h2 className="mt-4 text-display-md font-semibold text-ink">{advantages.title}</h2>
          </Reveal>
          <ul className="grid grid-cols-12 gap-4 sm:gap-6">
            {advantages.items.map((item, index) => (
              <Reveal
                key={item.index}
                className="col-span-12 md:col-span-6 lg:col-span-4"
                delay={index * 0.04}
              >
                <GlassPanel as="li" className={cn(panelClass, "flex flex-col")}>
                  <span className="font-mono text-sm font-semibold tabular-nums text-brand">
                    {String(item.index).padStart(2, "0")}
                  </span>
                  <h3 className="mt-3 text-lg font-semibold text-ink">{item.title}</h3>
                  <p className="mt-3 flex-1 text-sm font-normal leading-relaxed text-ink-muted">
                    {item.body}
                  </p>
                </GlassPanel>
              </Reveal>
            ))}
          </ul>
        </div>
      </section>

      <section className={cn(sectionPad, "bg-canvas-elevated")}>
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Reveal className={sectionHeadGap}>
            <SectionEyebrow className="text-gray-900 dark:text-white">
              {solutions.eyebrow}
            </SectionEyebrow>
          </Reveal>
          <ul className="grid grid-cols-12 gap-6">
            {solutions.items.map((solution, index) => {
              const featureList = (
                <ul className="mt-6 space-y-3">
                  {solution.features.map((feature) => (
                    <li
                      key={feature}
                      className="flex gap-3 text-sm font-normal leading-relaxed text-ink-muted"
                    >
                      <span className="mt-2 size-1.5 shrink-0 rounded-full bg-brand" aria-hidden />
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
              );

              const heading = (
                <h3 className="text-xl font-semibold text-ink">{solution.name}</h3>
              );

              return (
                <Reveal
                  key={solution.name}
                  className="col-span-12 lg:col-span-4"
                  delay={index * 0.05}
                >
                  <li className="h-full list-none">
                    {"href" in solution && solution.href ? (
                      <Link href={solution.href} className={solutionLinkClassName}>
                        <GlassPanel className={panelClass}>
                          {heading}
                          {featureList}
                        </GlassPanel>
                      </Link>
                    ) : (
                      <GlassPanel className={panelClass}>
                        {heading}
                        {featureList}
                      </GlassPanel>
                    )}
                  </li>
                </Reveal>
              );
            })}
          </ul>
        </div>
      </section>

      <section className={sectionPad}>
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <Reveal className={sectionHeadGap}>
            <SectionEyebrow>{caseStudies.eyebrow}</SectionEyebrow>
          </Reveal>
          <ul className="grid grid-cols-12 gap-6">
            {caseStudies.items.map((study, index) => (
              <Reveal
                key={study.title}
                className="col-span-12 md:col-span-4"
                delay={index * 0.05}
              >
                <GlassPanel as="li" className={cn(panelClass, "flex flex-col")}>
                  <h3 className="text-lg font-semibold text-balance text-ink">{study.title}</h3>
                  <p className="mt-4 flex-1 text-sm font-normal leading-relaxed text-ink-muted">
                    {study.body}
                  </p>
                  <Link
                    href="#contact"
                    className="mt-6 inline-flex min-h-11 items-center text-sm font-medium text-brand transition-colors hover:text-brand-hover"
                  >
                    Request case study brief
                  </Link>
                </GlassPanel>
              </Reveal>
            ))}
          </ul>
        </div>
      </section>

      <section className="border-t border-glass-stroke/60 py-10 md:py-12 dark:border-white/10">
        <div className="mx-auto max-w-7xl px-4 text-center sm:px-6 lg:px-8">
          <Link
            href="/#industries"
            className="text-sm font-medium text-brand transition-colors hover:text-brand-hover"
          >
            ← All industries
          </Link>
        </div>
      </section>
      <SiteFooter />
    </main>
  );
}
