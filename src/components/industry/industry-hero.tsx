import { Reveal } from "@/components/ui/reveal";

const titleGradientClassName =
  "bg-gradient-to-r from-[#FF6100] to-[#DD00FF] bg-clip-text text-transparent";

type IndustryHeroProps = {
  eyebrow: string;
  title: string;
  titleGradientPhrase?: string;
  videoSrc?: string;
};

function renderHeroTitle(title: string, gradientPhrase?: string) {
  if (!gradientPhrase) return title;

  const index = title.indexOf(gradientPhrase);
  if (index === -1) return title;

  const before = title.slice(0, index);
  const after = title.slice(index + gradientPhrase.length);

  return (
    <>
      {before}
      <span className={titleGradientClassName}>{gradientPhrase}</span>
      {after}
    </>
  );
}

export function IndustryHero({
  eyebrow,
  title,
  titleGradientPhrase,
  videoSrc,
}: IndustryHeroProps) {  return (
    <section className="relative flex h-[40vh] w-full items-center justify-center overflow-hidden md:h-[50vh]">
      {videoSrc ? (
        <>
          <video
            autoPlay
            loop
            muted
            playsInline
            className="absolute inset-0 -z-20 h-full w-full object-cover object-center"
            src={videoSrc}
            aria-hidden
          />
          <div className="absolute inset-0 -z-10 bg-black/50" aria-hidden />
        </>
      ) : (
        <>
          <div
            className="absolute inset-0 -z-20 bg-gradient-to-br from-[#0a0510] via-[#1c0f2e] to-[#120818]"
            aria-hidden
          />
          <div
            className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_70%_60%_at_50%_0%,rgba(242,101,34,0.18),transparent)]"
            aria-hidden
          />
          <div className="absolute inset-0 -z-10 bg-black/25" aria-hidden />
        </>
      )}
      <div className="relative z-10 mx-auto max-w-4xl px-4 text-center sm:px-6 lg:px-8">
        <Reveal>
          <p className="text-sm font-medium uppercase tracking-[0.24em] text-white">
            {eyebrow}
          </p>
        </Reveal>
        <Reveal delay={0.08}>
          <h1 className="mt-5 text-display-lg font-semibold text-balance text-white">
            {renderHeroTitle(title, titleGradientPhrase)}
          </h1>
        </Reveal>
      </div>
    </section>
  );
}
