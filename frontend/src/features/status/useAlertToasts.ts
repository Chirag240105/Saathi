import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import type { EventItem } from "@/types/api";

/** Toasts new events after the first load and returns ids to highlight for a few seconds. */
export function useAlertToasts(events: EventItem[] | undefined, elderName: string | undefined) {
  const seen = useRef<Set<number> | null>(null);
  const [fresh, setFresh] = useState<Set<number>>(new Set());

  useEffect(() => {
    if (!events) return;
    if (seen.current === null) {
      seen.current = new Set(events.map((e) => e.id));
      return;
    }
    const added = events.filter((e) => !seen.current!.has(e.id));
    if (added.length === 0) return;
    added.forEach((e) => seen.current!.add(e.id));
    added.forEach((e) =>
      toast.error(`${elderName ?? "Your parent"}: ${e.message}`, {
        description: e.type.replace("_", " "),
      }),
    );
    setFresh(new Set(added.map((e) => e.id)));
    const t = setTimeout(() => setFresh(new Set()), 6000);
    return () => clearTimeout(t);
  }, [events, elderName]);

  return fresh;
}
