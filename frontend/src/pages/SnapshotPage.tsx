import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { api } from '../services/api'
import { Snapshot } from '../types/models'

export default function SnapshotPage() {
  const queryClient = useQueryClient()
  const [left, setLeft] = useState('')
  const [right, setRight] = useState('')

  const { data = [] } = useQuery<Snapshot[]>({ queryKey: ['snapshots'], queryFn: api.listSnapshots })

  const generate = useMutation({
    mutationFn: api.generateSnapshot,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['snapshots'] }),
  })
  const merge = useMutation({
    mutationFn: api.mergeSnapshots,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['snapshots'] }),
  })

  return (
    <div className="space-y-4">
      <div className="panel flex flex-wrap gap-2">
        <button className="rounded bg-brand-600 px-3 py-2 text-white" onClick={() => generate.mutate({})}>snapshot 생성</button>
        <input className="rounded border p-2" placeholder="left snapshot id" value={left} onChange={(e) => setLeft(e.target.value)} />
        <input className="rounded border p-2" placeholder="right snapshot id" value={right} onChange={(e) => setRight(e.target.value)} />
        <button className="rounded bg-slate-700 px-3 py-2 text-white" onClick={() => merge.mutate({ left_snapshot_id: left, right_snapshot_id: right })}>snapshot 병합</button>
      </div>
      <div className="panel">
        <h3 className="mb-2 font-semibold">Snapshot 목록</h3>
        <div className="space-y-2">
          {data.map((s) => (
            <div key={s.snapshot_id} className="rounded border p-2 text-sm">
              <p className="font-medium">{s.snapshot_id}</p>
              <p>patch 수: {s.patches.length}</p>
              <p className="text-xs text-slate-500">parent: {s.parent_snapshot_id ?? '-'}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
