import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { FormEvent, useState } from 'react'
import { api } from '../services/api'
import { LambdaPatch } from '../types/models'

export default function PatchPage() {
  const queryClient = useQueryClient()
  const [category, setCategory] = useState('education')
  const [action, setAction] = useState('review_session')

  const { data = [] } = useQuery<LambdaPatch[]>({ queryKey: ['patches'], queryFn: api.listPatches })
  const mutation = useMutation({
    mutationFn: api.createPatch,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['patches'] }),
  })

  const onSubmit = (e: FormEvent) => {
    e.preventDefault()
    mutation.mutate({
      conditions: { category },
      outcome: { category, action, message: `${action} 제안` },
      probability_mass: 0.7,
      confidence: 0.8,
      constraint_proof: 'manual',
      witness_refs: [],
      anchor_weight: 1,
      labels: [category],
    })
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <form className="panel space-y-2" onSubmit={onSubmit}>
        <h3 className="font-semibold">Lambda Patch 생성</h3>
        <input className="w-full rounded border p-2" value={category} onChange={(e) => setCategory(e.target.value)} />
        <input className="w-full rounded border p-2" value={action} onChange={(e) => setAction(e.target.value)} />
        <button className="rounded bg-brand-600 px-3 py-2 text-white">생성</button>
      </form>
      <div className="panel">
        <h3 className="mb-2 font-semibold">Patch 목록</h3>
        <div className="max-h-[420px] space-y-2 overflow-auto">
          {data.map((p) => (
            <div key={p.id} className="rounded border p-2 text-sm">
              <p className="font-medium">{String(p.outcome.action ?? '')}</p>
              <p>{String(p.outcome.message ?? '')}</p>
              <p className="text-xs text-slate-500">{p.id}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
