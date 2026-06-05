import Link from "next/link";
import type { ReactNode } from "react";
import { cn } from "@/lib/cn";

type ButtonVariant = "solid" | "ghost" | "glass";

type ButtonBaseProps = {
  children: ReactNode;
  className?: string;
  variant?: ButtonVariant;
};

type ButtonAsButton = ButtonBaseProps & {
  href?: undefined;
  type?: "button" | "submit";
  disabled?: boolean;
};

type ButtonAsLink = ButtonBaseProps & {
  href: string;
};

export type ButtonProps = ButtonAsButton | ButtonAsLink;

const variantClasses: Record<ButtonVariant, string> = {
  solid:
    "min-h-12 bg-brand text-canvas shadow-cta hover:bg-brand-hover hover:shadow-[0_16px_40px_rgba(242,101,34,0.42)] active:scale-[0.97]",
  ghost:
    "min-h-11 border border-glass-stroke bg-transparent text-ink hover:bg-white/5 active:scale-[0.97]",
  glass:
    "min-h-11 border border-glass-stroke bg-white/10 text-ink backdrop-blur-md hover:bg-white/15 active:scale-[0.97]",
};

function buttonClasses(variant: ButtonVariant, className?: string) {
  return cn(
    "inline-flex cursor-pointer items-center justify-center gap-2 rounded-full px-6 text-sm font-semibold",
    "transition-[transform,background-color,box-shadow] duration-150 ease-out hover:duration-150 active:duration-75 active:ease-in",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/60 focus-visible:ring-offset-2 focus-visible:ring-offset-canvas",
    variantClasses[variant],
    className,
  );
}

export function Button(props: ButtonProps) {
  const { children, className, variant = "solid" } = props;

  if ("href" in props && props.href) {
    return (
      <Link href={props.href} className={buttonClasses(variant, className)}>
        {children}
      </Link>
    );
  }

  const { type = "button", disabled } = props as ButtonAsButton;

  return (
    <button
      type={type}
      disabled={disabled}
      aria-disabled={disabled}
      className={cn(
        buttonClasses(variant, className),
        disabled && "cursor-not-allowed opacity-50",
      )}
    >
      {children}
    </button>
  );
}
