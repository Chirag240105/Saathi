import { useCallback, useEffect, useRef, useState } from "react";
import { recognitionCtor, type Recognition } from "@/lib/speech";

export function useSpeechRecognition(onFinal: (text: string) => void) {
  const Ctor = recognitionCtor();
  const rec = useRef<Recognition | null>(null);
  const [listening, setListening] = useState(false);
  const [interim, setInterim] = useState("");
  const [error, setError] = useState<string | null>(null);
  const cb = useRef(onFinal);
  useEffect(() => {
    cb.current = onFinal;
  }, [onFinal]);

  useEffect(() => () => rec.current?.abort(), []);

  const start = useCallback(() => {
    if (!Ctor) return;
    const r = new Ctor();
    r.lang = "en-IN";
    r.interimResults = true;
    r.continuous = false;
    r.onresult = (e) => {
      const last = e.results[e.results.length - 1];
      setInterim(last[0].transcript);
      if (last.isFinal) {
        setInterim("");
        cb.current(last[0].transcript);
      }
    };
    r.onerror = (e) => {
      setError(
        e.error === "not-allowed"
          ? "Microphone permission is blocked. You can type or tap a button instead."
          : "I could not hear you. Please try again.",
      );
      setListening(false);
    };
    r.onend = () => setListening(false);
    setError(null);
    rec.current = r;
    r.start();
    setListening(true);
  }, [Ctor]);

  const stop = useCallback(() => rec.current?.stop(), []);
  return { supported: Ctor !== null, listening, interim, error, start, stop };
}
