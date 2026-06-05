import type { ReactNode } from "react";

/**
 * Shared surface for About + Stats so background does not break between card grid and metrics.
 */
export function AboutStatsBand({ children }: { children: ReactNode }) {
  return (
    <div className="bg-gradient-to-b from-canvas-elevated from-0% via-canvas via-[42%] to-canvas to-100%">
      {children}
    </div>
  );
}
