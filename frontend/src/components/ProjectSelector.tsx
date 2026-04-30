import { useState, useEffect, useRef } from "react";
import type { ProjectListItem } from "../types/evm";
import { getProjects } from "../api/client";

interface ProjectSelectorProps {
  currentProjectId: string;
  currentProjectName: string;
  onSelect: (projectId: string) => void;
}

export default function ProjectSelector({
  currentProjectId,
  currentProjectName,
  onSelect,
}: ProjectSelectorProps) {
  const [open, setOpen] = useState(false);
  const [projects, setProjects] = useState<ProjectListItem[]>([]);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (open && projects.length === 0) {
      getProjects().then(setProjects).catch(() => {});
    }
  }, [open, projects.length]);

  // Cerrar al hacer click fuera
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setOpen(false);
      }
    }
    if (open) document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [open]);

  return (
    <nav className="breadcrumb" ref={dropdownRef}>
      <span className="breadcrumb__item">
        <a href="/projects" className="breadcrumb__link">
          Proyectos
        </a>
      </span>
      <span className="breadcrumb__separator">/</span>
      <span className="breadcrumb__item breadcrumb__item--current">
        <button
          className="breadcrumb__dropdown-trigger"
          onClick={() => setOpen(!open)}
        >
          {currentProjectName} ▾
        </button>

        {open && (
          <ul className="breadcrumb__dropdown">
            {projects.map((p) => (
              <li key={p.id}>
                <button
                  className={`breadcrumb__option ${p.id === currentProjectId ? "breadcrumb__option--active" : ""}`}
                  onClick={() => {
                    if (p.id !== currentProjectId) {
                      onSelect(p.id);
                    }
                    setOpen(false);
                  }}
                >
                  {p.name}
                </button>
              </li>
            ))}
          </ul>
        )}
      </span>
    </nav>
  );
}
