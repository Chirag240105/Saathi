import { RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";

export function UpdatedIndicator({
  updatedAt,
  fetching,
}: {
  updatedAt: number;
  fetching: boolean;
}) {
  const [now, setNow] = useState(() => Date.now());
  useEffect(() => {
    const t = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(t);
  }, []);
  const secs = Math.max(0, Math.round((now - updatedAt) / 1000));
  return (
    <span className="inline-flex items-center gap-1.5 text-sm text-ink-soft" aria-live="off">
      <RefreshCw className={`h-4 w-4 ${fetching ? "animate-spin" : ""}`} aria-hidden="true" />
      {secs < 5 ? "Updated just now" : `Updated ${secs}s ago`}
    </span>
  );
}
