import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { qk } from "@/lib/queryKeys";

/** List + create + delete for a REST resource, with an optimistic delete. */
export function useCrud<T extends { id: number }, Input>(
  resource: "medications" | "appointments" | "contacts",
) {
  const qc = useQueryClient();
  const key = qk.list(resource);
  const list = useQuery({ queryKey: key, queryFn: () => api<T[]>(`/api/${resource}`) });

  const create = useMutation({
    mutationFn: (body: Input) => api<T>(`/api/${resource}`, { method: "POST", body, write: true }),
    onSuccess: () => {
      void qc.invalidateQueries({ queryKey: key });
      void qc.invalidateQueries({ queryKey: qk.status });
    },
  });

  const remove = useMutation({
    mutationFn: (id: number) =>
      api<void>(`/api/${resource}/${id}`, { method: "DELETE", write: true }),
    onMutate: async (id) => {
      await qc.cancelQueries({ queryKey: key });
      const prev = qc.getQueryData<T[]>(key);
      qc.setQueryData<T[]>(key, (old) => old?.filter((x) => x.id !== id));
      return { prev };
    },
    onError: (_e, _id, ctx) => qc.setQueryData(key, ctx?.prev),
    onSettled: () => {
      void qc.invalidateQueries({ queryKey: key });
      void qc.invalidateQueries({ queryKey: qk.status });
    },
  });

  return { list, create, remove };
}
