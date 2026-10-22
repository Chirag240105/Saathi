import { format, isToday, isTomorrow, formatDistanceToNowStrict } from "date-fns";

export const clock = (iso: string) => format(new Date(iso), "h:mm a");

export function dayAndTime(iso: string): string {
  const d = new Date(iso);
  const day = isToday(d) ? "Today" : isTomorrow(d) ? "Tomorrow" : format(d, "EEE d MMM");
  return `${day}, ${format(d, "h:mm a")}`;
}

export const ago = (iso: string) => `${formatDistanceToNowStrict(new Date(iso))} ago`;
export const MOOD_EMOJI = { good: "😊", okay: "🙂", unwell: "😟" } as const;
