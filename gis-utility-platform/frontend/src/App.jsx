import { Routes, Route, NavLink, useLocation } from 'react-router-dom'
import { AnimatePresence, motion } from 'framer-motion'
import Login from './pages/Login.jsx'
import MapPage from './pages/MapPage.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Technician from './pages/Technician.jsx'

const pageVariants = {
  initial: { opacity: 0, y: 10 },
  in: { opacity: 1, y: 0 },
  out: { opacity: 0, y: -10 },
}

export default function App() {
  const location = useLocation()
  return (
    <div className="min-h-full bg-slate-50 text-slate-900">
      <header className="sticky top-0 z-20 backdrop-blur bg-white/70 border-b">
        <nav className="container mx-auto px-4 py-3 flex items-center gap-4">
          <span className="font-semibold text-brand-600">GIS Utility</span>
          <div className="flex gap-3 text-sm">
            <NavLink to="/" className={({isActive}) => `px-2 py-1 rounded transition ${isActive ? 'bg-brand-50 text-brand-700' : 'hover:bg-slate-100'}`}>Dashboard</NavLink>
            <NavLink to="/map" className={({isActive}) => `px-2 py-1 rounded transition ${isActive ? 'bg-brand-50 text-brand-700' : 'hover:bg-slate-100'}`}>Map</NavLink>
            <NavLink to="/technician" className={({isActive}) => `px-2 py-1 rounded transition ${isActive ? 'bg-brand-50 text-brand-700' : 'hover:bg-slate-100'}`}>Technician</NavLink>
            <NavLink to="/login" className={({isActive}) => `px-2 py-1 rounded transition ${isActive ? 'bg-brand-50 text-brand-700' : 'hover:bg-slate-100'}`}>Login</NavLink>
          </div>
        </nav>
      </header>
      <main className="container mx-auto px-4 py-6">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route
              path="/"
              element={
                <motion.div variants={pageVariants} initial="initial" animate="in" exit="out" transition={{ duration: 0.2 }}>
                  <Dashboard />
                </motion.div>
              }
            />
            <Route
              path="/map"
              element={
                <motion.div variants={pageVariants} initial="initial" animate="in" exit="out" transition={{ duration: 0.2 }}>
                  <MapPage />
                </motion.div>
              }
            />
            <Route
              path="/technician"
              element={
                <motion.div variants={pageVariants} initial="initial" animate="in" exit="out" transition={{ duration: 0.2 }}>
                  <Technician />
                </motion.div>
              }
            />
            <Route
              path="/login"
              element={
                <motion.div variants={pageVariants} initial="initial" animate="in" exit="out" transition={{ duration: 0.2 }}>
                  <Login />
                </motion.div>
              }
            />
          </Routes>
        </AnimatePresence>
      </main>
    </div>
  )
}

