"""Tests de integración para endpoints de actividades."""

import uuid


FAKE_UUID = str(uuid.uuid4())


# ═════════════════════════════════════════════════════════════════════════════
# 8.3 — CRUD de actividades
# ═════════════════════════════════════════════════════════════════════════════


class TestCreateActivity:
    def test_crear_actividad_exitosa(self, client, sample_project):
        project_id = sample_project["id"]
        response = client.post(
            f"/api/v1/projects/{project_id}/activities",
            json={
                "name": "Diseño UI",
                "bac": 15000,
                "planned_percentage": 100,
                "actual_percentage": 100,
                "actual_cost": 18000,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Diseño UI"
        assert data["bac"] == 15000.0
        assert data["project_id"] == project_id
        assert "evm" in data
        assert data["evm"]["pv"] == 15000.0
        assert data["evm"]["ev"] == 15000.0

    def test_crear_actividad_proyecto_inexistente_404(self, client):
        response = client.post(
            f"/api/v1/projects/{FAKE_UUID}/activities",
            json={
                "name": "Test",
                "bac": 1000,
                "planned_percentage": 50,
                "actual_percentage": 50,
                "actual_cost": 500,
            },
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Proyecto no encontrado"


class TestListActivities:
    def test_listar_actividades_de_proyecto(self, client, sample_activity):
        project_id = sample_activity["project_id"]
        response = client.get(f"/api/v1/projects/{project_id}/activities")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Actividad Test"
        assert "evm" in data[0]

    def test_listar_actividades_proyecto_sin_actividades(self, client, sample_project):
        project_id = sample_project["id"]
        response = client.get(f"/api/v1/projects/{project_id}/activities")
        assert response.status_code == 200
        assert response.json() == []

    def test_listar_actividades_proyecto_inexistente_404(self, client):
        response = client.get(f"/api/v1/projects/{FAKE_UUID}/activities")
        assert response.status_code == 404


class TestUpdateActivity:
    def test_editar_actividad_exitosa(self, client, sample_activity):
        project_id = sample_activity["project_id"]
        activity_id = sample_activity["id"]
        response = client.put(
            f"/api/v1/projects/{project_id}/activities/{activity_id}",
            json={"actual_percentage": 80},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["actual_percentage"] == 80.0
        # EVM recalculado
        assert data["evm"]["ev"] == 8000.0  # 10000 * 80/100

    def test_editar_nombre_actividad(self, client, sample_activity):
        project_id = sample_activity["project_id"]
        activity_id = sample_activity["id"]
        response = client.put(
            f"/api/v1/projects/{project_id}/activities/{activity_id}",
            json={"name": "Nombre Nuevo"},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Nombre Nuevo"

    def test_editar_actividad_inexistente_404(self, client, sample_project):
        project_id = sample_project["id"]
        response = client.put(
            f"/api/v1/projects/{project_id}/activities/{FAKE_UUID}",
            json={"name": "No existe"},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Actividad no encontrada"


class TestDeleteActivity:
    def test_eliminar_actividad_exitosa(self, client, sample_activity):
        project_id = sample_activity["project_id"]
        activity_id = sample_activity["id"]
        response = client.delete(
            f"/api/v1/projects/{project_id}/activities/{activity_id}"
        )
        assert response.status_code == 204

        # Verificar que ya no aparece
        response = client.get(f"/api/v1/projects/{project_id}/activities")
        assert len(response.json()) == 0

    def test_eliminar_actividad_inexistente_404(self, client, sample_project):
        project_id = sample_project["id"]
        response = client.delete(
            f"/api/v1/projects/{project_id}/activities/{FAKE_UUID}"
        )
        assert response.status_code == 404


# ═════════════════════════════════════════════════════════════════════════════
# 8.4 — Validaciones
# ═════════════════════════════════════════════════════════════════════════════


class TestActivityValidations:
    def test_bac_cero_422(self, client, sample_project):
        response = client.post(
            f"/api/v1/projects/{sample_project['id']}/activities",
            json={
                "name": "Test",
                "bac": 0,
                "planned_percentage": 50,
                "actual_percentage": 50,
                "actual_cost": 100,
            },
        )
        assert response.status_code == 422

    def test_bac_negativo_422(self, client, sample_project):
        response = client.post(
            f"/api/v1/projects/{sample_project['id']}/activities",
            json={
                "name": "Test",
                "bac": -100,
                "planned_percentage": 50,
                "actual_percentage": 50,
                "actual_cost": 100,
            },
        )
        assert response.status_code == 422

    def test_actual_cost_negativo_422(self, client, sample_project):
        response = client.post(
            f"/api/v1/projects/{sample_project['id']}/activities",
            json={
                "name": "Test",
                "bac": 1000,
                "planned_percentage": 50,
                "actual_percentage": 50,
                "actual_cost": -1,
            },
        )
        assert response.status_code == 422

    def test_porcentaje_mayor_100_422(self, client, sample_project):
        response = client.post(
            f"/api/v1/projects/{sample_project['id']}/activities",
            json={
                "name": "Test",
                "bac": 1000,
                "planned_percentage": 101,
                "actual_percentage": 50,
                "actual_cost": 100,
            },
        )
        assert response.status_code == 422

    def test_porcentaje_negativo_422(self, client, sample_project):
        response = client.post(
            f"/api/v1/projects/{sample_project['id']}/activities",
            json={
                "name": "Test",
                "bac": 1000,
                "planned_percentage": 50,
                "actual_percentage": -5,
                "actual_cost": 100,
            },
        )
        assert response.status_code == 422

    def test_nombre_vacio_422(self, client, sample_project):
        response = client.post(
            f"/api/v1/projects/{sample_project['id']}/activities",
            json={
                "name": "",
                "bac": 1000,
                "planned_percentage": 50,
                "actual_percentage": 50,
                "actual_cost": 100,
            },
        )
        assert response.status_code == 422

    def test_validacion_en_update_bac_negativo_422(self, client, sample_activity):
        project_id = sample_activity["project_id"]
        activity_id = sample_activity["id"]
        response = client.put(
            f"/api/v1/projects/{project_id}/activities/{activity_id}",
            json={"bac": -500},
        )
        assert response.status_code == 422


# ═════════════════════════════════════════════════════════════════════════════
# 8.6 — Edge cases EVM en respuestas JSON
# ═════════════════════════════════════════════════════════════════════════════


class TestEvmEdgeCasesInResponse:
    def test_actividad_ac_cero_cpi_null_con_razon(self, client, sample_project):
        """AC=0 → cpi=null, razon_cpi='costo_real_es_cero'."""
        project_id = sample_project["id"]
        response = client.post(
            f"/api/v1/projects/{project_id}/activities",
            json={
                "name": "Sin costo",
                "bac": 8000,
                "planned_percentage": 50,
                "actual_percentage": 30,
                "actual_cost": 0,
            },
        )
        assert response.status_code == 201
        evm = response.json()["evm"]
        assert evm["cpi"] is None
        assert evm["razon_cpi"] == "costo_real_es_cero"
        assert evm["eac"] is None
        assert evm["vac"] is None
        assert evm["estado_cpi"] == "datos_insuficientes"

    def test_actividad_pv_cero_spi_null_con_razon(self, client, sample_project):
        """planned_percentage=0 → spi=null, razon_spi='valor_planificado_es_cero'."""
        project_id = sample_project["id"]
        response = client.post(
            f"/api/v1/projects/{project_id}/activities",
            json={
                "name": "Sin plan",
                "bac": 5000,
                "planned_percentage": 0,
                "actual_percentage": 0,
                "actual_cost": 0,
            },
        )
        assert response.status_code == 201
        evm = response.json()["evm"]
        assert evm["spi"] is None
        assert evm["razon_spi"] == "valor_planificado_es_cero"
        assert evm["estado_spi"] == "datos_insuficientes"

    def test_consolidado_sin_actividades(self, client, sample_project):
        """Proyecto sin actividades → consolidado con razón 'sin_actividades'."""
        project_id = sample_project["id"]
        response = client.get(f"/api/v1/projects/{project_id}")
        evm = response.json()["evm_consolidado"]
        assert evm["bac_total"] == 0
        assert evm["cpi"] is None
        assert evm["spi"] is None
        assert evm["razon_cpi"] == "sin_actividades"
        assert evm["razon_spi"] == "sin_actividades"

    def test_consolidado_todas_ac_cero(self, client, sample_project):
        """Todas las actividades con AC=0 → cpi consolidado null."""
        project_id = sample_project["id"]
        for name in ["Act A", "Act B"]:
            client.post(
                f"/api/v1/projects/{project_id}/activities",
                json={
                    "name": name,
                    "bac": 5000,
                    "planned_percentage": 50,
                    "actual_percentage": 30,
                    "actual_cost": 0,
                },
            )
        response = client.get(f"/api/v1/projects/{project_id}")
        evm = response.json()["evm_consolidado"]
        assert evm["cpi"] is None
        assert evm["razon_cpi"] == "costo_real_es_cero"

    def test_evm_valores_standard_en_respuesta(self, client, sample_activity):
        """Verificar que el EVM se refleja correctamente en el JSON de respuesta."""
        evm = sample_activity["evm"]
        # bac=10000, planned=60, actual=40, ac=7000
        assert evm["pv"] == 6000.0
        assert evm["ev"] == 4000.0
        assert evm["cv"] == -3000.0
        assert evm["sv"] == -2000.0
        assert evm["cpi"] == 0.5714
        assert evm["spi"] == 0.6667
        assert evm["estado_cpi"] == "sobre_presupuesto"
        assert evm["estado_spi"] == "atrasado"
        assert evm["razon_cpi"] is None
        assert evm["razon_spi"] is None
