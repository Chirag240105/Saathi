import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { qk } from "@/lib/queryKeys";
import type { EventItem } from "@/types/api";

export const useEvents = (type = "all", limit = 50) =>
  useQuery({
    queryKey: qk.events(type),
    queryFn: () =>
      api<EventItem[]>(`/api/events?limit=${limit}${type === "all" ? "" : `&type=${type}`}`),
  });
