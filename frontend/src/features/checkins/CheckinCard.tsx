import { Card, CardTitle } from "@/components/ui/card";
import { ago, MOOD_EMOJI } from "@/lib/format";
import type { StatusData } from "@/types/api";

export function CheckinCard({ last }: { last: StatusData["last_checkin"] }) {
  return (
    <Card>
      <CardTitle>Last check-in</CardTitle>
      {last ? (
        <div className="flex items-center gap-4">
          <span className="text-5xl" aria-hidden="true">
            {MOOD_EMOJI[last.mood]}
          </span>
          <div>
            <p className="text-xl font-bold capitalize">Feeling {last.mood}</p>
            {last.note && <p className="text-ink-soft">“{last.note}”</p>}
            <p className="text-sm text-ink-soft">{ago(last.created_at)}</p>
          </div>
        </div>
      ) : (
        <p className="text-ink-soft">No check-in yet today.</p>
      )}
    </Card>
  );
}
