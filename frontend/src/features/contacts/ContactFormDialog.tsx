import { zodResolver } from "@hookform/resolvers/zod";
import { UserPlus } from "lucide-react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { Field, inputCls } from "@/components/common/Field";
import { FormDialog } from "@/components/common/FormDialog";
import { Button } from "@/components/ui/button";
import { useCrud } from "@/hooks/useCrud";
import type { Contact } from "@/types/api";
import { contactSchema, type ContactForm } from "./schema";

export function ContactFormDialog() {
  const { create } = useCrud<
    Contact,
    { name: string; telegram_chat_id: string | null; role: string | null }
  >("contacts");
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ContactForm>({
    resolver: zodResolver(contactSchema),
    defaultValues: { name: "", telegram_chat_id: "", role: "" },
  });
  return (
    <FormDialog
      title="Add a family contact"
      trigger={
        <Button>
          <UserPlus className="h-5 w-5" aria-hidden="true" /> Add contact
        </Button>
      }
    >
      {(close) => (
        <form
          className="flex flex-col gap-4"
          onSubmit={handleSubmit((v) =>
            create.mutate(
              { name: v.name, telegram_chat_id: v.telegram_chat_id || null, role: v.role || null },
              {
                onSuccess: () => {
                  toast.success("Contact added");
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
          <Field label="Relationship" error={errors.role?.message}>
            <input className={inputCls} {...register("role")} placeholder="son" />
          </Field>
          <Field
            label="Telegram chat ID"
            error={errors.telegram_chat_id?.message}
            hint="Leave empty to use the console fallback. See the help below the list."
          >
            <input inputMode="numeric" className={inputCls} {...register("telegram_chat_id")} />
          </Field>
          <Button type="submit" disabled={create.isPending}>
            Save contact
          </Button>
        </form>
      )}
    </FormDialog>
  );
}
