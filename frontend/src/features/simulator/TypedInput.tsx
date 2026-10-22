import { Send } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export function TypedInput({
  onSend,
  disabled,
}: {
  onSend: (t: string) => void;
  disabled?: boolean;
}) {
  const [text, setText] = useState("");
  const submit = () => {
    if (text.trim()) onSend(text);
    setText("");
  };
  return (
    <div className="flex w-full gap-2">
      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && submit()}
        aria-label="Type a message to Saathi"
        placeholder="Type here, for example: I took my BP tablet"
        className="min-h-tap-elder min-w-0 flex-1 rounded-control border-2 border-line bg-surface px-4 text-xl"
      />
      <Button size="elder" onClick={submit} disabled={disabled} aria-label="Send">
        <Send className="h-6 w-6" aria-hidden="true" />
      </Button>
    </div>
  );
}
