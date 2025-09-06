import { motion } from 'framer-motion'

export default function Login() {
  return (
    <div className="max-w-md mx-auto">
      <motion.div initial={{ scale: 0.98, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: 0.25 }}
        className="bg-white rounded-lg shadow-sm border p-6">
        <h1 className="text-xl font-semibold mb-4">Login</h1>
        <form className="space-y-3">
          <div>
            <label className="block text-sm text-slate-600">Email</label>
            <input className="mt-1 w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500" placeholder="you@example.com" />
          </div>
          <div>
            <label className="block text-sm text-slate-600">Password</label>
            <input type="password" className="mt-1 w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500" placeholder="••••••••" />
          </div>
          <button type="button" className="w-full bg-brand-600 hover:bg-brand-700 text-white rounded px-3 py-2 transition">Sign in</button>
        </form>
      </motion.div>
    </div>
  )
}

