import { useState, useEffect } from "react";
import type { ProjectListItem } from "../types/evm";

interface ProjectModalProps {
  open: boolean;
  project: ProjectListItem | null;
  onSave: (data: { name: string; description: string | null }) => void;
  onCancel: () => void;
}

export default function ProjectModal({
  open,
  project,
  onSave,
  onCancel,
}: ProjectModalProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (open) {
      setName(project?.name ?? "");
      setDescription(project?.description ?? "");
    }
  }, [open, project]);

  if (!open) return null;

  const isEdit = project !== null;
  const canSave = name.trim().length > 0;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!canSave) return;
    onSave({
      name: name.trim(),
      description: description.trim() || null,
    });
  }

  return (
    <div className="dialog-overlay" onClick={onCancel}>
      <div className="dialog dialog--form" onClick={(e) => e.stopPropagation()}>
        <h3 className="dialog__title">
          {isEdit ? "Editar proyecto" : "Nuevo proyecto"}
        </h3>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="project-name">Nombre *</label>
            <input
              id="project-name"
              type="text"
              className="form-control"
              value={name}
              onChange={(e) => setName(e.target.value)}
              maxLength={255}
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="project-description">Descripción</label>
            <textarea
              id="project-description"
              className="form-control"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={3}
            />
          </div>

          <div className="dialog__actions">
            <button
              type="button"
              className="btn btn--secondary"
              onClick={onCancel}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="btn btn--primary"
              disabled={!canSave}
            >
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
