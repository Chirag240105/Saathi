import { AnimatePresence, motion } from "framer-motion";
import { CheckCircle2, XCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { EmptyState, ErrorState, Skeleton } from "@/components/common/States";
import { Tip } from "@/components/ui/tooltip";
import { cn } from "@/lib/utils";
import type { ToolCallItem } from "@/types/api";
import { useToolCalls } from "./useToolCalls";

/** Presentational list: each row shows tool, inputs, result, duration, status. */
export function ToolCallList({
  calls,
  compact = false,
}: {
  calls: ToolCallItem[];
  compact?: boolean;
}) {
  if (calls.length === 0) {
    return (
      <EmptyState
        title="No tool calls yet"
        hint="Say or tap something. Each request Saathi handles shows up here."
      />
    );
  }
  return (
    <ol className="flex flex-col gap-3" aria-label="MCP tool calls, newest first">
      <AnimatePresence initial={false}>
        {calls.map((c) => (
          <motion.li
            key={c.id}
            layout
            initial={{ opacity: 0, x: 16 }}
            animate={{ opacity: 1, x: 0 }}
            className="rounded-control border border-line bg-surface p-3 font-data text-sm"
          >
            <div className="flex flex-wrap items-center gap-2">
              <code className="font-bold text-teal-dark">{c.tool_name}</code>
              <Badge tone={c.source === "simulator" ? "teal" : "amber"}>{c.source}</Badge>
              <span className="ml-auto flex items-center gap-1">
                {c.success ? (
                  <CheckCircle2 className="h-4 w-4 text-teal" aria-hidden="true" />
                ) : (
                  <XCircle className="h-4 w-4 text-coral-ink" aria-hidden="true" />
                )}
                {c.success ? "ok" : "failed"} · {c.duration_ms} ms
              </span>
            </div>
            {!compact && (
              <pre className="mt-2 overflow-x-auto whitespace-pre-wrap break-words rounded bg-sand p-2 text-xs">
                {JSON.stringify(c.inputs)}
              </pre>
            )}
            <p className={cn("mt-2 text-ink", compact && "line-clamp-2")}>{c.result}</p>
          </motion.li>
        ))}
      </AnimatePresence>
    </ol>
  );
}

export function McpBadge() {
  return (
    <Tip label="Every request goes to the Saathi MCP server at /mcp using the Streamable HTTP transport.">
      <span tabIndex={0}>
        <Badge tone="teal">MCP over Streamable HTTP</Badge>
      </span>
    </Tip>
  );
}

/** Live panel: polls /api/tool-calls every 2 seconds. */
export function ToolCallLog({
  compact = false,
  limit = 30,
}: {
  compact?: boolean;
  limit?: number;
}) {
  const { data, isLoading, isError, refetch } = useToolCalls(limit);
  return (
    <section aria-label="Live MCP activity" className="flex flex-col gap-3">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h2 className="text-lg font-bold">Live MCP activity</h2>
        <McpBadge />
      </div>
      {isLoading && <Skeleton className="h-24" />}
      {isError && (
        <ErrorState message="Could not load tool calls." onRetry={() => void refetch()} />
      )}
      {data && <ToolCallList calls={data} compact={compact} />}
    </section>
  );
}
