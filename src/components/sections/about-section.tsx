import { Reveal } from "@/components/ui/reveal";
import { SectionEyebrow } from "@/components/ui/section-eyebrow";
import { aboutBlocks } from "@/lib/content";

export function AboutSection() {
  return (
    <section
      id="about"
      className="bg-transparent pt-12 pb-8 md:pt-16 md:pb-10"
      aria-labelledby="about-heading"
    >
      <h2 id="about-heading" className="sr-only">
        About RXAsia
      </h2>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-10 md:grid-cols-2 md:gap-12 lg:gap-16">
          <Reveal>
            <SectionEyebrow>{aboutBlocks.whatWeDo.eyebrow}</SectionEyebrow>
            <p className="mt-5 max-w-[65ch] text-lg font-normal leading-relaxed text-ink-muted">
              {aboutBlocks.whatWeDo.body}
            </p>
          </Reveal>
          <Reveal delay={0.06}>
            <SectionEyebrow>{aboutBlocks.mission.eyebrow}</SectionEyebrow>
            <p className="mt-5 max-w-[65ch] text-lg font-normal leading-relaxed text-ink-muted">
              {aboutBlocks.mission.body}
            </p>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
