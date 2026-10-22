import { CheckCircle2, Clock, XCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { clock } from "@/lib/format";
import type { Dose } from "@/types/api";

const LOOK = {
  taken: { Icon: CheckCircle2, label: "Taken", tone: "teal" },
  pending: { Icon: Clock, label: "Pending", tone: "neutral" },
  missed: { Icon: XCircle, label: "Missed", tone: "coral" },
} as const;

export function MedicinesCard({ doses }: { doses: Dose[] }) {
  const taken = doses.filter((d) => d.status === "taken").length;
  return (
    <Card>
      <CardTitle>
        Today’s medicines{" "}
        <span className="font-data text-base font-normal text-ink-soft">
          {taken}/{doses.length} taken
        </span>
      </CardTitle>
      <ul className="divide-y divide-line">
        {doses.map((d) => {
          const { Icon, label, tone } = LOOK[d.status];
          return (
            <li
              key={`${d.medication_id}-${d.scheduled_for}`}
              className="flex min-h-tap items-center justify-between gap-3 py-2"
            >
              <span>
                <b>{d.name}</b>{" "}
                <span className="font-data text-ink-soft">{clock(d.scheduled_for)}</span>
              </span>
              <Badge tone={tone}>
                <Icon className="h-4 w-4" aria-hidden="true" />
                {label}
              </Badge>
            </li>
          );
        })}
      </ul>
    </Card>
  );
}
