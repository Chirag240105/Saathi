import { AnimatePresence, motion } from "framer-motion";
import { useEffect, useRef } from "react";
import { cn } from "@/lib/utils";
import type { Message } from "./store";

function Avatar() {
  return (
    <span
      aria-hidden="true"
      className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-teal text-2xl text-white"
    >
      🪔
    </span>
  );
}

export function Transcript({
  messages,
  thinking,
  interim,
}: {
  messages: Message[];
  thinking: boolean;
  interim: string;
}) {
  const end = useRef<HTMLDivElement>(null);
  useEffect(
    () => end.current?.scrollIntoView?.({ behavior: "smooth", block: "end" }),
    [messages, thinking, interim],
  );

  return (
    <div
      aria-live="polite"
      aria-label="Conversation"
      className="flex max-h-[24rem] min-h-[10rem] flex-col gap-4 overflow-y-auto rounded-card bg-surface p-4 shadow-card"
    >
      <AnimatePresence initial={false}>
        {messages.map((m) => (
          <motion.div
            key={m.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className={cn("flex items-start gap-3", m.role === "elder" && "flex-row-reverse")}
          >
            {m.role === "saathi" && <Avatar />}
            <p
              className={cn(
                "max-w-[85%] rounded-card px-5 py-3 text-2xl leading-snug",
                m.role === "saathi" ? "bg-teal-wash text-ink" : "bg-sand-deep text-ink",
              )}
            >
              <span className="sr-only">
                {m.role === "saathi" ? "Saathi says: " : "You said: "}
              </span>
              {m.text}
            </p>
          </motion.div>
        ))}
      </AnimatePresence>
      {interim && (
        <p className="self-end rounded-card bg-sand-deep/60 px-5 py-3 text-2xl italic text-ink-soft">
          {interim}…
        </p>
      )}
      {thinking && (
        <div className="flex items-center gap-3 text-xl text-ink-soft" role="status">
          <Avatar /> Saathi is thinking…
        </div>
      )}
      <div ref={end} />
    </div>
  );
}
