import { cn } from "@/lib/cn";

type SectionEyebrowProps = {
  children: string;
  className?: string;
};

export function SectionEyebrow({ children, className }: SectionEyebrowProps) {
  return (
    <p
      className={cn(
        "text-xs font-semibold uppercase tracking-[0.28em] text-brand",
        className,
      )}
    >
      {children}
    </p>
  );
}
