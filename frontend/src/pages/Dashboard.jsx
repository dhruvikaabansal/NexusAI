import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import axios from 'axios'
import RoleKPI from '../components/RoleKPI'
import ChartCard from '../components/ChartCard'
import Chatbot from '../components/Chatbot'
import { LogOut, UserCircle } from 'lucide-react'

import { API_URL } from '../config'

function Dashboard({ user }) {
    const { role } = useParams()
    const navigate = useNavigate()
    const [data, setData] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true)
            try {
                const res = await axios.get(`${API_URL}/dashboards/${role}`)
                setData(res.data)
            } catch (err) {
                setError('Failed to load dashboard data.')
            } finally {
                setLoading(false)
            }
        }

        if (role) {
            fetchData()
        }
    }, [role])

    const handleLogout = () => {
        navigate('/login')
        window.location.reload() // Simple reset
    }

    if (loading) return <div className="flex items-center justify-center h-screen text-primary">Loading Dashboard...</div>
    if (error) return <div className="flex items-center justify-center h-screen text-red-400">{error}</div>
    if (!data) return null

    return (
        <div className="min-h-screen bg-dark p-6 pb-24">
            {/* Header */}
            <header className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white">NexusAI <span className="text-primary">Intelligence</span></h1>
                    <p className="text-gray-400">Welcome, {user.name}</p>
                </div>

                <div className="flex items-center gap-4">
                    <div className="bg-white/5 px-4 py-2 rounded-full flex items-center gap-2 border border-white/10">
                        <UserCircle size={20} className="text-primary" />
                        <span className="font-semibold text-sm">{role} View</span>
                    </div>
                    <button
                        onClick={handleLogout}
                        className="p-2 hover:bg-white/10 rounded-full transition-colors text-gray-400 hover:text-white"
                        title="Logout"
                    >
                        <LogOut size={20} />
                    </button>
                </div>
            </header>

            {/* KPIs */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {data.kpis.map((kpi, idx) => (
                    <RoleKPI key={idx} {...kpi} />
                ))}
            </div>

            {/* Charts */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                {data.charts.map((chart, idx) => (
                    <ChartCard key={idx} {...chart} />
                ))}
            </div>

            {/* Recommended Actions */}
            {data.actions && (
                <div className="mb-8">
                    <h2 className="text-xl font-bold text-white mb-4">Recommended Actions</h2>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {data.actions.map((action, idx) => (
                            <div key={idx} className="glass-panel p-4 flex items-center justify-between border-l-4 border-l-primary">
                                <div>
                                    <h3 className="font-semibold text-white">{action.title}</h3>
                                    <span className={`text-xs px-2 py-1 rounded mt-1 inline-block ${action.priority === 'High' ? 'bg-red-500/20 text-red-400' :
                                        action.priority === 'Medium' ? 'bg-yellow-500/20 text-yellow-400' :
                                            'bg-blue-500/20 text-blue-400'
                                        }`}>
                                        {action.priority} Priority
                                    </span>
                                </div>
                                <button className="text-sm bg-white/10 hover:bg-white/20 px-3 py-1 rounded transition-colors">
                                    View
                                </button>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Chatbot */}
            <Chatbot role={role} userId={String(user.user_id)} />
        </div>
    )
}

export default Dashboard
