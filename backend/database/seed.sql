-- =============================================================================
-- EVM Tracker v1 — Seed Data
-- Ejecutar DESPUÉS de schema.sql
-- =============================================================================

-- Limpieza previa (idempotente)
DELETE FROM activities;
DELETE FROM projects;

-- =============================================================================
-- Proyecto 1: "Rediseño Portal Web"
-- Narrativa: Proyecto en problemas — retrasado y sobre presupuesto
-- =============================================================================
INSERT INTO projects (id, name, description) VALUES
    ('a1b2c3d4-e5f6-7890-abcd-111111111111',
     'Rediseño Portal Web',
     'Actualización completa del portal corporativo con nuevo diseño y funcionalidades');

INSERT INTO activities (id, project_id, name, bac, planned_percentage, actual_percentage, actual_cost) VALUES
    ('aaaa1111-1111-1111-1111-aaaaaaaaaaaa',
     'a1b2c3d4-e5f6-7890-abcd-111111111111',
     'Diseño UI/UX', 15000.00, 100.00, 100.00, 18000.00),

    ('aaaa2222-2222-2222-2222-aaaaaaaaaaaa',
     'a1b2c3d4-e5f6-7890-abcd-111111111111',
     'Desarrollo Frontend', 25000.00, 60.00, 40.00, 18000.00),

    ('aaaa3333-3333-3333-3333-aaaaaaaaaaaa',
     'a1b2c3d4-e5f6-7890-abcd-111111111111',
     'Desarrollo Backend', 20000.00, 50.00, 35.00, 12000.00),

    ('aaaa4444-4444-4444-4444-aaaaaaaaaaaa',
     'a1b2c3d4-e5f6-7890-abcd-111111111111',
     'Testing QA', 10000.00, 30.00, 10.00, 5000.00);

-- =============================================================================
-- Proyecto 2: "App Móvil Inventarios"
-- Narrativa: Proyecto saludable — adelantado y dentro de presupuesto
-- =============================================================================
INSERT INTO projects (id, name, description) VALUES
    ('b2c3d4e5-f6a7-8901-bcde-222222222222',
     'App Móvil Inventarios',
     'Aplicación móvil para gestión de inventarios en tiempo real');

INSERT INTO activities (id, project_id, name, bac, planned_percentage, actual_percentage, actual_cost) VALUES
    ('bbbb1111-1111-1111-1111-bbbbbbbbbbbb',
     'b2c3d4e5-f6a7-8901-bcde-222222222222',
     'Arquitectura y diseño', 8000.00, 100.00, 100.00, 7500.00),

    ('bbbb2222-2222-2222-2222-bbbbbbbbbbbb',
     'b2c3d4e5-f6a7-8901-bcde-222222222222',
     'Módulo de inventario', 18000.00, 70.00, 80.00, 11000.00),

    ('bbbb3333-3333-3333-3333-bbbbbbbbbbbb',
     'b2c3d4e5-f6a7-8901-bcde-222222222222',
     'Módulo de reportes', 12000.00, 40.00, 50.00, 4500.00),

    ('bbbb4444-4444-4444-4444-bbbbbbbbbbbb',
     'b2c3d4e5-f6a7-8901-bcde-222222222222',
     'Integración API externa', 6000.00, 20.00, 15.00, 0.00);

-- =============================================================================
-- Proyecto 3: "Migración Base de Datos"
-- Narrativa: Proyecto perfecto — CPI=1, SPI=1 + edge case sin datos
-- =============================================================================
INSERT INTO projects (id, name, description) VALUES
    ('c3d4e5f6-a7b8-9012-cdef-333333333333',
     'Migración Base de Datos',
     'Migración de base de datos legacy a PostgreSQL con validación de integridad');

INSERT INTO activities (id, project_id, name, bac, planned_percentage, actual_percentage, actual_cost) VALUES
    ('cccc1111-1111-1111-1111-cccccccccccc',
     'c3d4e5f6-a7b8-9012-cdef-333333333333',
     'Análisis de esquema', 5000.00, 50.00, 50.00, 2500.00),

    ('cccc2222-2222-2222-2222-cccccccccccc',
     'c3d4e5f6-a7b8-9012-cdef-333333333333',
     'Ejecución de migración', 10000.00, 30.00, 30.00, 3000.00),

    ('cccc3333-3333-3333-3333-cccccccccccc',
     'c3d4e5f6-a7b8-9012-cdef-333333333333',
     'Validación post-migración', 5000.00, 0.00, 0.00, 0.00);
