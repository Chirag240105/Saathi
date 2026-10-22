import { create } from "zustand";

export interface Message {
  id: number;
  role: "elder" | "saathi";
  text: string;
}

interface SimState {
  messages: Message[];
  thinking: boolean;
  speakReplies: boolean;
  add: (role: Message["role"], text: string) => void;
  setThinking: (v: boolean) => void;
  setSpeak: (v: boolean) => void;
  reset: () => void;
}

const GREETING: Message = {
  id: 0,
  role: "saathi",
  text: "Namaste. I am here with you. Tap the microphone, or tap one of the buttons below.",
};
let nextId = 1;

export const useSimStore = create<SimState>((set) => ({
  messages: [GREETING],
  thinking: false,
  speakReplies: true,
  add: (role, text) => set((s) => ({ messages: [...s.messages, { id: nextId++, role, text }] })),
  setThinking: (thinking) => set({ thinking }),
  setSpeak: (speakReplies) => set({ speakReplies }),
  reset: () => set({ messages: [GREETING], thinking: false }),
}));
