import { GlassPanel } from "@/components/ui/glass-panel";
import { Reveal } from "@/components/ui/reveal";
import { stats } from "@/lib/content";

export function StatsSection() {
  return (
    <section className="section-y bg-transparent pt-0">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <ul className="grid grid-cols-12 gap-4 sm:gap-6">
          {stats.map((item, index) => (
            <Reveal
              key={item.value}
              className="col-span-12 sm:col-span-6 xl:col-span-3"
              delay={index * 0.05}
            >
              <GlassPanel className="flex h-full flex-col justify-between p-8">
                <p className="text-4xl font-semibold tabular-nums text-brand md:text-5xl">
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
  );
}
