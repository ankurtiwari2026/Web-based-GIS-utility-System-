import { motion } from 'framer-motion'

export default function Technician() {
  return (
    <div className="space-y-4">
      <motion.h1 initial={{ x: -10, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ duration: 0.2 }} className="text-xl font-semibold">Technician Console</motion.h1>
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.1 }} className="bg-white border rounded-lg p-4">
        <div className="h-40 grid place-items-center text-slate-400">Assignments TBD</div>
      </motion.div>
    </div>
  )
}

