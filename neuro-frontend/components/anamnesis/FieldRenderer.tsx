import { RepeaterField } from "./RepeaterField"
import { AnamnesisField } from "./types"

function normalizeOptions(options?: Array<{ label: string; value: string }> | string[]) {
  if (!options) return []
  return options.map((option) => typeof option === "string" ? { label: option, value: option } : option)
}

function DateField({ value, onChange, className }: { value: string | undefined; onChange: (value: string) => void; className: string }) {
  const [year = "", month = "", day = ""] = (value || "").split("-")
  const currentYear = new Date().getFullYear()
  const years = Array.from({ length: currentYear - 1899 }, (_, index) => String(currentYear - index))
  const months = Array.from({ length: 12 }, (_, index) => String(index + 1).padStart(2, "0"))
  const maxDays = year && month ? new Date(Number(year), Number(month), 0).getDate() : 31
  const days = Array.from({ length: maxDays }, (_, index) => String(index + 1).padStart(2, "0"))

  function updateDate(next: { year?: string; month?: string; day?: string }) {
    const nextYear = next.year ?? year
    const nextMonth = next.month ?? month
    const nextDay = next.day ?? day

    if (!nextYear || !nextMonth || !nextDay) {
      onChange("")
      return
    }

    const safeDay = Math.min(Number(nextDay), new Date(Number(nextYear), Number(nextMonth), 0).getDate())
    onChange(`${nextYear}-${nextMonth}-${String(safeDay).padStart(2, "0")}`)
  }

  return (
    <div className="grid grid-cols-3 gap-3">
      <select value={day} onChange={(e) => updateDate({ day: e.target.value })} className={className}>
        <option value="">Dia</option>
        {days.map((option) => <option key={option} value={option}>{option}</option>)}
      </select>
      <select value={month} onChange={(e) => updateDate({ month: e.target.value })} className={className}>
        <option value="">Mês</option>
        {months.map((option) => <option key={option} value={option}>{option}</option>)}
      </select>
      <select value={year} onChange={(e) => updateDate({ year: e.target.value })} className={className}>
        <option value="">Ano</option>
        {years.map((option) => <option key={option} value={option}>{option}</option>)}
      </select>
    </div>
  )
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
      return <DateField value={typeof value === "string" ? value : ""} onChange={onChange} className={commonClass} />
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
