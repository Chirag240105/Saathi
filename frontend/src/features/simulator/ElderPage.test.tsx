import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { Providers } from "@/app/providers/Providers";
import { ElderPage } from "@/pages/ElderPage";

describe("ElderPage", () => {
  it("tapping a quick action sends it to the simulator chat endpoint and shows the reply", async () => {
    const fetchMock = vi.fn(async (url: string, init?: RequestInit) => {
      void init;
      const body = String(url).includes("/api/simulator/chat")
        ? {
            reply: "I have told Rohan and Anita. Please sit down and rest.",
            used_llm: false,
            tool_calls: [
              { name: "report_concern", arguments: {}, result: "x", duration_ms: 5, success: true },
            ],
          }
        : String(url).includes("/api/tool-calls")
          ? []
          : {
              doses: [],
              next_appointment: null,
              recent_events: [],
              elder: { id: 1, name: "S", age: 72 },
              overall: "all_good",
            };
      return new Response(JSON.stringify(body), { status: 200 });
    });
    vi.stubGlobal("fetch", fetchMock);
    render(
      <Providers>
        <MemoryRouter>
          <ElderPage />
        </MemoryRouter>
      </Providers>,
    );

    await userEvent.click(screen.getByRole("button", { name: "I feel unwell" }));

    await waitFor(() =>
      expect(screen.getByText(/I have told Rohan and Anita/)).toBeInTheDocument(),
    );
    const call = fetchMock.mock.calls.find(([u]) => String(u).includes("/api/simulator/chat"))!;
    expect(JSON.parse(String(call[1]?.body))).toEqual({ text: "I feel unwell" });
    expect(screen.getByText(/call your local emergency number/i)).toBeInTheDocument();
  });
});
