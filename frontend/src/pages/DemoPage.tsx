import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useState } from 'react'
import { api } from '../services/api'

export default function DemoPage() {
  const queryClient = useQueryClient()
  const [log, setLog] = useState('')

  const boot = useMutation({
    mutationFn: api.bootstrapDemo,
    onSuccess: (data) => {
      setLog(JSON.stringify(data, null, 2))
      queryClient.invalidateQueries()
    },
  })

  const { data: policies } = useQuery({ queryKey: ['policies'], queryFn: api.policies })

  return (
    <div className="space-y-4">
      <div className="panel">
        <h3 className="mb-2 font-semibold">도메인 시뮬레이션 데모</h3>
        <button className="rounded bg-brand-600 px-3 py-2 text-white" onClick={() => boot.mutate()}>교육/게임/훈련 시드 주입</button>
        <pre className="mt-3 overflow-auto rounded bg-slate-900 p-3 text-xs text-slate-100">{log || '아직 실행 안 됨'}</pre>
      </div>
      <div className="panel">
        <h3 className="mb-2 font-semibold">정책 커널</h3>
        <pre className="overflow-auto rounded bg-slate-100 p-3 text-xs">{JSON.stringify(policies, null, 2)}</pre>
      </div>
    </div>
  )
}
