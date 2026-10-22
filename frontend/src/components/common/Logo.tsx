import { cn } from "@/lib/utils";

/** Two arcs leaning together: a companion beside you. */
export function Logo({ className, withWord = true }: { className?: string; withWord?: boolean }) {
  return (
    <span className={cn("inline-flex items-center gap-2.5", className)}>
      <svg width="34" height="34" viewBox="0 0 34 34" fill="none" aria-hidden="true">
        <circle cx="17" cy="17" r="17" fill="hsl(var(--teal))" />
        <path d="M9 22c0-6 3-10 8-10" stroke="#fff" strokeWidth="3" strokeLinecap="round" />
        <path d="M25 22c0-6-3-10-8-10" stroke="hsl(var(--amber))" strokeWidth="3" strokeLinecap="round" />
        <circle cx="17" cy="23.5" r="2" fill="#fff" />
      </svg>
      {withWord && <span className="text-2xl font-bold tracking-tight">Saathi</span>}
    </span>
  );
}
