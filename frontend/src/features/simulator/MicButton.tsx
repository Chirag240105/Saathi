import { motion } from "framer-motion";
import { Mic, Square } from "lucide-react";

export function MicButton({
  listening,
  disabled,
  onClick,
}: {
  listening: boolean;
  disabled?: boolean;
  onClick: () => void;
}) {
  return (
    <div className="relative flex h-40 w-40 items-center justify-center">
      {listening && (
        <motion.span
          aria-hidden="true"
          className="absolute inset-0 rounded-full bg-teal/30"
          animate={{ scale: [1, 1.35, 1], opacity: [0.6, 0, 0.6] }}
          transition={{ duration: 1.6, repeat: Infinity }}
        />
      )}
      <motion.button
        type="button"
        onClick={onClick}
        disabled={disabled}
        whileTap={{ scale: 0.95 }}
        animate={listening ? { scale: [1, 1.06, 1] } : { scale: 1 }}
        transition={listening ? { duration: 1.2, repeat: Infinity } : undefined}
        aria-pressed={listening}
        aria-label={listening ? "Stop listening" : "Start talking to Saathi"}
        className="relative flex h-32 w-32 items-center justify-center rounded-full bg-teal text-white shadow-lift hover:bg-teal-dark disabled:opacity-50"
      >
        {listening ? (
          <Square className="h-12 w-12" aria-hidden="true" />
        ) : (
          <Mic className="h-14 w-14" aria-hidden="true" />
        )}
      </motion.button>
    </div>
  );
}
