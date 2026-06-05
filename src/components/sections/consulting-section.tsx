import Image from "next/image";
import { Reveal } from "@/components/ui/reveal";
import { consulting } from "@/lib/content";

export function ConsultingSection() {
  return (
    <section className="section-y bg-transparent">
      <div className="mx-auto grid max-w-7xl grid-cols-12 items-center gap-10 px-4 sm:px-6 lg:px-8">
        <Reveal className="col-span-12 lg:col-span-5">
          <h2 className="text-display-md font-semibold text-balance text-ink">
            {consulting.title}
          </h2>
        </Reveal>
        <Reveal className="col-span-12 lg:col-span-7" delay={0.06}>
          <p className="max-w-[65ch] text-base font-normal leading-relaxed text-ink-muted">
            {consulting.body}
          </p>
        </Reveal>
        <Reveal className="col-span-12" delay={0.1}>
          <div className="relative mt-4 aspect-[21/9] overflow-hidden rounded-glass border border-glass-stroke">
            <Image
              src="https://picsum.photos/seed/rxasia-consulting-lab/1600/700"
              alt="Wide view of a technology workspace used for digital transformation consulting"
              fill
              sizes="100vw"
              className="object-cover opacity-90"
            />
            <div
              className="absolute inset-0 bg-canvas/40 mix-blend-multiply"
              aria-hidden
            />
          </div>
        </Reveal>
      </div>
    </section>
  );
}
