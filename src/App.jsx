import { Routes, Route } from 'react-router-dom'
import HomePage from './pages/index.jsx'
import ProblemViewer from './pages/problem/[id].jsx'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/problem/:id" element={<ProblemViewer />} />
      </Routes>
    </div>
  )
}

export default App 