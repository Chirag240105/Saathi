import { z } from "zod";

const HHMM = /^([01]\d|2[0-3]):[0-5]\d$/;
export const splitList = (v: string) =>
  v
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);

export const medicineSchema = z.object({
  name: z.string().trim().min(1, "Enter the medicine name").max(80),
  aliases: z.string().max(200),
  dose: z.string().max(60),
  times: z
    .string()
    .refine(
      (v) => splitList(v).length > 0 && splitList(v).every((t) => HHMM.test(t)),
      "Use 24-hour times like 08:00, 20:00",
    ),
});
export type MedicineForm = z.infer<typeof medicineSchema>;
