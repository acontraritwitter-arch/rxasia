import { Button } from "@/components/ui/button";
import { GlassPanel } from "@/components/ui/glass-panel";
import { Reveal } from "@/components/ui/reveal";
import { SectionEyebrow } from "@/components/ui/section-eyebrow";
import { aboutBlocks, achievements } from "@/lib/content";

export function AchievementsSection() {
  return (
    <section className="section-y bg-transparent" aria-labelledby="achievements-heading">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <Reveal>
          <h2 id="achievements-heading" className="sr-only">
            {aboutBlocks.achievementsEyebrow}
          </h2>
          <SectionEyebrow>{aboutBlocks.achievementsEyebrow}</SectionEyebrow>
        </Reveal>
        <div className="mt-10 grid grid-cols-12 gap-6 lg:gap-8">
          {achievements.map((card, index) => (
            <Reveal
              key={card.title}
              className="col-span-12 lg:col-span-6"
              delay={index * 0.08}
            >
              <GlassPanel className="flex h-full flex-col p-8">
                <h2 className="text-2xl font-semibold text-ink">{card.title}</h2>
                <div className="mt-6 space-y-4">
                  {card.body.map((paragraph) => (
                    <p
                      key={paragraph}
                      className="text-base font-normal leading-relaxed text-ink-muted"
                    >
                      {paragraph}
                    </p>
                  ))}
                </div>
                <div className="mt-8">
                  <Button href="#contact" variant="solid">
                    {card.cta}
                  </Button>
                </div>
              </GlassPanel>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
