import { NavLink, Outlet } from "react-router-dom";
import { Logo } from "@/components/common/Logo";
import { cn } from "@/lib/utils";
import { NAV_ITEMS } from "./nav";
import { TopBar } from "./TopBar";

const linkCls = ({ isActive }: { isActive: boolean }) =>
  cn(
    "flex min-h-tap items-center gap-3 rounded-control px-4 font-bold transition-colors",
    isActive ? "bg-teal text-white" : "text-ink hover:bg-sand-deep",
  );

export function AppShell() {
  return (
    <div className="min-h-screen md:grid md:grid-cols-[15rem_1fr]">
      <aside className="hidden border-r border-line bg-surface p-5 md:block">
        <NavLink to="/" aria-label="Saathi home" className="mb-8 block">
          <Logo />
        </NavLink>
        <nav aria-label="Main" className="flex flex-col gap-1">
          {NAV_ITEMS.map(({ to, label, Icon }) => (
            <NavLink key={to} to={to} className={linkCls}>
              <Icon className="h-5 w-5" aria-hidden="true" />
              {label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <div className="flex min-w-0 flex-col pb-24 md:pb-0">
        <TopBar />
        <main id="main" className="mx-auto w-full max-w-6xl flex-1 p-4 md:p-8">
          <Outlet />
        </main>
      </div>
      <nav
        aria-label="Main"
        className="fixed inset-x-0 bottom-0 z-20 grid grid-cols-3 border-t border-line bg-surface pb-[env(safe-area-inset-bottom)] md:hidden"
      >
        {NAV_ITEMS.map(({ to, label, Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                "flex min-h-[3.75rem] flex-col items-center justify-center gap-0.5 text-sm font-bold",
                isActive ? "text-teal-dark" : "text-ink-soft",
              )
            }
          >
            <Icon className="h-6 w-6" aria-hidden="true" />
            {label}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
