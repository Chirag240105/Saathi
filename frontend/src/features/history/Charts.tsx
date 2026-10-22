import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { format } from "date-fns";
import type { HistoryDay } from "@/types/api";

const TEAL = "#0f766e";
const CORAL = "#d9534f";
const INK = "#1e1b4b";
const MOODS = ["", "Unwell", "Okay", "Good"];

const short = (d: unknown) => format(new Date(`${String(d)}T00:00:00`), "d MMM");

export function AdherenceChart({ days }: { days: HistoryDay[] }) {
  return (
    <div role="img" aria-label="Bar chart of doses taken and missed per day" className="h-72">
      <ResponsiveContainer>
        <BarChart data={days} margin={{ left: -16 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="date" tickFormatter={short} fontSize={12} stroke={INK} />
          <YAxis allowDecimals={false} fontSize={12} stroke={INK} />
          <Tooltip labelFormatter={short} />
          <Legend />
          <Bar dataKey="taken" name="Taken" stackId="a" fill={TEAL} radius={[0, 0, 4, 4]} />
          <Bar dataKey="missed" name="Missed" stackId="a" fill={CORAL} radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function MoodChart({ days }: { days: HistoryDay[] }) {
  return (
    <div role="img" aria-label="Line chart of daily mood" className="h-64">
      <ResponsiveContainer>
        <LineChart data={days} margin={{ left: 8 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} />
          <XAxis dataKey="date" tickFormatter={short} fontSize={12} stroke={INK} />
          <YAxis
            domain={[1, 3]}
            ticks={[1, 2, 3]}
            tickFormatter={(v: number) => MOODS[v]}
            fontSize={12}
            width={56}
            stroke={INK}
          />
          <Tooltip labelFormatter={short} formatter={(v: unknown) => MOODS[Number(v)] ?? ""} />
          <Line
            type="monotone"
            dataKey="mood_score"
            name="Mood"
            stroke={TEAL}
            strokeWidth={3}
            dot={{ r: 4 }}
            connectNulls
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
