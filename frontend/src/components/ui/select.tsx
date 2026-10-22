import * as S from "@radix-ui/react-select";
import { Check, ChevronDown } from "lucide-react";

export function Select({
  value,
  onValueChange,
  options,
  label,
}: {
  value: string;
  onValueChange: (v: string) => void;
  options: { value: string; label: string }[];
  label: string;
}) {
  return (
    <S.Root value={value} onValueChange={onValueChange}>
      <S.Trigger
        aria-label={label}
        className="inline-flex min-h-tap items-center gap-2 rounded-control border-2 border-line bg-surface px-4 font-bold"
      >
        <S.Value />
        <ChevronDown className="h-4 w-4" aria-hidden="true" />
      </S.Trigger>
      <S.Portal>
        <S.Content
          className="z-50 rounded-control bg-surface p-1 shadow-lift"
          position="popper"
          sideOffset={6}
        >
          <S.Viewport>
            {options.map((o) => (
              <S.Item
                key={o.value}
                value={o.value}
                className="flex min-h-tap cursor-pointer items-center justify-between gap-6 rounded-control px-3 font-bold outline-none data-[highlighted]:bg-teal-wash"
              >
                <S.ItemText>{o.label}</S.ItemText>
                <S.ItemIndicator>
                  <Check className="h-4 w-4" aria-hidden="true" />
                </S.ItemIndicator>
              </S.Item>
            ))}
          </S.Viewport>
        </S.Content>
      </S.Portal>
    </S.Root>
  );
}
