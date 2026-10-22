import type { ReactNode } from "react";

export function Field({
  label,
  error,
  hint,
  children,
}: {
  label: string;
  error?: string;
  hint?: string;
  children: ReactNode;
}) {
  return (
    <label className="flex flex-col gap-1 text-base font-bold">
      {label}
      {children}
      {hint && !error && <span className="text-sm font-normal text-ink-soft">{hint}</span>}
      {error && (
        <span role="alert" className="text-sm font-bold text-coral-ink">
          {error}
        </span>
      )}
    </label>
  );
}

export const inputCls =
  "min-h-tap rounded-control border-2 border-line bg-surface px-3 text-base font-normal";
