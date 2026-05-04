import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import type { ProjectListItem } from "../types/evm";
import {
  getProjects,
  createProject,
  updateProject,
  deleteProject,
} from "../api/client";
import ProjectCard from "../components/ProjectCard";
import ProjectModal from "../components/ProjectModal";
import ConfirmDialog from "../components/ConfirmDialog";

export default function ProjectListPage() {
  const navigate = useNavigate();

  const [projects, setProjects] = useState<ProjectListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal crear/editar
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<ProjectListItem | null>(null);

  // Diálogo de eliminación
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingProject, setDeletingProject] = useState<ProjectListItem | null>(null);

  // Carga inicial y recarga
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;
    getProjects()
      .then((data) => {
        if (!cancelled) {
          setProjects(data);
          setError(null);
        }
      })
      .catch(() => {
        if (!cancelled) setError("No se pudieron cargar los proyectos.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [reloadKey]);

  function reload() {
    setLoading(true);
    setReloadKey((k) => k + 1);
  }

  // ── Crear / Editar ──────────────────────────────────────────────────────

  function handleNewClick() {
    setEditingProject(null);
    setModalOpen(true);
  }

  function handleEditClick(project: ProjectListItem) {
    setEditingProject(project);
    setModalOpen(true);
  }

  async function handleSave(data: { name: string; description: string | null }) {
    try {
      if (editingProject) {
        await updateProject(editingProject.id, data);
      } else {
        await createProject(data);
      }
      setModalOpen(false);
      reload();
    } catch {
      setError("No se pudo guardar el proyecto.");
    }
  }

  // ── Eliminar ────────────────────────────────────────────────────────────

  function handleDeleteClick(project: ProjectListItem) {
    setDeletingProject(project);
    setDeleteDialogOpen(true);
  }

  async function handleConfirmDelete() {
    if (!deletingProject) return;
    try {
      await deleteProject(deletingProject.id);
      setDeleteDialogOpen(false);
      setDeletingProject(null);
      reload();
    } catch {
      setError("No se pudo eliminar el proyecto.");
    }
  }

  // ── Render ──────────────────────────────────────────────────────────────

  if (loading) {
    return <div className="page-status">Cargando proyectos…</div>;
  }

  if (error) {
    return (
      <div className="page-status page-status--error">
        <p>{error}</p>
        <button className="btn btn--primary" onClick={reload}>
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="page">
      <div className="page__header">
        <h1>Proyectos</h1>
        <button className="btn btn--primary" onClick={handleNewClick}>
          + Nuevo
        </button>
      </div>

      {projects.length === 0 ? (
        <div className="empty-state">
          <p>No hay proyectos registrados.</p>
          <button className="btn btn--primary" onClick={handleNewClick}>
            Crear primer proyecto
          </button>
        </div>
      ) : (
        <div className="card-grid">
          {projects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onClick={() => navigate(`/projects/${project.id}`)}
              onEdit={() => handleEditClick(project)}
              onDelete={() => handleDeleteClick(project)}
            />
          ))}
        </div>
      )}

      <ProjectModal
        open={modalOpen}
        project={editingProject}
        onSave={handleSave}
        onCancel={() => setModalOpen(false)}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        title="Eliminar proyecto"
        message={
          deletingProject
            ? `¿Desea eliminar el proyecto "${deletingProject.name}"? Se eliminarán ${deletingProject.total_actividades} ${deletingProject.total_actividades === 1 ? "actividad" : "actividades"}. Esta acción no se puede deshacer.`
            : ""
        }
        onConfirm={handleConfirmDelete}
        onCancel={() => {
          setDeleteDialogOpen(false);
          setDeletingProject(null);
        }}
      />
    </div>
  );
}
