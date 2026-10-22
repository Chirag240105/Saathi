import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { TOOL_CALLS_POLL_MS } from "@/lib/constants";
import { qk } from "@/lib/queryKeys";
import type { ToolCallItem } from "@/types/api";

export const useToolCalls = (limit = 30) =>
  useQuery({
    queryKey: [...qk.toolCalls, limit],
    queryFn: () => api<ToolCallItem[]>(`/api/tool-calls?limit=${limit}`),
    refetchInterval: TOOL_CALLS_POLL_MS,
  });
