import { zodResolver } from "@hookform/resolvers/zod";
import { Plus } from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { Field, inputCls } from "@/components/common/Field";
import { FormDialog } from "@/components/common/FormDialog";
import { Button } from "@/components/ui/button";
import { useCrud } from "@/hooks/useCrud";
import type { Medication } from "@/types/api";
import { medicineSchema, splitList, type MedicineForm } from "./schema";

type Input = { name: string; aliases: string[]; dose: string | null; times: string[] };

export function MedicineFormDialog() {
  const { create } = useCrud<Medication, Input>("medications");
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<MedicineForm>({
    resolver: zodResolver(medicineSchema),
    defaultValues: { name: "", aliases: "", dose: "", times: "" },
  });

  return (
    <FormDialog
      title="Add a medicine"
      description="Aliases are the ways your parent says it, such as “BP tablet”."
      trigger={
        <Button>
          <Plus className="h-5 w-5" aria-hidden="true" /> Add medicine
        </Button>
      }
    >
      {(close) => (
        <form
          className="flex flex-col gap-4"
          onSubmit={handleSubmit((v) =>
            create.mutate(
              {
                name: v.name,
                aliases: splitList(v.aliases),
                dose: v.dose || null,
                times: splitList(v.times),
              },
              {
                onSuccess: () => {
                  toast.success("Medicine added");
                  reset();
                  close();
                },
                onError: (e) => toast.error(e.message),
              },
            ),
          )}
        >
          <Field label="Name" error={errors.name?.message}>
            <input className={inputCls} {...register("name")} />
          </Field>
          <Field label="Other names (comma separated)" error={errors.aliases?.message}>
            <input className={inputCls} {...register("aliases")} placeholder="bp, blood pressure" />
          </Field>
          <Field label="Dose" error={errors.dose?.message}>
            <input className={inputCls} {...register("dose")} placeholder="1 tablet" />
          </Field>
          <Field label="Times (24-hour, comma separated)" error={errors.times?.message}>
            <input className={inputCls} {...register("times")} placeholder="08:00, 20:00" />
          </Field>
          <Button type="submit" disabled={create.isPending}>
            Save medicine
          </Button>
        </form>
      )}
    </FormDialog>
  );
}
