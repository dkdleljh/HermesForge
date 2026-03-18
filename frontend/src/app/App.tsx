import { useState } from 'react'
import NavTabs from '../components/NavTabs'
import DashboardPage from '../pages/DashboardPage'
import DemoPage from '../pages/DemoPage'
import EvidencePage from '../pages/EvidencePage'
import MaterializePage from '../pages/MaterializePage'
import PatchPage from '../pages/PatchPage'
import SnapshotPage from '../pages/SnapshotPage'

const tabs = ['대시보드', 'Evidence', 'Patch', 'Snapshot', 'Materialize', 'Demo']

export default function App() {
  const [active, setActive] = useState(tabs[0])

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-100 via-white to-brand-50 p-4 md:p-8">
      <div className="mx-auto max-w-6xl space-y-4">
        <header className="panel">
          <h1 className="text-2xl font-extrabold text-slate-800">HermesForge</h1>
          <p className="text-sm text-slate-600">POSSIBILITY FIELD ENGINE / NOT FACT</p>
        </header>
        <NavTabs tabs={tabs} active={active} onChange={setActive} />
        {active === '대시보드' && <DashboardPage />}
        {active === 'Evidence' && <EvidencePage />}
        {active === 'Patch' && <PatchPage />}
        {active === 'Snapshot' && <SnapshotPage />}
        {active === 'Materialize' && <MaterializePage />}
        {active === 'Demo' && <DemoPage />}
      </div>
    </main>
  )
}
