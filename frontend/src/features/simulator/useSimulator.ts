import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { qk } from "@/lib/queryKeys";
import { speak } from "@/lib/speech";
import type { ChatResponse } from "@/types/api";
import { useSimStore } from "./store";

/** Sends what the elder said to the backend agent, which calls the real MCP server. */
export function useSimulator() {
  const qc = useQueryClient();
  const { add, setThinking } = useSimStore();

  const mutation = useMutation({
    mutationFn: (text: string) =>
      api<ChatResponse>("/api/simulator/chat", { method: "POST", body: { text }, write: true }),
    onMutate: (text) => {
      add("elder", text);
      setThinking(true);
    },
    onSuccess: (res) => {
      add("saathi", res.reply);
      if (useSimStore.getState().speakReplies) speak(res.reply);
      if (
        res.tool_calls.some(
          (c) =>
            c.name === "report_concern" ||
            (c.name === "daily_checkin" && c.arguments.mood === "unwell"),
        )
      ) {
        toast.warning("Your family has been told");
      }
      for (const k of [qk.status, qk.toolCalls, ["events"]])
        void qc.invalidateQueries({ queryKey: k });
    },
    onError: (e) => {
      const msg = "Sorry, I could not reach Saathi just now. Please try again.";
      add("saathi", msg);
      toast.error(e instanceof Error ? e.message : msg);
    },
    onSettled: () => setThinking(false),
  });

  return {
    send: (text: string) => text.trim() && mutation.mutate(text.trim()),
    busy: mutation.isPending,
  };
}
