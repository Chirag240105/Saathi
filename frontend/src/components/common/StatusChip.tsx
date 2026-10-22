import { AlertTriangle, CheckCircle2, ShieldAlert } from "lucide-react";
import type { OverallStatus } from "@/types/status";
import { cn } from "@/lib/utils";

const CONFIG = {
  all_good: { label: "All good", Icon: CheckCircle2, cls: "bg-teal-wash text-teal-dark" },
  attention: { label: "Needs attention", Icon: AlertTriangle, cls: "bg-amber-wash text-amber-ink" },
  alert: { label: "Alert", Icon: ShieldAlert, cls: "bg-coral-wash text-coral-ink" },
} as const;

/** Status is always icon + text + colour, never colour alone. */
export function StatusChip({ status, className }: { status: OverallStatus; className?: string }) {
  const { label, Icon, cls } = CONFIG[status];
  return (
    <span
      role="status"
      data-status={status}
      className={cn(
        "inline-flex min-h-tap items-center gap-2 rounded-full px-4 py-1.5 text-base font-bold",
        cls,
        className,
      )}
    >
      <Icon className="h-5 w-5" aria-hidden="true" />
      {label}
    </span>
  );
}
