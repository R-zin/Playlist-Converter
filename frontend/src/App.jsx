import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout.jsx'
import Landing from './pages/Landing.jsx'
import Converter from './pages/Converter.jsx'
import Progress from './pages/Progress.jsx'
import Result from './pages/Result.jsx'
import AdminOAuth from './pages/AdminOAuth.jsx'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Landing />} />
        <Route path="/convert" element={<Converter />} />
        <Route path="/progress/:taskId" element={<Progress />} />
        <Route path="/result" element={<Result />} />
        <Route path="/admin" element={<AdminOAuth />} />
      </Route>
    </Routes>
  )
}
