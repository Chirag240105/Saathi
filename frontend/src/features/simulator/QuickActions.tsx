import { Button } from "@/components/ui/button";

export const QUICK_ACTIONS = [
  "What do I have today?",
  "I took my medicine",
  "I feel okay",
  "I feel unwell",
  "I need help",
] as const;

export function QuickActions({
  onPick,
  disabled,
}: {
  onPick: (text: string) => void;
  disabled?: boolean;
}) {
  return (
    <div className="flex flex-wrap justify-center gap-3" role="group" aria-label="Quick actions">
      {QUICK_ACTIONS.map((q) => (
        <Button
          key={q}
          size="elder"
          variant={q === "I need help" || q === "I feel unwell" ? "danger" : "outline"}
          disabled={disabled}
          onClick={() => onPick(q)}
        >
          {q}
        </Button>
      ))}
    </div>
  );
}
