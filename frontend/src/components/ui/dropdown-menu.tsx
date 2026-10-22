import * as M from "@radix-ui/react-dropdown-menu";
import type { ComponentProps } from "react";

export const DropdownMenu = M.Root;
export const DropdownMenuTrigger = M.Trigger;
export function DropdownMenuContent(p: ComponentProps<typeof M.Content>) {
  return (
    <M.Portal>
      <M.Content
        align="end"
        sideOffset={6}
        className="z-50 min-w-48 rounded-control bg-surface p-1 shadow-lift"
        {...p}
      />
    </M.Portal>
  );
}
export function DropdownMenuItem(p: ComponentProps<typeof M.Item>) {
  return (
    <M.Item
      className="flex min-h-tap cursor-pointer items-center gap-2 rounded-control px-3 font-bold outline-none data-[highlighted]:bg-teal-wash"
      {...p}
    />
  );
}
