export type Evidence = {
  id: string
  source: string
  payload: Record<string, unknown>
  trust_score: number
  timestamp: string
  hash: string
}

export type LambdaPatch = {
  id: string
  conditions: Record<string, unknown>
  outcome: Record<string, unknown>
  probability_mass: number
  confidence: number
  constraint_proof: string
  witness_refs: string[]
  anchor_weight: number
  labels: string[]
}

export type Snapshot = {
  snapshot_id: string
  parent_snapshot_id: string | null
  patches: string[]
  policy_root: string
  witness_root: string
  entropy_budget: number
  created_at: string
  version: string
}

export type RenderedEvent = {
  render_id: string
  snapshot_id: string
  context_hash: string
  rendered_event: Record<string, unknown>
  confidence: number
  policy_hash: string
  provenance: Record<string, unknown>
  label: string
  timestamp: string
}

export type PolicyInfo = {
  policy_name: string
  version: string
  rules: { code: string; description: string }[]
}
