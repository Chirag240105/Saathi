import { Activity, ArrowLeft, Volume2 } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Switch } from "@/components/ui/switch";
import { Logo } from "@/components/common/Logo";
import { MicButton } from "@/features/simulator/MicButton";
import { QuickActions } from "@/features/simulator/QuickActions";
import { TodayCard } from "@/features/simulator/TodayCard";
import { Transcript } from "@/features/simulator/Transcript";
import { TypedInput } from "@/features/simulator/TypedInput";
import { useSimStore } from "@/features/simulator/store";
import { useSimulator } from "@/features/simulator/useSimulator";
import { useSpeechRecognition } from "@/features/simulator/useSpeechRecognition";
import { ToolCallLog } from "@/features/toolcalls/ToolCallLog";
import { EMERGENCY_LINE } from "@/lib/constants";
import { canSpeak, stopSpeaking } from "@/lib/speech";

export function ElderPage() {
  const { messages, thinking, speakReplies, setSpeak } = useSimStore();
  const { send, busy } = useSimulator();
  const { supported, listening, interim, error, start, stop } = useSpeechRecognition(send);

  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[1fr_26rem]">
      <main
        id="main"
        className="mx-auto flex w-full max-w-3xl flex-col items-center gap-6 p-4 text-2xl md:p-8"
      >
        <header className="flex w-full items-center justify-between">
          <Link
            to="/"
            className="flex min-h-tap items-center gap-2 text-lg font-bold"
            aria-label="Back to home"
          >
            <ArrowLeft className="h-5 w-5" aria-hidden="true" />
            <Logo />
          </Link>
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline" className="lg:hidden">
                <Activity className="h-5 w-5" aria-hidden="true" /> MCP activity
              </Button>
            </DialogTrigger>
            <DialogContent side="right">
              <DialogTitle className="sr-only">MCP activity</DialogTitle>
              <ToolCallLog />
            </DialogContent>
          </Dialog>
        </header>

        <TodayCard />
        <Transcript messages={messages} thinking={thinking} interim={interim} />

        {supported ? (
          <>
            <MicButton listening={listening} disabled={busy} onClick={listening ? stop : start} />
            <p className="text-xl text-ink-soft" aria-live="polite">
              {listening ? "I am listening…" : "Tap the microphone and speak"}
            </p>
            {error && (
              <p role="alert" className="rounded-control bg-amber-wash p-3 text-lg text-amber-ink">
                {error}
              </p>
            )}
          </>
        ) : (
          <p role="note" className="rounded-control bg-amber-wash p-4 text-lg text-amber-ink">
            Voice input is not available in this browser, so please type or tap a button. Chrome or
            Edge work best.
          </p>
        )}

        <QuickActions onPick={send} disabled={busy} />
        {!supported && <TypedInput onSend={send} disabled={busy} />}

        {canSpeak() && (
          <label className="flex min-h-tap items-center gap-3 text-lg">
            <Switch
              checked={speakReplies}
              onCheckedChange={(v) => {
                setSpeak(v);
                if (!v) stopSpeaking();
              }}
              aria-label="Speak replies aloud"
            />
            <Volume2 className="h-5 w-5" aria-hidden="true" /> Speak replies aloud
          </label>
        )}
        {!canSpeak() && (
          <p className="text-lg text-ink-soft">
            Replies are shown on screen because spoken replies are not supported here.
          </p>
        )}

        <p
          role="note"
          className="rounded-control bg-coral-wash px-4 py-3 text-center text-lg font-bold text-coral-ink"
        >
          {EMERGENCY_LINE}
        </p>
      </main>

      <aside
        className="hidden border-l border-line bg-sand-deep/50 p-5 lg:block"
        aria-label="MCP activity panel"
      >
        <div className="sticky top-5 max-h-[calc(100vh-2.5rem)] overflow-y-auto">
          <ToolCallLog />
        </div>
      </aside>
    </div>
  );
}
