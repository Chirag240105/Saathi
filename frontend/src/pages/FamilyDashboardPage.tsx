import { AnimatePresence, motion } from "framer-motion";
import { CalendarPlus, MessageCircleHeart } from "lucide-react";
import { useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { ErrorState, Skeleton } from "@/components/common/States";
import { StatusChip } from "@/components/common/StatusChip";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { AppointmentCard } from "@/features/appointments/AppointmentCard";
import { AppointmentFormDialog } from "@/features/appointments/AppointmentFormDialog";
import { CheckinCard } from "@/features/checkins/CheckinCard";
import { EventsTimeline } from "@/features/events/EventsTimeline";
import { MedicinesCard } from "@/features/status/MedicinesCard";
import { UpdatedIndicator } from "@/features/status/UpdatedIndicator";
import { useAlertToasts } from "@/features/status/useAlertToasts";
import { useStatus } from "@/features/status/useStatus";
import { ToolCallLog } from "@/features/toolcalls/ToolCallLog";
import { api } from "@/lib/api";

export function FamilyDashboardPage() {
  const { data, isLoading, isError, error, refetch, dataUpdatedAt, isFetching } = useStatus();
  const fresh = useAlertToasts(data?.recent_events, data?.elder.name);
  const nudge = useMutation({
    mutationFn: () =>
      api<{ sent: number; total: number }>("/api/messages/check-in", {
        method: "POST",
        write: true,
      }),
    onSuccess: (r) => toast.success(`Check-in message sent to ${r.sent} of ${r.total}`),
    onError: (e) => toast.error(e.message),
  });

  if (isLoading) {
    return (
      <div className="grid gap-4 md:grid-cols-2" aria-busy="true">
        <Skeleton className="h-24 md:col-span-2" />
        <Skeleton className="h-56" />
        <Skeleton className="h-56" />
      </div>
    );
  }
  if (isError || !data)
    return (
      <ErrorState
        message={error?.message ?? "Could not load today’s status."}
        onRetry={() => void refetch()}
      />
    );

  return (
    <div className="flex flex-col gap-5">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <span
            aria-hidden="true"
            className="flex h-14 w-14 items-center justify-center rounded-full bg-teal text-2xl font-bold text-white"
          >
            {data.elder.name[0]}
          </span>
          <div>
            <h1 className="text-3xl font-bold">{data.elder.name}</h1>
            <UpdatedIndicator updatedAt={dataUpdatedAt} fetching={isFetching} />
          </div>
        </div>
        <AnimatePresence mode="wait">
          <motion.div
            key={data.overall}
            initial={{ scale: 0.85, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <StatusChip status={data.overall} className="text-xl" />
          </motion.div>
        </AnimatePresence>
      </header>
      <p className="sr-only" aria-live="assertive">
        Status: {data.overall.replace("_", " ")}
      </p>

      <div className="flex flex-wrap gap-3">
        <Button variant="outline" onClick={() => nudge.mutate()} disabled={nudge.isPending}>
          <MessageCircleHeart className="h-5 w-5" aria-hidden="true" /> Send a gentle check-in
          message
        </Button>
        <AppointmentFormDialog
          trigger={
            <Button variant="outline">
              <CalendarPlus className="h-5 w-5" aria-hidden="true" /> Add appointment
            </Button>
          }
        />
      </div>

      <div className="grid gap-5 md:grid-cols-2">
        <MedicinesCard doses={data.doses} />
        <div className="flex flex-col gap-5">
          <CheckinCard last={data.last_checkin} />
          <AppointmentCard next={data.next_appointment} />
        </div>
        <EventsTimeline events={data.recent_events} freshIds={fresh} />
        <Card className="md:col-span-2">
          <ToolCallLog compact limit={5} />
        </Card>
      </div>
    </div>
  );
}
