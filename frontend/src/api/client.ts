import axios from "axios";
import type {
  Activity,
  ActivityCreate,
  ActivityUpdate,
  ProjectCreate,
  ProjectDetail,
  ProjectListItem,
  Project,
  ProjectUpdate,
} from "../types/evm";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
  headers: { "Content-Type": "application/json" },
});

// ─────────────────────────────────────────────────────────────────────────────
// Proyectos
// ─────────────────────────────────────────────────────────────────────────────

export async function getProjects(): Promise<ProjectListItem[]> {
  const { data } = await api.get<ProjectListItem[]>("/projects");
  return data;
}

export async function getProjectDetail(projectId: string): Promise<ProjectDetail> {
  const { data } = await api.get<ProjectDetail>(`/projects/${projectId}`);
  return data;
}

export async function createProject(payload: ProjectCreate): Promise<Project> {
  const { data } = await api.post<Project>("/projects", payload);
  return data;
}

export async function updateProject(
  projectId: string,
  payload: ProjectUpdate,
): Promise<Project> {
  const { data } = await api.put<Project>(`/projects/${projectId}`, payload);
  return data;
}

export async function deleteProject(projectId: string): Promise<void> {
  await api.delete(`/projects/${projectId}`);
}

// ─────────────────────────────────────────────────────────────────────────────
// Actividades
// ─────────────────────────────────────────────────────────────────────────────

export async function getActivities(projectId: string): Promise<Activity[]> {
  const { data } = await api.get<Activity[]>(
    `/projects/${projectId}/activities`,
  );
  return data;
}

export async function createActivity(
  projectId: string,
  payload: ActivityCreate,
): Promise<Activity> {
  const { data } = await api.post<Activity>(
    `/projects/${projectId}/activities`,
    payload,
  );
  return data;
}

export async function updateActivity(
  projectId: string,
  activityId: string,
  payload: ActivityUpdate,
): Promise<Activity> {
  const { data } = await api.put<Activity>(
    `/projects/${projectId}/activities/${activityId}`,
    payload,
  );
  return data;
}

export async function deleteActivity(
  projectId: string,
  activityId: string,
): Promise<void> {
  await api.delete(`/projects/${projectId}/activities/${activityId}`);
}
