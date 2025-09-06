import { useEffect, useMemo, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, useMapEvents } from 'react-leaflet'
import L from 'leaflet'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import 'leaflet/dist/leaflet.css'

const markerIcon = new L.Icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41]
})

function DraggableMarker({ position, setPosition }) {
  const [draggable, setDraggable] = useState(true)
  const dragHandlers = useMemo(
    () => ({
      dragend(e) {
        const m = e.target
        setPosition(m.getLatLng())
      },
    }),
    [setPosition]
  )
  useMapEvents({
    click(e) {
      setPosition(e.latlng)
    }
  })
  return (
    <Marker draggable={draggable} eventHandlers={dragHandlers} position={position} icon={markerIcon}>
      <Popup minWidth={200}>
        <div className="text-sm">
          Drag or click map to update location
          <div className="mt-1 text-xs text-slate-500">{position.lat.toFixed(5)}, {position.lng.toFixed(5)}</div>
        </div>
      </Popup>
    </Marker>
  )
}

export default function MapPage() {
  const [position, setPosition] = useState({ lat: 26.449, lng: 80.331 })
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [category, setCategory] = useState('plumbing')

  useEffect(() => {
    toast.success('Map ready! Drag the pin or click to set location.', { id: 'map-ready' })
  }, [])

  function submit() {
    toast.promise(new Promise((res) => setTimeout(res, 600)), {
      loading: 'Submitting complaint...',
      success: 'Complaint submitted!',
      error: 'Failed to submit'
    })
  }

  return (
    <div className="grid lg:grid-cols-2 gap-4">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.2 }} className="bg-white border rounded-lg overflow-hidden">
        <MapContainer center={[position.lat, position.lng]} zoom={15} style={{ height: 420 }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <DraggableMarker position={position} setPosition={setPosition} />
        </MapContainer>
      </motion.div>
      <motion.div initial={{ x: 10, opacity: 0 }} animate={{ x: 0, opacity: 1 }} transition={{ duration: 0.25 }} className="bg-white border rounded-lg p-4">
        <h2 className="text-lg font-semibold mb-3">Submit Complaint</h2>
        <div className="space-y-3">
          <div>
            <label className="block text-sm text-slate-600">Title</label>
            <input value={title} onChange={e=>setTitle(e.target.value)} className="mt-1 w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500" />
          </div>
          <div>
            <label className="block text-sm text-slate-600">Description</label>
            <textarea value={description} onChange={e=>setDescription(e.target.value)} className="mt-1 w-full border rounded px-3 py-2 h-24 focus:outline-none focus:ring-2 focus:ring-brand-500" />
          </div>
          <div>
            <label className="block text-sm text-slate-600">Category</label>
            <select value={category} onChange={e=>setCategory(e.target.value)} className="mt-1 w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand-500">
              <option>plumbing</option>
              <option>electricity</option>
              <option>sewage</option>
              <option>elevator</option>
              <option>security</option>
              <option>housekeeping</option>
              <option>other</option>
            </select>
          </div>
          <div className="text-sm text-slate-600">Location: <span className="font-mono">{position.lat.toFixed(5)}, {position.lng.toFixed(5)}</span></div>
          <button onClick={submit} className="bg-brand-600 hover:bg-brand-700 text-white rounded px-3 py-2 transition">Submit</button>
        </div>
      </motion.div>
    </div>
  )
}

