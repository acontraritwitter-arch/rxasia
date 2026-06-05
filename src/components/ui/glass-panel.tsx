import type { ReactNode } from "react";
import { cn } from "@/lib/cn";

/** Default inner padding — matches stats cards (300, 32, 500, 900). */
export const glassPanelPaddingClassName = "p-8";

type GlassPanelProps = {
  children: ReactNode;
  className?: string;
  as?: "div" | "section" | "article" | "li";
};

export function GlassPanel({
  children,
  className,
  as: Component = "div",
}: GlassPanelProps) {
  return (
    <Component
      className={cn(
        "glass-fallback rounded-glass border border-glass-stroke bg-glass-highlight shadow-glass",
        "backdrop-blur-xl backdrop-saturate-[1.8]",
        "shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]",
        className,
      )}
    >
      {children}
    </Component>
  );
}
