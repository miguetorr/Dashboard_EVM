-- =============================================================================
-- EVM Tracker v1 — DDL
-- PostgreSQL 14+
-- =============================================================================

-- Forzar encoding UTF-8 para caracteres especiales
SET client_encoding TO 'UTF8';

-- Extensión para generación de UUIDs
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- -----------------------------------------------------------------------------
-- Tabla: projects
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS projects (
    id            UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    name          VARCHAR(255) NOT NULL,
    description   TEXT,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- -----------------------------------------------------------------------------
-- Tabla: activities
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS activities (
    id                  UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id          UUID            NOT NULL
                        REFERENCES projects(id) ON DELETE CASCADE,
    name                VARCHAR(255)    NOT NULL,
    bac                 NUMERIC(14,2)   NOT NULL,
    planned_percentage  NUMERIC(5,2)    NOT NULL DEFAULT 0,
    actual_percentage   NUMERIC(5,2)    NOT NULL DEFAULT 0,
    actual_cost         NUMERIC(14,2)   NOT NULL DEFAULT 0,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    -- CHECK constraints (integridad de dominio)
    CONSTRAINT chk_bac_positive
        CHECK (bac > 0),
    CONSTRAINT chk_actual_cost_non_negative
        CHECK (actual_cost >= 0),
    CONSTRAINT chk_planned_percentage_range
        CHECK (planned_percentage >= 0 AND planned_percentage <= 100),
    CONSTRAINT chk_actual_percentage_range
        CHECK (actual_percentage >= 0 AND actual_percentage <= 100)
);

-- -----------------------------------------------------------------------------
-- Índices
-- -----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_activities_project_id
    ON activities(project_id);
