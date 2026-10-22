import * as T from "@radix-ui/react-tooltip";
import type { ReactNode } from "react";

export const TooltipProvider = T.Provider;

export function Tip({ label, children }: { label: string; children: ReactNode }) {
  return (
    <T.Root delayDuration={150}>
      <T.Trigger asChild>{children}</T.Trigger>
      <T.Portal>
        <T.Content
          sideOffset={6}
          className="z-50 max-w-xs rounded-control bg-ink px-3 py-2 text-sm text-white"
        >
          {label}
        </T.Content>
      </T.Portal>
    </T.Root>
  );
}
