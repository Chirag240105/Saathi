import { render, screen } from "@testing-library/react";
import { ToolCallList } from "./ToolCallLog";
import type { ToolCallItem } from "@/types/api";

const call = (over: Partial<ToolCallItem>): ToolCallItem => ({
  id: 1,
  tool_name: "report_concern",
  inputs: { message: "I feel dizzy" },
  result: "I have told Rohan.",
  duration_ms: 42,
  success: true,
  source: "simulator",
  created_at: new Date().toISOString(),
  ...over,
});

describe("ToolCallList", () => {
  it("shows tool name, inputs, result, duration and status text", () => {
    render(
      <ToolCallList
        calls={[call({}), call({ id: 2, tool_name: "daily_checkin", success: false })]}
      />,
    );
    expect(screen.getByText("report_concern")).toBeInTheDocument();
    expect(screen.getAllByText(/I feel dizzy/)).toHaveLength(2);
    expect(screen.getAllByText("I have told Rohan.", { selector: "p" })).toHaveLength(2);
    expect(screen.getByText(/ok · 42 ms/)).toBeInTheDocument();
    expect(screen.getByText(/failed/)).toBeInTheDocument();
  });

  it("shows an empty state when there are no calls", () => {
    render(<ToolCallList calls={[]} />);
    expect(screen.getByText("No tool calls yet")).toBeInTheDocument();
  });
});
