import { EmptyState } from "@/components/common/States";

export function HistoryPage() {
  return (
    <section>
      <h1 className="mb-4 text-3xl font-bold">History</h1>
      <EmptyState title="Coming in Phase 6" hint="This screen is scaffolded and wired into the router." />
    </section>
  );
}
