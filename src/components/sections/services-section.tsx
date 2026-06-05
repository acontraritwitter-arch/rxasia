import { GlassPanel } from "@/components/ui/glass-panel";
import { Reveal } from "@/components/ui/reveal";
import { SectionEyebrow } from "@/components/ui/section-eyebrow";
import { aboutBlocks, services } from "@/lib/content";

export function ServicesSection() {
  return (
    <section id="services" className="section-y bg-transparent" aria-labelledby="services-heading">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-12 gap-8">
          <Reveal className="col-span-12 lg:col-span-4">
            <h2 id="services-heading" className="sr-only">
              {aboutBlocks.servicesEyebrow}
            </h2>
            <SectionEyebrow>{aboutBlocks.servicesEyebrow}</SectionEyebrow>
            <p className="mt-6 text-base font-normal leading-relaxed text-ink-muted">
              {services.intro}
            </p>
          </Reveal>
          <div className="col-span-12 flex flex-col gap-6 lg:col-span-8">
            {services.items.map((item, index) => (
              <Reveal key={item.title} delay={index * 0.06}>
                <GlassPanel className="p-8">
                  <h3 className="text-xl font-semibold text-ink">{item.title}</h3>
                  {item.description ? (
                    <p className="mt-4 text-sm font-normal leading-relaxed text-ink-muted">
                      {item.description}
                    </p>
                  ) : null}
                </GlassPanel>
              </Reveal>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
