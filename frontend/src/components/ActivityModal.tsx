import { useState, useEffect } from "react";
import type { Activity } from "../types/evm";
import { calculateActivityEvm } from "../utils/evmCalculator";
import StatusBadge from "./StatusBadge";

interface ActivityModalProps {
  open: boolean;
  activity: Activity | null;
  onSave: (data: {
    name: string;
    bac: number;
    planned_percentage: number;
    actual_percentage: number;
    actual_cost: number;
  }) => void;
  onCancel: () => void;
}

export default function ActivityModal({
  open,
  activity,
  onSave,
  onCancel,
}: ActivityModalProps) {
  const [name, setName] = useState("");
  const [bac, setBac] = useState("0");
  const [plannedPct, setPlannedPct] = useState("0");
  const [actualPct, setActualPct] = useState("0");
  const [actualCost, setActualCost] = useState("0");

  useEffect(() => {
    if (open) {
      setName(activity?.name ?? "");
      setBac(activity?.bac?.toString() ?? "");
      setPlannedPct(activity?.planned_percentage?.toString() ?? "0");
      setActualPct(activity?.actual_percentage?.toString() ?? "0");
      setActualCost(activity?.actual_cost?.toString() ?? "0");
    }
  }, [open, activity]);

  if (!open) return null;

  const isEdit = activity !== null;

  const bacNum = parseFloat(bac) || 0;
  const plannedNum = parseFloat(plannedPct) || 0;
  const actualNum = parseFloat(actualPct) || 0;
  const costNum = parseFloat(actualCost) || 0;

  // Vista previa reactiva
  const preview =
    bacNum > 0
      ? calculateActivityEvm(bacNum, plannedNum, actualNum, costNum)
      : null;

  const canSave =
    name.trim().length > 0 &&
    bacNum > 0 &&
    plannedNum >= 0 && plannedNum <= 100 &&
    actualNum >= 0 && actualNum <= 100 &&
    costNum >= 0;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!canSave) return;
    onSave({
      name: name.trim(),
      bac: bacNum,
      planned_percentage: plannedNum,
      actual_percentage: actualNum,
      actual_cost: costNum,
    });
  }

  return (
    <div className="dialog-overlay" onClick={onCancel}>
      <div
        className="dialog dialog--form dialog--wide"
        onClick={(e) => e.stopPropagation()}
      >
        <h3 className="dialog__title">
          {isEdit ? "Editar actividad" : "Nueva actividad"}
        </h3>

        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="act-name">Nombre *</label>
              <input
                id="act-name"
                type="text"
                className="form-control"
                value={name}
                onChange={(e) => setName(e.target.value)}
                maxLength={255}
                autoFocus
              />
            </div>

            <div className="form-group">
              <label htmlFor="act-bac">BAC (presupuesto) *</label>
              <input
                id="act-bac"
                type="number"
                className="form-control"
                value={bac}
                onChange={(e) => setBac(e.target.value)}
                min="0.01"
                step="0.01"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="act-planned">% Planificado</label>
              <input
                id="act-planned"
                type="number"
                className="form-control"
                value={plannedPct}
                onChange={(e) => setPlannedPct(e.target.value)}
                min="0"
                max="100"
                step="0.01"
              />
            </div>

            <div className="form-group">
              <label htmlFor="act-actual">% Real</label>
              <input
                id="act-actual"
                type="number"
                className="form-control"
                value={actualPct}
                onChange={(e) => setActualPct(e.target.value)}
                min="0"
                max="100"
                step="0.01"
              />
            </div>

            <div className="form-group">
              <label htmlFor="act-cost">Costo Real</label>
              <input
                id="act-cost"
                type="number"
                className="form-control"
                value={actualCost}
                onChange={(e) => setActualCost(e.target.value)}
                min="0"
                step="0.01"
              />
            </div>
          </div>

          {/* Vista previa EVM reactiva */}
          {preview && (
            <div className="evm-preview">
              <h4>Vista previa EVM</h4>
              <div className="evm-preview__grid">
                <div className="evm-preview__item">
                  <span>PV</span>
                  <span>${preview.pv.toFixed(2)}</span>
                </div>
                <div className="evm-preview__item">
                  <span>EV</span>
                  <span>${preview.ev.toFixed(2)}</span>
                </div>
                <div className="evm-preview__item">
                  <span>CV</span>
                  <span>${preview.cv.toFixed(2)}</span>
                </div>
                <div className="evm-preview__item">
                  <span>SV</span>
                  <span>${preview.sv.toFixed(2)}</span>
                </div>
                <div className="evm-preview__item">
                  <span>CPI</span>
                  <StatusBadge
                    status={preview.estado_cpi}
                    value={preview.cpi}
                    reason={preview.razon_cpi}
                  />
                </div>
                <div className="evm-preview__item">
                  <span>SPI</span>
                  <StatusBadge
                    status={preview.estado_spi}
                    value={preview.spi}
                    reason={preview.razon_spi}
                  />
                </div>
              </div>
            </div>
          )}

          <div className="dialog__actions">
            <button
              type="button"
              className="btn btn--secondary"
              onClick={onCancel}
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="btn btn--primary"
              disabled={!canSave}
            >
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
