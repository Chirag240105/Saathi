import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

export function NotFoundPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center gap-4 p-6 text-center">
      <h1 className="text-3xl font-bold">We could not find that page</h1>
      <p className="text-ink-soft">The link may be old. Start again from the home page.</p>
      <Button asChild>
        <Link to="/">Go to home</Link>
      </Button>
    </main>
  );
}
