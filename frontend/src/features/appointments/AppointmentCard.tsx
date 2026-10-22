import { CalendarDays } from "lucide-react";
import { Card, CardTitle } from "@/components/ui/card";
import { dayAndTime } from "@/lib/format";
import type { StatusData } from "@/types/api";

export function AppointmentCard({ next }: { next: StatusData["next_appointment"] }) {
  return (
    <Card>
      <CardTitle>
        <CalendarDays className="h-5 w-5 text-teal" aria-hidden="true" /> Next appointment
      </CardTitle>
      {next ? (
        <>
          <p className="text-xl font-bold">{next.title}</p>
          <p className="font-data text-ink-soft">{dayAndTime(next.starts_at)}</p>
        </>
      ) : (
        <p className="text-ink-soft">Nothing planned yet.</p>
      )}
    </Card>
  );
}
