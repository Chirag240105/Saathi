import { EmptyState } from "@/components/common/States";

export function ElderPage() {
  return (
    <section>
      <h1 className="mb-4 text-3xl font-bold">Voice companion</h1>
      <EmptyState title="Coming in Phase 6" hint="This screen is scaffolded and wired into the router." />
    </section>
  );
}
