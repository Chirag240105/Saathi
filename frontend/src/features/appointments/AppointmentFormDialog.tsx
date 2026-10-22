import { zodResolver } from "@hookform/resolvers/zod";
import { CalendarPlus } from "lucide-react";
import type { ReactNode } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { Field, inputCls } from "@/components/common/Field";
import { FormDialog } from "@/components/common/FormDialog";
import { Button } from "@/components/ui/button";
import { useCrud } from "@/hooks/useCrud";
import type { Appointment } from "@/types/api";
import { appointmentSchema, type AppointmentForm } from "./schema";

export function AppointmentFormDialog({ trigger }: { trigger?: ReactNode }) {
  const { create } = useCrud<Appointment, { title: string; starts_at: string }>("appointments");
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<AppointmentForm>({
    resolver: zodResolver(appointmentSchema),
    defaultValues: { title: "", date: "", time: "" },
  });
  return (
    <FormDialog
      title="Add an appointment"
      trigger={
        trigger ?? (
          <Button>
            <CalendarPlus className="h-5 w-5" aria-hidden="true" /> Add appointment
          </Button>
        )
      }
    >
      {(close) => (
        <form
          className="flex flex-col gap-4"
          onSubmit={handleSubmit((v) =>
            create.mutate(
              { title: v.title, starts_at: `${v.date}T${v.time}:00` },
              {
                onSuccess: () => {
                  toast.success("Appointment added");
                  reset();
                  close();
                },
                onError: (e) => toast.error(e.message),
              },
            ),
          )}
        >
          <Field label="What is it for?" error={errors.title?.message}>
            <input className={inputCls} {...register("title")} placeholder="Eye checkup" />
          </Field>
          <Field label="Date" error={errors.date?.message}>
            <input type="date" className={inputCls} {...register("date")} />
          </Field>
          <Field label="Time" error={errors.time?.message}>
            <input type="time" className={inputCls} {...register("time")} />
          </Field>
          <Button type="submit" disabled={create.isPending}>
            Save appointment
          </Button>
        </form>
      )}
    </FormDialog>
  );
}
