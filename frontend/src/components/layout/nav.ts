import { HeartPulse, History, Settings2, type LucideIcon } from "lucide-react";

export const NAV_ITEMS: { to: string; label: string; Icon: LucideIcon }[] = [
  { to: "/family", label: "Today", Icon: HeartPulse },
  { to: "/history", label: "History", Icon: History },
  { to: "/setup", label: "Care setup", Icon: Settings2 },
];
