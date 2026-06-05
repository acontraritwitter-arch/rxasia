import { SiteFooter } from "@/components/layout/site-footer";
import { ContactInviteSection } from "@/components/sections/contact-invite-section";
import { AboutSection } from "@/components/sections/about-section";
import { AchievementsSection } from "@/components/sections/achievements-section";
import { ApproachSection } from "@/components/sections/approach-section";
import { ConsultingSection } from "@/components/sections/consulting-section";
import { HeroSection } from "@/components/sections/hero-section";
import { IndustriesSection } from "@/components/sections/industries-section";
import { ServicesSection } from "@/components/sections/services-section";
import { StatsSection } from "@/components/sections/stats-section";

export default function HomePage() {
  return (
    <main id="main">
      <HeroSection />
      <div className="bg-gradient-to-b from-white to-[#fff8f5] dark:from-zinc-950 dark:to-[#140a1d]">
        <AboutSection />
        <StatsSection />
        <AchievementsSection />
        <ConsultingSection />
        <ServicesSection />
        <IndustriesSection />
        <ApproachSection />
        <section id="careers" className="sr-only bg-transparent" tabIndex={-1} aria-label="Careers" />
      </div>
      <ContactInviteSection />
      <SiteFooter />
    </main>
  );
}
