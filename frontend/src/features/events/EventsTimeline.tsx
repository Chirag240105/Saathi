import { AlertTriangle, Frown, Pill } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { EmptyState } from "@/components/common/States";
import { ago } from "@/lib/format";
import { cn } from "@/lib/utils";
import type { EventItem } from "@/types/api";

const ICON = { concern: AlertTriangle, missed_dose: Pill, unwell: Frown } as const;
const LABEL = { concern: "Concern", missed_dose: "Missed dose", unwell: "Felt unwell" } as const;

export function EventRow({ e, fresh }: { e: EventItem; fresh?: boolean }) {
  const Icon = ICON[e.type];
  return (
    <li
      className={cn(
        "flex gap-3 rounded-control p-3 transition-colors",
        fresh ? "bg-coral-wash ring-2 ring-coral" : "bg-sand",
      )}
    >
      <Icon className="mt-1 h-5 w-5 shrink-0 text-coral-ink" aria-hidden="true" />
      <div className="min-w-0 flex-1">
        <p className="font-bold">{LABEL[e.type]}</p>
        <p className="break-words">{e.message}</p>
        <p className="mt-1 flex flex-wrap items-center gap-2 text-sm text-ink-soft">
          {ago(e.created_at)}
          <Badge tone={e.notified ? "teal" : "amber"}>
            {e.notified ? "Family told" : "Not delivered"}
          </Badge>
        </p>
      </div>
    </li>
  );
}

export function EventsTimeline({
  events,
  freshIds,
}: {
  events: EventItem[];
  freshIds: Set<number>;
}) {
  return (
    <Card className="md:col-span-2">
      <CardTitle>Recent events</CardTitle>
      {events.length === 0 ? (
        <EmptyState
          title="Nothing to worry about"
          hint="Concerns and missed doses will appear here."
        />
      ) : (
        <ul className="flex flex-col gap-2">
          {events.map((e) => (
            <EventRow key={e.id} e={e} fresh={freshIds.has(e.id)} />
          ))}
        </ul>
      )}
    </Card>
  );
}
