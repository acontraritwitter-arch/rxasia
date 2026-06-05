import { Reveal } from "@/components/ui/reveal";
import { site } from "@/lib/content";
import { publicMediaUrl } from "@/lib/public-asset";

const heroVideoSrc = publicMediaUrl("media/hero-bg.mp4");

export function HeroSection() {
  return (
    <section className="relative flex h-[40vh] w-full items-center justify-center overflow-hidden md:h-[50vh]">
      <video
        autoPlay
        loop
        muted
        playsInline
        className="absolute inset-0 -z-20 h-full w-full object-cover object-center"
        src={heroVideoSrc}
        aria-hidden
      />
      <div className="absolute inset-0 -z-10 bg-black/30" aria-hidden />
      <div className="relative z-10 mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
        <Reveal>
          <p className="text-sm font-medium uppercase tracking-[0.24em] text-white/80">
            {site.tagline}
          </p>
        </Reveal>
        <Reveal delay={0.08}>
          <h1 className="mt-6 text-display-lg font-semibold text-balance text-white">
            {site.heroTitle.replace(/\s*excellence\s*$/i, " ")}
            <span className="bg-gradient-to-r from-[#FF6100] to-[#DD00FF] bg-clip-text text-transparent">
              excellence
            </span>
          </h1>
        </Reveal>
      </div>
    </section>
  );
}
