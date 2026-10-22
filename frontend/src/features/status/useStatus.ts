import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { STATUS_POLL_MS } from "@/lib/constants";
import { qk } from "@/lib/queryKeys";
import type { StatusData } from "@/types/api";

export const useStatus = () =>
  useQuery({
    queryKey: qk.status,
    queryFn: () => api<StatusData>("/api/status"),
    refetchInterval: STATUS_POLL_MS,
  });
