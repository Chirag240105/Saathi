import { z } from "zod";

export const appointmentSchema = z
  .object({
    title: z.string().trim().min(1, "Say what the appointment is for").max(120),
    date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "Choose a date"),
    time: z.string().regex(/^\d{2}:\d{2}$/, "Choose a time"),
  })
  .refine((v) => new Date(`${v.date}T${v.time}`).getTime() > Date.now(), {
    message: "Pick a time in the future",
    path: ["time"],
  });
export type AppointmentForm = z.infer<typeof appointmentSchema>;
