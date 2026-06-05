import { GlassPanel } from "@/components/ui/glass-panel";
import { Reveal } from "@/components/ui/reveal";
import { SectionEyebrow } from "@/components/ui/section-eyebrow";
import { aboutBlocks, approachItems } from "@/lib/content";

export function ApproachSection() {
  return (
    <section id="approach" className="section-y bg-transparent" aria-labelledby="approach-heading">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-12 gap-8 lg:items-end">
          <Reveal className="col-span-12 lg:col-span-5">
            <p className="text-sm font-medium text-ink-muted">
              {aboutBlocks.approachTagline}
            </p>
            <h2 id="approach-heading" className="sr-only">
              {aboutBlocks.approachEyebrow}
            </h2>
            <SectionEyebrow className="mt-4">
              {aboutBlocks.approachEyebrow}
            </SectionEyebrow>
          </Reveal>
        </div>

        <ul className="mt-12 grid grid-cols-12 gap-4 sm:gap-6">
          {approachItems.map((item, index) => (
            <Reveal
              key={item.index}
              className="col-span-12 md:col-span-6 xl:col-span-4"
              delay={(index % 3) * 0.05}
            >
              <GlassPanel className="flex h-full flex-col p-8">
                <span className="text-3xl font-semibold tabular-nums text-brand/80">
                  {item.index}
                </span>
                <h3 className="mt-4 text-lg font-semibold text-ink">{item.title}</h3>
                <p className="mt-3 flex-1 text-sm font-normal leading-relaxed text-ink-muted">
                  {item.description}
                </p>
              </GlassPanel>
            </Reveal>
          ))}
        </ul>
      </div>
    </section>
  );
}
