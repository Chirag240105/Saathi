import { useState } from "react";
import { format } from "date-fns";
import { ErrorState, EmptyState, Skeleton } from "@/components/common/States";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle } from "@/components/ui/card";
import { Select } from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useEvents } from "@/features/events/useEvents";
import { AdherenceChart, MoodChart } from "@/features/history/Charts";
import { useHistory } from "@/features/history/useHistory";

const FILTERS = [
  { value: "all", label: "All events" },
  { value: "concern", label: "Concerns" },
  { value: "missed_dose", label: "Missed doses" },
  { value: "unwell", label: "Felt unwell" },
];

export function HistoryPage() {
  const [range, setRange] = useState("7");
  const [filter, setFilter] = useState("all");
  const hist = useHistory(Number(range));
  const events = useEvents(filter);

  const days = hist.data?.days ?? [];
  const taken = days.reduce((a, d) => a + d.taken, 0);
  const total = taken + days.reduce((a, d) => a + d.missed, 0);

  return (
    <div className="flex flex-col gap-5">
      <header className="flex flex-wrap items-center justify-between gap-3">
        <h1 className="text-3xl font-bold">History</h1>
        <Tabs value={range} onValueChange={setRange}>
          <TabsList aria-label="Range">
            {["7", "14", "30"].map((d) => (
              <TabsTrigger key={d} value={d}>
                {d} days
              </TabsTrigger>
            ))}
          </TabsList>
        </Tabs>
      </header>

      {hist.isLoading && <Skeleton className="h-72" />}
      {hist.isError && (
        <ErrorState message="Could not load history." onRetry={() => void hist.refetch()} />
      )}
      {hist.data && (
        <div className="grid gap-5 lg:grid-cols-2">
          <Card>
            <CardTitle>
              Dose adherence{" "}
              {total > 0 && <Badge tone="teal">{Math.round((taken / total) * 100)}% taken</Badge>}
            </CardTitle>
            <AdherenceChart days={days} />
          </Card>
          <Card>
            <CardTitle>Mood trend</CardTitle>
            <MoodChart days={days} />
          </Card>
        </div>
      )}

      <Card>
        <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
          <CardTitle className="mb-0">Events</CardTitle>
          <Select
            value={filter}
            onValueChange={setFilter}
            options={FILTERS}
            label="Filter events"
          />
        </div>
        {events.isLoading && <Skeleton className="h-32" />}
        {events.isError && (
          <ErrorState message="Could not load events." onRetry={() => void events.refetch()} />
        )}
        {events.data && events.data.length === 0 && (
          <EmptyState title="No events" hint="Nothing matches this filter." />
        )}
        {events.data && events.data.length > 0 && (
          <div className="overflow-x-auto">
            <table className="w-full min-w-[32rem] text-left">
              <thead className="text-sm text-ink-soft">
                <tr>
                  <th className="py-2">When</th>
                  <th>Type</th>
                  <th>Message</th>
                  <th>Family told</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line">
                {events.data.map((e) => (
                  <tr key={e.id}>
                    <td className="py-2 font-data text-sm">
                      {format(new Date(e.created_at), "d MMM, h:mm a")}
                    </td>
                    <td>
                      <Badge tone={e.type === "missed_dose" ? "amber" : "coral"}>
                        {e.type.replace("_", " ")}
                      </Badge>
                    </td>
                    <td>{e.message}</td>
                    <td>{e.notified ? "Yes" : "No"}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
