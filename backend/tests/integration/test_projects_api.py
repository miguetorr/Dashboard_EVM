"""Tests de integración para endpoints de proyectos."""

import uuid


FAKE_UUID = str(uuid.uuid4())


# ═════════════════════════════════════════════════════════════════════════════
# 8.2 — CRUD de proyectos
# ═════════════════════════════════════════════════════════════════════════════


class TestCreateProject:
    def test_crear_proyecto_exitoso(self, client):
        response = client.post(
            "/api/v1/projects",
            json={"name": "Portal Web", "description": "Rediseño completo"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Portal Web"
        assert data["description"] == "Rediseño completo"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_crear_proyecto_sin_descripcion(self, client):
        response = client.post(
            "/api/v1/projects",
            json={"name": "App Móvil"},
        )
        assert response.status_code == 201
        assert response.json()["description"] is None

    def test_crear_proyecto_nombre_vacio_422(self, client):
        response = client.post("/api/v1/projects", json={"name": ""})
        assert response.status_code == 422

    def test_crear_proyecto_sin_nombre_422(self, client):
        response = client.post("/api/v1/projects", json={})
        assert response.status_code == 422


class TestListProjects:
    def test_listar_sin_proyectos(self, client):
        response = client.get("/api/v1/projects")
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_con_proyectos(self, client, sample_project):
        response = client.get("/api/v1/projects")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        item = data[0]
        assert "total_actividades" in item
        assert "evm_consolidado" in item
        assert item["evm_consolidado"]["bac_total"] is not None

    def test_listar_incluye_conteo_actividades(self, client, sample_activity):
        response = client.get("/api/v1/projects")
        data = response.json()
        project_item = next(
            p for p in data if p["id"] == sample_activity["project_id"]
        )
        assert project_item["total_actividades"] == 1


class TestGetProjectDetail:
    def test_detalle_proyecto_existente(self, client, sample_project):
        project_id = sample_project["id"]
        response = client.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == project_id
        assert "actividades" in data
        assert "evm_consolidado" in data

    def test_detalle_con_actividades_incluye_evm(self, client, sample_activity):
        project_id = sample_activity["project_id"]
        response = client.get(f"/api/v1/projects/{project_id}")
        data = response.json()
        assert len(data["actividades"]) == 1
        act = data["actividades"][0]
        assert "evm" in act
        assert act["evm"]["pv"] == 6000.0
        assert act["evm"]["ev"] == 4000.0

    def test_detalle_proyecto_inexistente_404(self, client):
        response = client.get(f"/api/v1/projects/{FAKE_UUID}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Proyecto no encontrado"


class TestUpdateProject:
    def test_editar_nombre(self, client, sample_project):
        project_id = sample_project["id"]
        response = client.put(
            f"/api/v1/projects/{project_id}",
            json={"name": "Nombre Nuevo"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Nombre Nuevo"

    def test_editar_descripcion(self, client, sample_project):
        project_id = sample_project["id"]
        response = client.put(
            f"/api/v1/projects/{project_id}",
            json={"description": "Nueva descripción"},
        )
        assert response.status_code == 200
        assert response.json()["description"] == "Nueva descripción"

    def test_editar_proyecto_inexistente_404(self, client):
        response = client.put(
            f"/api/v1/projects/{FAKE_UUID}",
            json={"name": "No existe"},
        )
        assert response.status_code == 404


class TestDeleteProject:
    def test_eliminar_proyecto_exitoso(self, client, sample_project):
        project_id = sample_project["id"]
        response = client.delete(f"/api/v1/projects/{project_id}")
        assert response.status_code == 204

        # Verificar que ya no existe
        response = client.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == 404

    def test_eliminar_proyecto_inexistente_404(self, client):
        response = client.delete(f"/api/v1/projects/{FAKE_UUID}")
        assert response.status_code == 404


# ═════════════════════════════════════════════════════════════════════════════
# 8.5 — Cascade delete
# ═════════════════════════════════════════════════════════════════════════════


class TestCascadeDelete:
    def test_eliminar_proyecto_elimina_actividades(self, client, sample_activity):
        project_id = sample_activity["project_id"]

        # Verificar que la actividad existe
        response = client.get(f"/api/v1/projects/{project_id}/activities")
        assert len(response.json()) == 1

        # Eliminar proyecto
        response = client.delete(f"/api/v1/projects/{project_id}")
        assert response.status_code == 204

        # Verificar que proyecto y actividades desaparecieron
        response = client.get(f"/api/v1/projects/{project_id}")
        assert response.status_code == 404
