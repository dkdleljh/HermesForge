import { useQuery } from '@tanstack/react-query'
import Badge from '../components/Badge'
import { api } from '../services/api'
import { Evidence, LambdaPatch, RenderedEvent, Snapshot } from '../types/models'

export default function DashboardPage() {
  const { data: evidence = [] } = useQuery<Evidence[]>({ queryKey: ['evidence'], queryFn: api.listEvidence })
  const { data: patches = [] } = useQuery<LambdaPatch[]>({ queryKey: ['patches'], queryFn: api.listPatches })
  const { data: snapshots = [] } = useQuery<Snapshot[]>({ queryKey: ['snapshots'], queryFn: api.listSnapshots })
  const { data: renders = [] } = useQuery<RenderedEvent[]>({ queryKey: ['renders'], queryFn: api.listRenders })

  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-4">
        <div className="panel"><p className="text-sm text-slate-500">Evidence</p><p className="text-3xl font-bold">{evidence.length}</p></div>
        <div className="panel"><p className="text-sm text-slate-500">Patch</p><p className="text-3xl font-bold">{patches.length}</p></div>
        <div className="panel"><p className="text-sm text-slate-500">Snapshot</p><p className="text-3xl font-bold">{snapshots.length}</p></div>
        <div className="panel"><p className="text-sm text-slate-500">Recent Renders</p><p className="text-3xl font-bold">{renders.length}</p></div>
      </div>
      <div className="panel">
        <h3 className="mb-2 font-semibold">최근 렌더 결과</h3>
        <div className="space-y-2">
          {renders.slice(0, 3).map((item) => (
            <div key={item.render_id} className="rounded-lg border p-3">
              <div className="mb-2 flex items-center gap-2">
                <Badge text={item.label} tone="green" />
                <Badge text={String(item.provenance?.watermark ?? 'NOT_FACT')} tone="red" />
              </div>
              <p className="text-sm">{String(item.rendered_event?.message ?? '')}</p>
            </div>
          ))}
        </div>
        <p className="mt-3 text-xs text-slate-500">모든 결과는 사실이 아닌 가능역 렌더입니다.</p>
      </div>
    </div>
  )
}
