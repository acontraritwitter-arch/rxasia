import { cn } from "@/lib/cn";

type GlassInputProps = {
  id: string;
  name: string;
  type?: string;
  placeholder?: string;
  className?: string;
  autoComplete?: string;
  disabled?: boolean;
  "aria-invalid"?: boolean;
  "aria-describedby"?: string;
};

export function GlassInput({
  id,
  name,
  type = "email",
  placeholder,
  className,
  autoComplete,
  disabled,
  "aria-invalid": ariaInvalid,
  "aria-describedby": ariaDescribedBy,
}: GlassInputProps) {
  return (
    <input
      id={id}
      name={name}
      type={type}
      placeholder={placeholder}
      autoComplete={autoComplete}
      disabled={disabled}
      aria-invalid={ariaInvalid}
      aria-describedby={ariaDescribedBy}
      className={cn(
        "w-full min-h-11 rounded-xl border border-glass-stroke bg-white/10 px-4 py-2.5 text-sm font-medium text-ink shadow-inner",
        "placeholder:text-ink-faint",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-500/50",
        "disabled:cursor-not-allowed disabled:opacity-50",
        ariaInvalid && "border-red-500/60 focus-visible:ring-red-500/40",
        className,
      )}
    />
  );
}
