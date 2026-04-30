import type { ProjectListItem } from "../types/evm";
import StatusBadge from "./StatusBadge";

interface ProjectCardProps {
  project: ProjectListItem;
  onClick: () => void;
  onEdit: () => void;
  onDelete: () => void;
}

export default function ProjectCard({
  project,
  onClick,
  onEdit,
  onDelete,
}: ProjectCardProps) {
  const { evm_consolidado } = project;

  return (
    <div className="card" onClick={onClick}>
      <div className="card__header">
        <h3 className="card__title">{project.name}</h3>
        <div className="card__actions" onClick={(e) => e.stopPropagation()}>
          <button
            type="button"
            className="btn btn--icon"
            title="Editar proyecto"
            onClick={onEdit}
          >
            ✏️
          </button>
          <button
            type="button"
            className="btn btn--icon"
            title="Eliminar proyecto"
            onClick={onDelete}
          >
            🗑️
          </button>
        </div>
      </div>

      {project.description && (
        <p className="card__description">{project.description}</p>
      )}

      <div className="card__meta">
        <span className="card__activity-count">
          {project.total_actividades}{" "}
          {project.total_actividades === 1 ? "actividad" : "actividades"}
        </span>
        <span className="card__bac">
          BAC: ${evm_consolidado.bac_total.toLocaleString("es-CO", { minimumFractionDigits: 2 })}
        </span>
      </div>

      <div className="card__indicators">
        <div className="card__indicator">
          <span className="card__indicator-label">CPI</span>
          <StatusBadge
            status={evm_consolidado.estado_cpi}
            value={evm_consolidado.cpi}
            reason={evm_consolidado.razon_cpi}
          />
        </div>
        <div className="card__indicator">
          <span className="card__indicator-label">SPI</span>
          <StatusBadge
            status={evm_consolidado.estado_spi}
            value={evm_consolidado.spi}
            reason={evm_consolidado.razon_spi}
          />
        </div>
      </div>
    </div>
  );
}
