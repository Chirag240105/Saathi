import { Trash2 } from "lucide-react";
import type { ReactNode } from "react";
import { EmptyState, ErrorState, Skeleton } from "@/components/common/States";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { AppointmentFormDialog } from "@/features/appointments/AppointmentFormDialog";
import { ContactFormDialog } from "@/features/contacts/ContactFormDialog";
import { MedicineFormDialog } from "@/features/medications/MedicineFormDialog";
import { useCrud } from "@/hooks/useCrud";
import { dayAndTime } from "@/lib/format";
import type { Appointment, Contact, Medication } from "@/types/api";

function Row({
  title,
  sub,
  onDelete,
  label,
}: {
  title: string;
  sub: string;
  onDelete: () => void;
  label: string;
}) {
  return (
    <li className="flex items-center justify-between gap-3 py-3">
      <div className="min-w-0">
        <p className="font-bold">{title}</p>
        <p className="break-words text-ink-soft">{sub}</p>
      </div>
      <Button
        variant="ghost"
        size="icon"
        aria-label={`Delete ${label}`}
        onClick={() => window.confirm(`Delete ${label}?`) && onDelete()}
      >
        <Trash2 className="h-5 w-5 text-coral-ink" aria-hidden="true" />
      </Button>
    </li>
  );
}

function Panel<T>({
  q,
  empty,
  add,
  render,
}: {
  q: { isLoading: boolean; isError: boolean; data?: T[]; refetch: () => unknown };
  empty: string;
  add: ReactNode;
  render: (items: T[]) => ReactNode;
}) {
  return (
    <Card>
      <div className="mb-3 flex justify-end">{add}</div>
      {q.isLoading && <Skeleton className="h-32" />}
      {q.isError && (
        <ErrorState message="Could not load this list." onRetry={() => void q.refetch()} />
      )}
      {q.data && q.data.length === 0 && <EmptyState title={empty} />}
      {q.data && q.data.length > 0 && <ul className="divide-y divide-line">{render(q.data)}</ul>}
    </Card>
  );
}

export function CareSetupPage() {
  const meds = useCrud<Medication, unknown>("medications");
  const appts = useCrud<Appointment, unknown>("appointments");
  const contacts = useCrud<Contact, unknown>("contacts");
  return (
    <div className="flex flex-col gap-5">
      <h1 className="text-3xl font-bold">Care setup</h1>
      <Tabs defaultValue="medicines">
        <TabsList>
          <TabsTrigger value="medicines">Medicines</TabsTrigger>
          <TabsTrigger value="appointments">Appointments</TabsTrigger>
          <TabsTrigger value="contacts">Family contacts</TabsTrigger>
        </TabsList>
        <TabsContent value="medicines">
          <Panel
            q={meds.list}
            empty="No medicines yet"
            add={<MedicineFormDialog />}
            render={(items) =>
              items.map((m) => (
                <Row
                  key={m.id}
                  label={m.name}
                  title={m.name}
                  sub={`${m.dose ?? ""} · ${m.times.join(", ")}${m.aliases.length ? ` · also “${m.aliases.slice(0, 3).join("”, “")}”` : ""}`}
                  onDelete={() => meds.remove.mutate(m.id)}
                />
              ))
            }
          />
        </TabsContent>
        <TabsContent value="appointments">
          <Panel
            q={appts.list}
            empty="No upcoming appointments"
            add={<AppointmentFormDialog />}
            render={(items) =>
              items.map((a) => (
                <Row
                  key={a.id}
                  label={a.title}
                  title={a.title}
                  sub={dayAndTime(a.starts_at)}
                  onDelete={() => appts.remove.mutate(a.id)}
                />
              ))
            }
          />
        </TabsContent>
        <TabsContent value="contacts">
          <Panel
            q={contacts.list}
            empty="No family contacts yet"
            add={<ContactFormDialog />}
            render={(items) =>
              items.map((c) => (
                <Row
                  key={c.id}
                  label={c.name}
                  title={`${c.name}${c.role ? ` (${c.role})` : ""}`}
                  sub={
                    c.telegram_chat_id
                      ? `Telegram chat ID ${c.telegram_chat_id}`
                      : "No Telegram yet: alerts go to the console"
                  }
                  onDelete={() => contacts.remove.mutate(c.id)}
                />
              ))
            }
          />
          <Card className="mt-5 bg-teal-wash text-teal-dark">
            <h2 className="mb-2 text-lg font-bold">How to get a Telegram chat ID</h2>
            <ol className="list-decimal space-y-1 pl-5">
              <li>
                In Telegram, open <b>@BotFather</b>, send <code>/newbot</code>, and copy the bot
                token into <code>TELEGRAM_BOT_TOKEN</code> in <code>.env</code>.
              </li>
              <li>
                Ask each family member to open your new bot and press <b>Start</b>.
              </li>
              <li>
                Open <code>https://api.telegram.org/bot&lt;TOKEN&gt;/getUpdates</code> and find{" "}
                <code>"chat":&#123;"id": 123456789</code>.
              </li>
              <li>Paste that number here as the contact’s chat ID.</li>
            </ol>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
