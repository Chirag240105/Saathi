import { CalendarDays, Pill } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Skeleton } from "@/components/common/States";
import { useStatus } from "@/features/status/useStatus";
import { clock, dayAndTime } from "@/lib/format";

/** Plain-language summary for the elder: next medicine and next appointment. */
export function TodayCard() {
  const { data, isLoading } = useStatus();
  if (isLoading) return <Skeleton className="h-28" />;
  if (!data) return null;
  const next = data.doses.find((d) => d.status !== "taken");
  return (
    <Card className="grid gap-3 text-xl md:grid-cols-2">
      <p className="flex items-start gap-3">
        <Pill className="mt-1 h-7 w-7 shrink-0 text-teal" aria-hidden="true" />
        <span>
          <b>Next medicine</b>
          <br />
          {next ? `${next.name} at ${clock(next.scheduled_for)}` : "All done for today"}
        </span>
      </p>
      <p className="flex items-start gap-3">
        <CalendarDays className="mt-1 h-7 w-7 shrink-0 text-teal" aria-hidden="true" />
        <span>
          <b>Next appointment</b>
          <br />
          {data.next_appointment
            ? `${data.next_appointment.title}, ${dayAndTime(data.next_appointment.starts_at)}`
            : "Nothing planned"}
        </span>
      </p>
    </Card>
  );
}
