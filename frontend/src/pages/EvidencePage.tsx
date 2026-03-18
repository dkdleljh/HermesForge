import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { FormEvent, useState } from 'react'
import { api } from '../services/api'
import { Evidence } from '../types/models'

export default function EvidencePage() {
  const queryClient = useQueryClient()
  const [source, setSource] = useState('manual.input')
  const [category, setCategory] = useState('education')
  const [message, setMessage] = useState('수동 입력 evidence')

  const { data = [] } = useQuery<Evidence[]>({ queryKey: ['evidence'], queryFn: api.listEvidence })
  const mutation = useMutation({
    mutationFn: api.createEvidence,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['evidence'] }),
  })

  const onSubmit = (e: FormEvent) => {
    e.preventDefault()
    mutation.mutate({
      source,
      payload: { category, suggested_outcome: 'review_session', message },
      trust_score: 0.7,
      timestamp: new Date().toISOString(),
    })
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <form className="panel space-y-2" onSubmit={onSubmit}>
        <h3 className="font-semibold">Evidence 추가</h3>
        <input className="w-full rounded border p-2" value={source} onChange={(e) => setSource(e.target.value)} />
        <input className="w-full rounded border p-2" value={category} onChange={(e) => setCategory(e.target.value)} />
        <input className="w-full rounded border p-2" value={message} onChange={(e) => setMessage(e.target.value)} />
        <button className="rounded bg-brand-600 px-3 py-2 text-white">추가</button>
      </form>
      <div className="panel">
        <h3 className="mb-2 font-semibold">Evidence 목록</h3>
        <div className="max-h-[420px] space-y-2 overflow-auto">
          {data.map((e) => (
            <div key={e.id} className="rounded border p-2 text-sm">
              <p className="font-medium">{e.source}</p>
              <p>{String(e.payload.message ?? '')}</p>
              <p className="text-xs text-slate-500">{e.id}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
