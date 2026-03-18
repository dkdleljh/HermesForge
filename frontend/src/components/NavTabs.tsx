type Props = {
  tabs: string[]
  active: string
  onChange: (tab: string) => void
}

export default function NavTabs({ tabs, active, onChange }: Props) {
  return (
    <div className="panel flex flex-wrap gap-2">
      {tabs.map((tab) => (
        <button
          key={tab}
          onClick={() => onChange(tab)}
          className={`rounded-lg px-3 py-2 text-sm font-semibold ${
            active === tab ? 'bg-brand-600 text-white' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
          }`}
        >
          {tab}
        </button>
      ))}
    </div>
  )
}
