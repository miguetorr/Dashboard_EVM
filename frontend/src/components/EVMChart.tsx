import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import type { Activity } from "../types/evm";

interface EVMChartProps {
  activities: Activity[];
}

export default function EVMChart({ activities }: EVMChartProps) {
  if (activities.length === 0) {
    return (
      <div className="chart-empty">
        <p>No hay actividades para graficar.</p>
      </div>
    );
  }

  const chartData = activities.map((act) => ({
    name: act.name.length > 20 ? act.name.slice(0, 18) + "…" : act.name,
    PV: act.evm.pv,
    EV: act.evm.ev,
    AC: act.actual_cost,
  }));

  return (
    <div className="chart">
      <h3>Comparativa PV / EV / AC</h3>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={chartData} margin={{ top: 10, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip
            formatter={(value) =>
              `$${Number(value).toLocaleString("es-CO", { minimumFractionDigits: 2 })}`
            }
          />
          <Legend />
          <Bar dataKey="PV" fill="#8884d8" name="Valor Planificado (PV)" />
          <Bar dataKey="EV" fill="#82ca9d" name="Valor Ganado (EV)" />
          <Bar dataKey="AC" fill="#ffc658" name="Costo Real (AC)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
