import { render, screen } from "@testing-library/react";
import { StatusChip } from "./StatusChip";

describe("StatusChip", () => {
  it.each([
    ["all_good", "All good"],
    ["attention", "Needs attention"],
    ["alert", "Alert"],
  ] as const)("shows text for %s so colour is never the only signal", (status, label) => {
    render(<StatusChip status={status} />);
    expect(screen.getByRole("status")).toHaveTextContent(label);
    expect(screen.getByRole("status").querySelector("svg")).not.toBeNull();
  });
});
