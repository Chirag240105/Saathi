import { motion } from "framer-motion";
import { Mic, Users } from "lucide-react";
import { Link } from "react-router-dom";
import { Logo } from "@/components/common/Logo";
import { EMERGENCY_LINE } from "@/lib/constants";

const CHOICES = [
  {
    to: "/elder",
    Icon: Mic,
    title: "I am the elder",
    body: "Talk to Saathi about your medicines, your day and how you feel.",
    cls: "bg-teal text-white hover:bg-teal-dark",
  },
  {
    to: "/family",
    Icon: Users,
    title: "I am family",
    body: "See today at a glance and get told straight away if something is wrong.",
    cls: "bg-surface text-ink hover:bg-teal-wash",
  },
];

export function LandingPage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col justify-center gap-10 p-6 md:p-10">
      <header className="flex flex-col gap-4">
        <Logo />
        <h1 className="max-w-2xl text-4xl font-bold md:text-5xl">
          Someone is always listening for your parents.
        </h1>
        <p className="max-w-xl text-lg text-ink-soft">
          Saathi reminds your mother or father about medicines, hears how they feel, and tells you
          the moment something is wrong.
        </p>
      </header>

      <h2 className="sr-only">Who is using Saathi?</h2>
      <div className="grid gap-5 md:grid-cols-2">
        {CHOICES.map(({ to, Icon, title, body, cls }, i) => (
          <motion.div
            key={to}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 * i, duration: 0.35 }}
          >
            <Link
              to={to}
              className={`flex min-h-[11rem] flex-col justify-between gap-4 rounded-card p-7 shadow-card transition-colors ${cls}`}
            >
              <Icon className="h-10 w-10" aria-hidden="true" />
              <span>
                <span className="block text-3xl font-bold">{title}</span>
                <span className="mt-1 block text-lg opacity-90">{body}</span>
              </span>
            </Link>
          </motion.div>
        ))}
      </div>

      <footer className="rounded-control bg-amber-wash p-4 text-amber-ink">
        <p className="font-bold">Saathi reminds and keeps a record. It does not give medical advice.</p>
        <p>{EMERGENCY_LINE}</p>
      </footer>
    </main>
  );
}
