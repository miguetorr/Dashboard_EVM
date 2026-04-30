// Estados de interpretación del CPI
export const CPI_STATUS = {
  BAJO_PRESUPUESTO: "bajo_presupuesto",
  EN_PRESUPUESTO: "en_presupuesto",
  SOBRE_PRESUPUESTO: "sobre_presupuesto",
} as const;

// Estados de interpretación del SPI
export const SPI_STATUS = {
  ADELANTADO: "adelantado",
  EN_CRONOGRAMA: "en_cronograma",
  ATRASADO: "atrasado",
} as const;

// Estado compartido cuando el indicador no es calculable
export const DATOS_INSUFICIENTES = "datos_insuficientes" as const;

// Razones por las que un indicador puede ser nulo
export const EVM_REASONS = {
  COSTO_REAL_ES_CERO: "costo_real_es_cero",
  VALOR_PLANIFICADO_ES_CERO: "valor_planificado_es_cero",
  SIN_ACTIVIDADES: "sin_actividades",
} as const;

export type EVMCpiStatus =
  | (typeof CPI_STATUS)[keyof typeof CPI_STATUS]
  | typeof DATOS_INSUFICIENTES;

export type EVMSpiStatus =
  | (typeof SPI_STATUS)[keyof typeof SPI_STATUS]
  | typeof DATOS_INSUFICIENTES;

export type EVMReason =
  | (typeof EVM_REASONS)[keyof typeof EVM_REASONS]
  | null;

export interface EVMResult {
  pv: number;
  ev: number;
  cv: number;
  sv: number;
  cpi: number | null;
  spi: number | null;
  eac: number | null;
  vac: number | null;
  estado_cpi: EVMCpiStatus;
  estado_spi: EVMSpiStatus;
  razon_cpi: string | null;
  razon_spi: string | null;
}

export interface EVMConsolidated {
  bac_total: number;
  pv: number;
  ev: number;
  ac: number;
  cv: number;
  sv: number;
  cpi: number | null;
  spi: number | null;
  eac: number | null;
  vac: number | null;
  estado_cpi: EVMCpiStatus;
  estado_spi: EVMSpiStatus;
  razon_cpi: string | null;
  razon_spi: string | null;
}

export interface Activity {
  id: string;
  project_id: string;
  name: string;
  bac: number;
  planned_percentage: number;
  actual_percentage: number;
  actual_cost: number;
  created_at: string;
  updated_at: string;
  evm: EVMResult;
}

export interface ActivityCreate {
  name: string;
  bac: number;
  planned_percentage: number;
  actual_percentage: number;
  actual_cost: number;
}

export interface ActivityUpdate {
  name?: string;
  bac?: number;
  planned_percentage?: number;
  actual_percentage?: number;
  actual_cost?: number;
}

export interface Project {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string | null;
}

export interface ProjectUpdate {
  name?: string;
  description?: string | null;
}

export interface ProjectListItem {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  total_actividades: number;
  evm_consolidado: EVMConsolidated;
}

export interface ProjectDetail {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  actividades: Activity[];
  evm_consolidado: EVMConsolidated;
}
