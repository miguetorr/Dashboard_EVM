import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import type { ProjectDetail, Activity } from "../types/evm";
import {
  getProjectDetail,
  createActivity,
  updateActivity,
  deleteActivity,
} from "../api/client";
import ProjectSelector from "../components/ProjectSelector";
import EVMIndicators from "../components/EVMIndicators";
import ActivityTable from "../components/ActivityTable";
import ActivityModal from "../components/ActivityModal";
import EVMChart from "../components/EVMChart";
import EVMGlossary from "../components/EVMGlossary";
import ConfirmDialog from "../components/ConfirmDialog";

export default function ProjectDashboardPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [project, setProject] = useState<ProjectDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Modal de actividad
  const [actModalOpen, setActModalOpen] = useState(false);
  const [editingActivity, setEditingActivity] = useState<Activity | null>(null);

  // Diálogo de eliminación de actividad
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [deletingActivity, setDeletingActivity] = useState<Activity | null>(null);

  // Carga y recarga
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    if (!id) return;
    let cancelled = false;
    getProjectDetail(id)
      .then((data) => {
        if (!cancelled) {
          setProject(data);
          setError(null);
        }
      })
      .catch(() => {
        if (!cancelled) setError("No se pudo cargar el proyecto.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [id, reloadKey]);

  function reload() {
    setLoading(true);
    setReloadKey((k) => k + 1);
  }

  // ── Crear / Editar actividad ────────────────────────────────────────────

  function handleNewActivity() {
    setEditingActivity(null);
    setActModalOpen(true);
  }

  function handleEditActivity(activity: Activity) {
    setEditingActivity(activity);
    setActModalOpen(true);
  }

  async function handleSaveActivity(data: {
    name: string;
    bac: number;
    planned_percentage: number;
    actual_percentage: number;
    actual_cost: number;
  }) {
    if (!id) return;
    try {
      if (editingActivity) {
        await updateActivity(id, editingActivity.id, data);
      } else {
        await createActivity(id, data);
      }
      setActModalOpen(false);
      reload();
    } catch {
      setError("No se pudo guardar la actividad.");
    }
  }

  // ── Eliminar actividad ──────────────────────────────────────────────────

  function handleDeleteClick(activity: Activity) {
    setDeletingActivity(activity);
    setDeleteDialogOpen(true);
  }

  async function handleConfirmDelete() {
    if (!id || !deletingActivity) return;
    try {
      await deleteActivity(id, deletingActivity.id);
      setDeleteDialogOpen(false);
      setDeletingActivity(null);
      reload();
    } catch {
      setError("No se pudo eliminar la actividad.");
    }
  }

  // ── Cambio rápido de proyecto ───────────────────────────────────────────

  function handleProjectChange(projectId: string) {
    navigate(`/projects/${projectId}`);
  }

  // ── Render ──────────────────────────────────────────────────────────────

  if (loading) {
    return <div className="page-status">Cargando dashboard…</div>;
  }

  if (error || !project) {
    return (
      <div className="page-status page-status--error">
        <p>{error ?? "Proyecto no encontrado."}</p>
        <button className="btn btn--primary" onClick={reload}>
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="page">
      <ProjectSelector
        currentProjectId={project.id}
        currentProjectName={project.name}
        onSelect={handleProjectChange}
      />

      {project.description && (
        <p className="page__description">{project.description}</p>
      )}

      <EVMIndicators data={project.evm_consolidado} />

      <EVMGlossary />

      <ActivityTable
        activities={project.actividades}
        onEdit={handleEditActivity}
        onDelete={handleDeleteClick}
        onNew={handleNewActivity}
      />

      <EVMChart activities={project.actividades} />

      <ActivityModal
        open={actModalOpen}
        activity={editingActivity}
        onSave={handleSaveActivity}
        onCancel={() => setActModalOpen(false)}
      />

      <ConfirmDialog
        open={deleteDialogOpen}
        title="Eliminar actividad"
        message={
          deletingActivity
            ? `¿Desea eliminar la actividad "${deletingActivity.name}"? Esta acción no se puede deshacer.`
            : ""
        }
        onConfirm={handleConfirmDelete}
        onCancel={() => {
          setDeleteDialogOpen(false);
          setDeletingActivity(null);
        }}
      />
    </div>
  );
}
