import { motion } from 'framer-motion'

const Card = ({ title, value, delay = 0 }) => (
  <motion.div initial={{ y: 10, opacity: 0 }} animate={{ y: 0, opacity: 1 }} transition={{ delay, duration: 0.25 }}
    className="bg-white border rounded-lg p-4 shadow-sm">
    <div className="text-sm text-slate-500">{title}</div>
    <div className="text-2xl font-semibold mt-1">{value}</div>
  </motion.div>
)

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card title="Open Complaints" value="12" />
        <Card title="SLA Breaches Today" value="1" delay={0.05} />
        <Card title="Avg Response (7d)" value="48m" delay={0.1} />
        <Card title="Worker Utilization" value="72%" delay={0.15} />
      </div>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.3 }} className="bg-white border rounded-lg p-6">
        <div className="text-sm text-slate-500 mb-2">Activity</div>
        <div className="h-40 grid place-items-center text-slate-400">Charts TBD</div>
      </motion.div>
    </div>
  )
}

