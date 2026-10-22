import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QUICK_ACTIONS, QuickActions } from "./QuickActions";

describe("QuickActions", () => {
  it("renders the five big chips and reports the tapped phrase", async () => {
    const onPick = vi.fn();
    render(<QuickActions onPick={onPick} />);
    expect(screen.getAllByRole("button")).toHaveLength(5);
    await userEvent.click(screen.getByRole("button", { name: "I feel unwell" }));
    expect(onPick).toHaveBeenCalledWith("I feel unwell");
    expect(QUICK_ACTIONS).toContain("What do I have today?");
  });
});
