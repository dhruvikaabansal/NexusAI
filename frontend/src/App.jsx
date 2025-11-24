import { Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import RoleSelect from './pages/RoleSelect'
import Dashboard from './pages/Dashboard'
import { useState } from 'react'

function App() {
    const [user, setUser] = useState(null)

    return (
        <div className="min-h-screen bg-dark">
            <Routes>
                <Route path="/login" element={<Login setUser={setUser} />} />
                <Route path="/role-select" element={user ? <RoleSelect user={user} /> : <Navigate to="/login" />} />
                <Route path="/dashboard/:role" element={user ? <Dashboard user={user} /> : <Navigate to="/login" />} />
                <Route path="/" element={<Navigate to="/login" />} />
            </Routes>
        </div>
    )
}

export default App
