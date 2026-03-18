import { Evidence, LambdaPatch, PolicyInfo, RenderedEvent, Snapshot } from '../types/models'

const API_BASE = 'http://localhost:8000/api'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || 'API 요청 실패')
  }
  return response.json() as Promise<T>
}

export const api = {
  health: () => request<{ status: string; service: string; timestamp: string }>('/health'),
  listEvidence: () => request<Evidence[]>('/evidence'),
  createEvidence: (body: unknown) => request<Evidence>('/evidence', { method: 'POST', body: JSON.stringify(body) }),
  listPatches: () => request<LambdaPatch[]>('/patches'),
  createPatch: (body: unknown) => request<LambdaPatch>('/patches', { method: 'POST', body: JSON.stringify(body) }),
  generateSnapshot: (body: unknown) => request<Snapshot>('/snapshots/generate', { method: 'POST', body: JSON.stringify(body) }),
  listSnapshots: () => request<Snapshot[]>('/snapshots'),
  getSnapshot: (id: string) => request<Snapshot>(`/snapshots/${id}`),
  mergeSnapshots: (body: unknown) => request<Snapshot>('/snapshots/merge', { method: 'POST', body: JSON.stringify(body) }),
  materialize: (body: unknown) => request<RenderedEvent>('/materialize', { method: 'POST', body: JSON.stringify(body) }),
  listRenders: () => request<RenderedEvent[]>('/renders'),
  policies: () => request<PolicyInfo>('/policies'),
  bootstrapDemo: () => request<{ message: string; evidence_count: number; patch_count: number; snapshot_count: number }>('/demo/bootstrap', { method: 'POST' }),
}
