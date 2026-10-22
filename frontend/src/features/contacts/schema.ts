import { z } from "zod";

export const contactSchema = z.object({
  name: z.string().trim().min(1, "Enter a name").max(80),
  telegram_chat_id: z
    .string()
    .trim()
    .regex(/^(-?\d+)?$/, "A chat ID is only digits, like 123456789"),
  role: z.string().max(40),
});
export type ContactForm = z.infer<typeof contactSchema>;
