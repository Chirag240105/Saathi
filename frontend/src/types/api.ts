import type { OverallStatus } from "./status";

export type Mood = "good" | "okay" | "unwell";
export type DoseStatus = "taken" | "pending" | "missed";
export type EventType = "concern" | "missed_dose" | "unwell";

export interface Dose {
  medication_id: number;
  name: string;
  dose: string | null;
  scheduled_for: string;
  time: string;
  status: DoseStatus;
}
export interface EventItem {
  id: number;
  type: EventType;
  severity: string;
  message: string;
  created_at: string;
  notified: boolean;
  delivery: string;
}
export interface StatusData {
  elder: { id: number; name: string; age: number | null };
  overall: OverallStatus;
  server_time: string;
  doses: Dose[];
  last_checkin: { mood: Mood; note: string | null; created_at: string } | null;
  next_appointment: { id: number; title: string; starts_at: string } | null;
  recent_events: EventItem[];
}
export interface ToolCallItem {
  id: number;
  tool_name: string;
  inputs: Record<string, unknown>;
  result: string;
  duration_ms: number;
  success: boolean;
  source: "alexa" | "simulator" | "inspector";
  created_at: string;
}
export interface HistoryDay {
  date: string;
  taken: number;
  missed: number;
  pending: number;
  mood: Mood | null;
  mood_score: number | null;
}
export interface Medication {
  id: number;
  name: string;
  aliases: string[];
  dose: string | null;
  times: string[];
}
export interface Appointment {
  id: number;
  title: string;
  starts_at: string;
}
export interface Contact {
  id: number;
  name: string;
  telegram_chat_id: string | null;
  role: string | null;
}
export interface ChatResponse {
  reply: string;
  used_llm: boolean;
  tool_calls: {
    name: string;
    arguments: Record<string, unknown>;
    result: string;
    duration_ms: number;
    success: boolean;
  }[];
}
