import { RepeaterField } from "./RepeaterField"
import { AnamnesisField } from "./types"

function normalizeOptions(options?: Array<{ label: string; value: string }> | string[]) {
  if (!options) return []
  return options.map((option) => typeof option === "string" ? { label: option, value: option } : option)
}

export function FieldRenderer({ field, value, onChange }: { field: AnamnesisField; value: any; onChange: (value: any) => void }) {
  const commonClass = "w-full rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700"
  const options = normalizeOptions(field.options)

  if (field.type === "repeater") {
    return <RepeaterField field={field} value={Array.isArray(value) ? value : []} onChange={onChange} />
  }

  switch (field.type) {
    case "textarea":
      return <textarea value={value ?? ""} onChange={(e) => onChange(e.target.value)} className={`${commonClass} min-h-[110px]`} placeholder={field.placeholder} />
    case "number":
      return <input type="number" value={value ?? ""} onChange={(e) => onChange(e.target.value)} className={commonClass} placeholder={field.placeholder} />
    case "date":
      return <input type="date" value={value ?? ""} onChange={(e) => onChange(e.target.value)} className={commonClass} />
    case "select":
      return (
        <select value={value ?? ""} onChange={(e) => onChange(e.target.value)} className={commonClass}>
          <option value="">Selecione...</option>
          {options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
        </select>
      )
    case "radio":
    case "yes_no": {
      const radioOptions = field.type === "yes_no" ? [{ label: "Sim", value: "true" }, { label: "Não", value: "false" }] : options
      return (
        <div className="flex flex-col gap-2">
          {radioOptions.map((option) => (
            <label key={option.value} className="flex items-center gap-2 text-sm text-slate-700">
              <input type="radio" checked={String(value) === option.value} onChange={() => onChange(field.type === "yes_no" ? option.value === "true" : option.value)} />
              {option.label}
            </label>
          ))}
        </div>
      )
    }
    case "checkbox":
      return <label className="flex items-center gap-2 text-sm text-slate-700"><input type="checkbox" checked={Boolean(value)} onChange={(e) => onChange(e.target.checked)} /> Marcar</label>
    case "multiselect":
      return (
        <div className="flex flex-col gap-2">
          {options.map((option) => {
            const selected = Array.isArray(value) ? value.includes(option.value) : false
            return (
              <label key={option.value} className="flex items-center gap-2 text-sm text-slate-700">
                <input
                  type="checkbox"
                  checked={selected}
                  onChange={(e) => {
                    const current = Array.isArray(value) ? value : []
                    onChange(e.target.checked ? [...current, option.value] : current.filter((item: string) => item !== option.value))
                  }}
                />
                {option.label}
              </label>
            )
          })}
        </div>
      )
    case "email":
      return <input type="email" value={value ?? ""} onChange={(e) => onChange(e.target.value)} className={commonClass} placeholder={field.placeholder} />
    case "phone":
      return <input type="tel" value={value ?? ""} onChange={(e) => onChange(e.target.value)} className={commonClass} placeholder={field.placeholder || "(00) 00000-0000"} />
    default:
      return <input type="text" value={value ?? ""} onChange={(e) => onChange(e.target.value)} className={commonClass} placeholder={field.placeholder} />
  }
}
