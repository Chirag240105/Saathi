import { Mic, RotateCcw } from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api";

export function TopBar() {
  const [busy, setBusy] = useState(false);

  async function resetDemo() {
    if (!window.confirm("Reset all demo data to the starting story?")) return;
    setBusy(true);
    try {
      await api("/api/admin/reset-demo", { method: "POST", write: true });
      toast.success("Demo data reset");
      window.location.reload();
    } catch (e) {
      toast.error(e instanceof Error ? e.message : "Could not reset demo data");
    } finally {
      setBusy(false);
    }
  }

  return (
    <header className="flex items-center justify-between gap-3 border-b border-line bg-sand/90 px-4 py-3 backdrop-blur md:px-8">
      <span className="rounded-full bg-amber-wash px-3 py-1 text-sm font-bold text-amber-ink">
        Demo mode · fictional data
      </span>
      <div className="flex items-center gap-2">
        <Button variant="ghost" onClick={resetDemo} disabled={busy} aria-label="Reset demo data">
          <RotateCcw className="h-5 w-5" aria-hidden="true" />
          <span className="hidden sm:inline">Reset demo</span>
        </Button>
        <Button asChild variant="outline">
          <Link to="/elder">
            <Mic className="h-5 w-5" aria-hidden="true" />
            <span className="hidden sm:inline">Open voice simulator</span>
          </Link>
        </Button>
      </div>
    </header>
  );
}
