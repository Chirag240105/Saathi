import type { HTMLAttributes } from "react";
import { cn } from "@/lib/utils";

const TONES = {
  neutral: "bg-sand-deep text-ink",
  teal: "bg-teal-wash text-teal-dark",
  amber: "bg-amber-wash text-amber-ink",
  coral: "bg-coral-wash text-coral-ink",
} as const;

export function Badge({
  tone = "neutral",
  className,
  ...p
}: HTMLAttributes<HTMLSpanElement> & { tone?: keyof typeof TONES }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full px-2.5 py-0.5 text-sm font-bold",
        TONES[tone],
        className,
      )}
      {...p}
    />
  );
}
