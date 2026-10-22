import { contactSchema } from "@/features/contacts/schema";
import { appointmentSchema } from "@/features/appointments/schema";
import { medicineSchema } from "./schema";

describe("form validation", () => {
  it("medicine needs a name and 24-hour times", () => {
    expect(
      medicineSchema.safeParse({ name: "Iron", aliases: "", dose: "", times: "08:00, 20:00" })
        .success,
    ).toBe(true);
    expect(
      medicineSchema.safeParse({ name: "", aliases: "", dose: "", times: "08:00" }).success,
    ).toBe(false);
    expect(
      medicineSchema.safeParse({ name: "Iron", aliases: "", dose: "", times: "8am" }).success,
    ).toBe(false);
  });
  it("contact chat id must be digits (or empty)", () => {
    expect(
      contactSchema.safeParse({ name: "A", telegram_chat_id: "123456", role: "" }).success,
    ).toBe(true);
    expect(contactSchema.safeParse({ name: "A", telegram_chat_id: "", role: "" }).success).toBe(
      true,
    );
    expect(contactSchema.safeParse({ name: "A", telegram_chat_id: "abc", role: "" }).success).toBe(
      false,
    );
  });
  it("appointment must be in the future", () => {
    expect(
      appointmentSchema.safeParse({ title: "Dentist", date: "2001-01-01", time: "10:00" }).success,
    ).toBe(false);
    expect(
      appointmentSchema.safeParse({ title: "Dentist", date: "2099-01-01", time: "10:00" }).success,
    ).toBe(true);
  });
});
