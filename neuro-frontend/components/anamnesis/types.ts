export type ConditionalRule = {
  field: string
  equals: string | boolean | number
}

export type AnamnesisField = {
  id: string
  label: string
  type: string
  required?: boolean
  placeholder?: string
  help_text?: string
  options?: Array<{ label: string; value: string }> | string[]
  conditional?: ConditionalRule
  item_fields?: AnamnesisField[]
}

export type AnamnesisStep = {
  id: string
  title: string
  description?: string
  fields: AnamnesisField[]
}

export type AnamnesisSchema = {
  title?: string
  description?: string
  intro?: string
  steps?: AnamnesisStep[]
}
