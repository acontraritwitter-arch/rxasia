import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
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

const solutionGroupClassName =
  "group block h-full outline-none rounded-glass cursor-pointer";

const solutionPanelClassName = cn(
  "flex h-full flex-col overflow-hidden p-0",
  "transition-all duration-500 ease-[cubic-bezier(0.23,1,0.32,1)]",
  "group-hover:-translate-y-1.5 group-hover:shadow-xl group-hover:shadow-brand/10",
  "dark:group-hover:bg-white/[0.08] dark:group-hover:border-white/20 dark:group-hover:shadow-brand/5",
);

const solutionImagePaths = [
  "images/1.jpeg",
  "images/2.jpg",
  "images/3.jpg",
  "images/4.jpeg",
] as const;

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

      <section className={cn(sectionPad, "bg-gray-50 dark:bg-[#0a0510]")}>
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
                  <span className="text-sm font-semibold tabular-nums text-brand">
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

      <section className={cn(sectionPad, "bg-gray-50 dark:bg-[#0a0510]")}>
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
                <h3 className="text-xl font-semibold text-ink transition-colors duration-300 group-hover:text-brand dark:group-hover:text-white">
                  {solution.name}
                </h3>
              );

              const imagePath = solutionImagePaths[index];
              const imageSrc = imagePath ? publicMediaUrl(imagePath) : null;

              const cardBody = (
                <>
                  {imageSrc ? (
                    <div className="relative aspect-[5/3] w-full shrink-0 overflow-hidden">
                      <Image
                        src={imageSrc}
                        alt={`${solution.name} solution`}
                        fill
                        className="object-cover transition-transform duration-500 ease-[cubic-bezier(0.23,1,0.32,1)] group-hover:scale-105"
                        sizes="(max-width: 1024px) 100vw, 33vw"
                      />
                    </div>
                  ) : null}
                  <div className={cn(glassPanelPaddingClassName, "flex flex-1 flex-col")}>
                    {heading}
                    {featureList}
                  </div>
                </>
              );

              return (
                <Reveal
                  key={solution.name}
                  className="col-span-12 lg:col-span-4"
                  delay={index * 0.04}
                >
                  <li className="h-full list-none">
                    {"href" in solution && solution.href ? (
                      <Link href={solution.href} className={solutionGroupClassName}>
                        <GlassPanel className={solutionPanelClassName}>{cardBody}</GlassPanel>
                      </Link>
                    ) : (
                      <div className={cn(solutionGroupClassName, "cursor-default")}>
                        <GlassPanel className={solutionPanelClassName}>{cardBody}</GlassPanel>
                      </div>
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
                  <span className="mt-6 text-sm font-medium text-brand">Read more</span>
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
    </main>
  );
}
