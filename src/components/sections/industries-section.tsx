import Link from "next/link";
import {
  Landmark,
  Truck,
  Pickaxe,
  Plane,
  ShoppingBag,
  type LucideIcon,
} from "lucide-react";
import { GlassPanel, glassPanelPaddingClassName } from "@/components/ui/glass-panel";
import { Reveal } from "@/components/ui/reveal";
import { SectionEyebrow } from "@/components/ui/section-eyebrow";
import { aboutBlocks, industryItems } from "@/lib/content";
import { cn } from "@/lib/cn";

const industryIcons: Record<(typeof industryItems)[number]["slug"], LucideIcon> = {
  banking: Landmark,
  logistics: Truck,
  airports: Plane,
  retail: ShoppingBag,
  mining: Pickaxe,
};

const industryLinkClassName = "group block h-full outline-none rounded-2xl";

const industryPanelClassName = cn(
  glassPanelPaddingClassName,
  "flex h-full min-h-[8.5rem] flex-col items-center justify-center gap-3 text-center",
  "transition-all duration-500 ease-[cubic-bezier(0.23,1,0.32,1)]",
  "group-hover:-translate-y-1.5 group-hover:shadow-xl group-hover:shadow-brand/10",
  "dark:group-hover:bg-white/[0.08] dark:group-hover:border-white/20 dark:group-hover:shadow-brand/5"
);

export function IndustriesSection() {
  return (
    <section id="industries" className="section-y bg-transparent" aria-labelledby="industries-heading">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <Reveal>
          <h2 id="industries-heading" className="sr-only">
            {aboutBlocks.industriesEyebrow}
          </h2>
          <SectionEyebrow>{aboutBlocks.industriesEyebrow}</SectionEyebrow>
        </Reveal>
        
        <ul className="mt-10 grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-5">
          {industryItems.map((industry, index) => {
            const Icon = industryIcons[industry.slug];
            
            return (
              <Reveal key={industry.slug} delay={index * 0.04} className="h-full">
                <li className="h-full">
                  <Link href={`/${industry.slug}`} className={industryLinkClassName}>
                    <GlassPanel className={industryPanelClassName}>
                      <span className="flex size-11 items-center justify-center rounded-full bg-brand/10 text-brand transition-transform duration-500 ease-[cubic-bezier(0.23,1,0.32,1)] group-hover:scale-110">
                        <Icon className="size-5" strokeWidth={1.75} aria-hidden />
                      </span>
                      <span className="text-sm font-semibold text-ink transition-colors duration-300 group-hover:text-brand dark:group-hover:text-white">
                        {industry.name}
                      </span>
                    </GlassPanel>
                  </Link>
                </li>
              </Reveal>
            );
          })}
        </ul>
      </div>
    </section>
  );
}