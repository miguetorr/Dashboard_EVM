## 1. Configuración del proyecto

- [x] 1.1 Crear estructura de directorios del backend (app/, routers/, schemas/, models/, services/, repositories/, core/, tests/)
- [x] 1.2 Crear requirements.txt con dependencias: fastapi, uvicorn, sqlalchemy, psycopg2-binary, pydantic, pydantic-settings, pytest, httpx, pytest-cov
- [x] 1.3 Configurar flake8 (.flake8) y pyproject.toml con black
- [x] 1.4 Crear estructura de directorios del frontend con Vite + React + TypeScript
- [x] 1.5 Configurar ESLint y Prettier en el frontend (.eslintrc.cjs, .prettierrc)
- [x] 1.6 Instalar dependencias frontend: axios, recharts, react-router-dom

## 2. Base de datos

- [x] 2.1 Crear script DDL (SQL) con tabla projects, tabla activities, CHECK constraints, cascade delete, y extensión uuid-ossp/pgcrypto
- [x] 2.2 Crear script seed (SQL) con al menos 2 proyectos y 3+ actividades cada uno, cubriendo escenarios variados (buen estado, mal estado, AC=0)
- [x] 2.3 Crear modelos SQLAlchemy (Project, Activity) con relaciones y constraints mapeados
- [x] 2.4 Crear database.py con engine, SessionLocal y get_db dependency

## 3. Core — Motor EVM

- [x] 3.1 Crear evm_constants.py con estados (bajo_presupuesto, sobre_presupuesto, etc.) y razones en español
- [x] 3.2 Crear evm_calculator.py con función calculate_activity_evm(bac, planned_pct, actual_pct, actual_cost) → EVMResult
- [x] 3.3 Crear función calculate_project_evm(activities) → EVMConsolidated (suma de componentes)
- [x] 3.4 Implementar manejo de edge cases: AC=0, PV=0, CPI=0 → null + razón
- [x] 3.5 Implementar redondeo: índices a 4 decimales, monetarios a 2 decimales
- [x] 3.6 Escribir tests unitarios para calculate_activity_evm: caso estándar, actividad completa, CPI/SPI=1
- [x] 3.7 Escribir tests unitarios para edge cases: AC=0, PV=0, actual_pct=0, todo en cero
- [x] 3.8 Escribir tests unitarios para calculate_project_evm: consolidado múltiples actividades, sin actividades, todas AC=0
- [x] 3.9 Escribir tests unitarios para interpretación de estados CPI/SPI en español
- [x] 3.10 Escribir tests unitarios para precisión de redondeo

## 4. Schemas Pydantic (contratos de API)

- [x] 4.1 Crear schemas de proyecto: ProjectCreate, ProjectUpdate, ProjectResponse, ProjectListResponse (con resumen EVM)
- [x] 4.2 Crear schemas de actividad: ActivityCreate, ActivityUpdate, ActivityResponse (con validaciones: bac>0, ac>=0, porcentajes 0-100)
- [x] 4.3 Crear schemas EVM: EVMResult (por actividad), EVMConsolidated (por proyecto) con campos estado_cpi, estado_spi, razon_cpi, razon_spi
- [x] 4.4 Crear ProjectDetailResponse con lista de actividades + evm_consolidado

## 5. Repositorios

- [x] 5.1 Crear base.py con AbstractRepository
- [x] 5.2 Crear ProjectRepository: get_all, get_by_id, create, update, delete
- [x] 5.3 Crear ActivityRepository: get_by_project_id, get_by_id, create, update, delete

## 6. Servicios

- [x] 6.1 Crear exceptions.py con excepciones de dominio (ProjectNotFound, ActivityNotFound)
- [x] 6.2 Crear ProjectService: list_projects (con resumen EVM), get_project_detail (con actividades + EVM consolidado), create, update, delete
- [x] 6.3 Crear ActivityService: list_by_project, create (valida que proyecto exista), update, delete
- [x] 6.4 Integrar EVM calculator en services (calcular indicadores al retornar actividades/proyectos)
- [x] 6.5 Implementar AnonymousPrincipal como preparación para auth V2

## 7. Routers (capa HTTP)

- [ ] 7.1 Crear router de proyectos: GET /api/v1/projects, POST, GET /{id}, PUT /{id}, DELETE /{id}
- [ ] 7.2 Crear router de actividades: GET /api/v1/projects/{id}/activities, POST, PUT /{act_id}, DELETE /{act_id}
- [ ] 7.3 Crear main.py con app factory, CORS middleware, inclusión de routers, y docs en /docs
- [ ] 7.4 Configurar config.py con pydantic-settings para DATABASE_URL y CORS origins

## 8. Tests de integración (API)

- [ ] 8.1 Crear conftest.py con fixtures: test database, test client, proyecto y actividad de ejemplo
- [ ] 8.2 Tests de integración para endpoints de proyectos: crear, listar, detalle, editar, eliminar, 404s
- [ ] 8.3 Tests de integración para endpoints de actividades: crear, listar, editar, eliminar, 404s
- [ ] 8.4 Tests de integración para validaciones: bac<=0, ac<0, porcentaje>100, porcentaje<0, nombre vacío
- [ ] 8.5 Tests de integración para cascade delete: eliminar proyecto verifica que actividades se eliminan
- [ ] 8.6 Tests de integración para edge cases EVM en respuestas: verificar null + razones en JSON de respuesta
- [ ] 8.7 Verificar cobertura ≥ 80% en lógica de negocio con pytest-cov

## 9. Frontend — Tipos y utilidades

- [ ] 9.1 Crear tipos TypeScript: Project, Activity, EVMResult, EVMConsolidated, EVMStatus
- [ ] 9.2 Crear evmCalculator.ts con misma lógica que backend (para cálculo reactivo local)
- [ ] 9.3 Crear cliente API (axios instance con baseURL, interceptors de error, funciones tipadas por endpoint)

## 10. Frontend — Componentes compartidos

- [ ] 10.1 Crear componente StatusBadge (badge de color según estado EVM)
- [ ] 10.2 Crear componente ConfirmDialog (diálogo de confirmación reutilizable con botón rojo)
- [ ] 10.3 Crear componente EVMGlossary (panel colapsable con definiciones en español)

## 11. Frontend — Página de lista de proyectos

- [ ] 11.1 Crear componente ProjectCard (nombre, descripción, conteo actividades, CPI/SPI con badges)
- [ ] 11.2 Crear page ProjectListPage con grid de cards, botón "Nuevo", estado vacío
- [ ] 11.3 Crear modal para crear/editar proyecto (campos: nombre, descripción)
- [ ] 11.4 Integrar eliminación de proyecto con ConfirmDialog (muestra nombre + conteo de actividades)

## 12. Frontend — Dashboard de proyecto

- [ ] 12.1 Crear componente EVMIndicators (BAC, PV, EV, AC, CV, SV, CPI, SPI, EAC, VAC con badges y tooltips con fórmulas)
- [ ] 12.2 Crear componente ActivityTable con columnas de datos + EVM, botones ✏️ y 🗑️, y lógica "Ver más/Ver menos" (5 iniciales)
- [ ] 12.3 Crear componente ActivityModal con campos de actividad + vista previa EVM reactiva (recalcula al editar sin API)
- [ ] 12.4 Crear componente EVMChart (barras agrupadas PV/EV/AC por actividad con Recharts)
- [ ] 12.5 Crear componente ProjectSelector (dropdown breadcrumb para cambio rápido de proyecto)
- [ ] 12.6 Crear page ProjectDashboardPage integrando todos los componentes del dashboard
- [ ] 12.7 Integrar eliminación de actividad con ConfirmDialog (muestra nombre de la actividad)

## 13. Frontend — Routing y App

- [ ] 13.1 Configurar React Router con rutas: /projects (lista), /projects/:id (dashboard)
- [ ] 13.2 Configurar App.tsx con layout base y router
- [ ] 13.3 Manejar estados de carga y error en las páginas

## 14. Entregables finales

- [ ] 14.1 Crear README.md con instrucciones completas: levantar PostgreSQL, ejecutar DDL, ejecutar seed, levantar backend, levantar frontend
- [ ] 14.2 Verificar OpenAPI docs accesible en /docs con descripciones, schemas y códigos de error
- [ ] 14.3 Confirmar que los schemas de FastAPI son consistentes con openapi.yaml (nombres de campos, tipos, nullables)
- [ ] 14.4 Verificar que linters pasan sin errores (flake8 backend, eslint frontend)
- [ ] 14.5 Verificar cobertura de tests ≥ 80% en lógica de negocio
