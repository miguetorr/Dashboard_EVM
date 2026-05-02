import { Routes, Route, Navigate } from "react-router-dom";
import ProjectListPage from "./pages/ProjectListPage";
import ProjectDashboardPage from "./pages/ProjectDashboardPage";

export default function App() {
  return (
    <div className="app">
      <header className="app-header">
        <a href="/projects" className="app-header__brand">
          EVM Tracker
        </a>
      </header>

      <main className="app-main">
        <Routes>
          <Route path="/projects" element={<ProjectListPage />} />
          <Route path="/projects/:id" element={<ProjectDashboardPage />} />
          <Route path="*" element={<Navigate to="/projects" replace />} />
        </Routes>
      </main>
    </div>
  );
}
