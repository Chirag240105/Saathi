import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { qk } from "@/lib/queryKeys";
import type { HistoryDay } from "@/types/api";

export const useHistory = (days: number) =>
  useQuery({
    queryKey: qk.history(days),
    queryFn: () => api<{ days: HistoryDay[] }>(`/api/history?days=${days}`),
  });
