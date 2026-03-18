type Props = {
  text: string
  tone?: 'green' | 'red' | 'gray'
}

export default function Badge({ text, tone = 'gray' }: Props) {
  const cls =
    tone === 'green'
      ? 'badge bg-brand-100 text-brand-700'
      : tone === 'red'
      ? 'badge bg-red-100 text-danger'
      : 'badge bg-slate-200 text-slate-700'

  return <span className={cls}>{text}</span>
}
