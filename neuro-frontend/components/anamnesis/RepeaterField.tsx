import { AnamnesisField } from "./types"

function emptyItem(fields: AnamnesisField[]) {
  const result: Record<string, any> = {}
  fields.forEach((field) => {
    result[field.id] = field.type === "checkbox" ? false : field.type === "multiselect" ? [] : ""
  })
  return result
}

export function RepeaterField({ field, value, onChange }: { field: AnamnesisField; value: any[]; onChange: (value: any[]) => void }) {
  const fields = field.item_fields || []
  const items = Array.isArray(value) ? value : []

  return (
    <div className="space-y-3">
      {items.map((item, index) => (
        <div key={index} className="rounded-xl border border-slate-200 bg-slate-50 p-4">
          <div className="mb-3 flex items-center justify-between gap-3">
            <div className="text-sm font-medium text-slate-700">Registro {index + 1}</div>
            <button type="button" onClick={() => onChange(items.filter((_, itemIndex) => itemIndex !== index))} className="text-sm text-rose-700">Remover</button>
          </div>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {fields.map((itemField) => (
              <div key={itemField.id} className="space-y-2">
                <label className="text-sm font-medium text-slate-700">{itemField.label}{itemField.required ? " *" : ""}</label>
                <input
                  value={item?.[itemField.id] ?? ""}
                  onChange={(e) => {
                    const next = [...items]
                    next[index] = { ...next[index], [itemField.id]: e.target.value }
                    onChange(next)
                  }}
                  className="w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm"
                />
              </div>
            ))}
          </div>
        </div>
      ))}

      <button type="button" onClick={() => onChange([...items, emptyItem(fields)])} className="rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm text-slate-700">
        Adicionar item
      </button>
    </div>
  )
}
