import { useState } from "react";
import type { Activity } from "../types/evm";
import StatusBadge from "./StatusBadge";

const INITIAL_VISIBLE = 5;

interface ActivityTableProps {
  activities: Activity[];
  onEdit: (activity: Activity) => void;
  onDelete: (activity: Activity) => void;
  onNew: () => void;
}

export default function ActivityTable({
  activities,
  onEdit,
  onDelete,
  onNew,
}: ActivityTableProps) {
  const [expanded, setExpanded] = useState(false);

  const hasMore = activities.length > INITIAL_VISIBLE;
  const visible = expanded ? activities : activities.slice(0, INITIAL_VISIBLE);
  const remaining = activities.length - INITIAL_VISIBLE;

  return (
    <div className="activity-table">
      <div className="activity-table__header">
        <h3>Actividades</h3>
        <button className="btn btn--primary" onClick={onNew}>
          + Nueva actividad
        </button>
      </div>

      {activities.length === 0 ? (
        <p className="empty-state">No hay actividades registradas.</p>
      ) : (
        <>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Nombre</th>
                  <th>BAC</th>
                  <th>% Plan.</th>
                  <th>% Real</th>
                  <th>Costo Real</th>
                  <th>CPI</th>
                  <th>SPI</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {visible.map((act) => (
                  <tr key={act.id}>
                    <td>{act.name}</td>
                    <td className="num">
                      ${act.bac.toLocaleString("es-CO", { minimumFractionDigits: 2 })}
                    </td>
                    <td className="num">{act.planned_percentage}%</td>
                    <td className="num">{act.actual_percentage}%</td>
                    <td className="num">
                      ${act.actual_cost.toLocaleString("es-CO", { minimumFractionDigits: 2 })}
                    </td>
                    <td>
                      <StatusBadge
                        status={act.evm.estado_cpi}
                        value={act.evm.cpi}
                        reason={act.evm.razon_cpi}
                      />
                    </td>
                    <td>
                      <StatusBadge
                        status={act.evm.estado_spi}
                        value={act.evm.spi}
                        reason={act.evm.razon_spi}
                      />
                    </td>
                    <td className="actions">
                      <button
                        className="btn btn--icon"
                        title="Editar actividad"
                        onClick={() => onEdit(act)}
                      >
                        ✏️
                      </button>
                      <button
                        className="btn btn--icon"
                        title="Eliminar actividad"
                        onClick={() => onDelete(act)}
                      >
                        🗑️
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {hasMore && (
            <button
              className="btn btn--link activity-table__toggle"
              onClick={() => setExpanded(!expanded)}
            >
              {expanded
                ? "Ver menos"
                : `Ver más (${remaining} ${remaining === 1 ? "actividad restante" : "actividades restantes"})`}
            </button>
          )}
        </>
      )}
    </div>
  );
}
