import * as D from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import type { ReactNode } from "react";
import { cn } from "@/lib/utils";

export const Dialog = D.Root;
export const DialogTrigger = D.Trigger;
export const DialogClose = D.Close;
export const DialogTitle = D.Title;
export const DialogDescription = D.Description;

/** side="right" renders it as a sheet (used for the mobile tool-call panel). */
export function DialogContent({
  children,
  side = "center",
  className,
}: {
  children: ReactNode;
  side?: "center" | "right";
  className?: string;
}) {
  return (
    <D.Portal>
      <D.Overlay className="fixed inset-0 z-40 bg-ink/40" />
      <D.Content
        className={cn(
          "fixed z-50 overflow-y-auto bg-surface p-6 shadow-lift",
          side === "center"
            ? "left-1/2 top-1/2 max-h-[90vh] w-[calc(100%-2rem)] max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-card"
            : "inset-y-0 right-0 w-[min(26rem,100%)]",
          className,
        )}
      >
        {children}
        <D.Close
          aria-label="Close"
          className="absolute right-3 top-3 flex min-h-tap min-w-tap items-center justify-center rounded-full hover:bg-sand-deep"
        >
          <X className="h-5 w-5" aria-hidden="true" />
        </D.Close>
      </D.Content>
    </D.Portal>
  );
}
