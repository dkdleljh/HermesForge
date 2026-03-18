import { useMutation, useQuery } from '@tanstack/react-query'
import { useState } from 'react'
import Badge from '../components/Badge'
import { api } from '../services/api'
import { RenderedEvent, Snapshot } from '../types/models'

export default function MaterializePage() {
  const [snapshotId, setSnapshotId] = useState('')
  const [profile, setProfile] = useState('education')
  const [mode, setMode] = useState('deterministic')
  const [result, setResult] = useState<RenderedEvent | null>(null)

  const { data: snapshots = [] } = useQuery<Snapshot[]>({ queryKey: ['snapshots'], queryFn: api.listSnapshots })

  const mutation = useMutation({
    mutationFn: api.materialize,
    onSuccess: (data) => setResult(data as RenderedEvent),
  })

  return (
    <div className="space-y-4">
      <div className="panel grid gap-2 md:grid-cols-4">
        <select className="rounded border p-2" value={snapshotId} onChange={(e) => setSnapshotId(e.target.value)}>
          <option value="">snapshot 선택</option>
          {snapshots.map((s) => <option key={s.snapshot_id} value={s.snapshot_id}>{s.snapshot_id}</option>)}
        </select>
        <select className="rounded border p-2" value={profile} onChange={(e) => setProfile(e.target.value)}>
          <option value="education">education</option>
          <option value="game">game</option>
          <option value="training">training</option>
        </select>
        <select className="rounded border p-2" value={mode} onChange={(e) => setMode(e.target.value)}>
          <option value="deterministic">deterministic</option>
          <option value="weighted">weighted</option>
        </select>
        <button
          className="rounded bg-brand-600 px-3 py-2 text-white"
          onClick={() =>
            mutation.mutate({
              snapshot_id: snapshotId,
              mode,
              context: {
                user_role: profile === 'training' ? 'trainer' : profile === 'game' ? 'player' : 'teacher',
                environment: profile === 'training' ? 'high_risk' : profile === 'game' ? 'field' : 'classroom',
                permissions: ['render'],
                state_flags: { signal: profile },
                scenario_profile: profile,
                intent: profile === 'training' ? 'evacuate' : profile === 'game' ? 'explore' : 'review',
              },
            })
          }
        >
          렌더 실행
        </button>
      </div>

      {result && (
        <div className="panel">
          <div className="mb-2 flex gap-2">
            <Badge text={result.label} tone="green" />
            <Badge text={String(result.provenance.watermark ?? 'NOT_FACT')} tone="red" />
          </div>
          <h3 className="font-semibold">{String(result.rendered_event.action ?? '')}</h3>
          <p className="text-sm">{String(result.rendered_event.message ?? '')}</p>
          <p className="mt-2 text-xs text-slate-500">본 결과는 사실 기록이 아닌 가능역 렌더입니다.</p>
        </div>
      )}
    </div>
  )
}
