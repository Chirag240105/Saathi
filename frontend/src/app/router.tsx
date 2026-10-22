import { createBrowserRouter } from "react-router-dom";
import { AppShell } from "@/components/layout/AppShell";
import { CareSetupPage } from "@/pages/CareSetupPage";
import { ElderPage } from "@/pages/ElderPage";
import { FamilyDashboardPage } from "@/pages/FamilyDashboardPage";
import { HistoryPage } from "@/pages/HistoryPage";
import { LandingPage } from "@/pages/LandingPage";
import { NotFoundPage } from "@/pages/NotFoundPage";

export const router = createBrowserRouter([
  { path: "/", element: <LandingPage /> },
  { path: "/elder", element: <ElderPage /> },
  {
    element: <AppShell />,
    children: [
      { path: "/family", element: <FamilyDashboardPage /> },
      { path: "/history", element: <HistoryPage /> },
      { path: "/setup", element: <CareSetupPage /> },
    ],
  },
  { path: "*", element: <NotFoundPage /> },
]);
