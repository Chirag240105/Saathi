import * as T from "@radix-ui/react-tabs";
import type { ComponentProps } from "react";
import { cn } from "@/lib/utils";

export const Tabs = T.Root;
export function TabsList({ className, ...p }: ComponentProps<typeof T.List>) {
  return (
    <T.List
      className={cn("mb-4 inline-flex gap-1 rounded-control bg-sand-deep p-1", className)}
      {...p}
    />
  );
}
export function TabsTrigger({ className, ...p }: ComponentProps<typeof T.Trigger>) {
  return (
    <T.Trigger
      className={cn(
        "min-h-tap rounded-control px-4 font-bold text-ink-soft data-[state=active]:bg-surface data-[state=active]:text-ink data-[state=active]:shadow-card",
        className,
      )}
      {...p}
    />
  );
}
export const TabsContent = T.Content;
