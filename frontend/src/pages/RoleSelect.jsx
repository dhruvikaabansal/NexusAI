import { useNavigate } from 'react-router-dom'

function RoleSelect({ user }) {
    const navigate = useNavigate()

    // In a real app, user.roles would be a list. 
    // For this demo, we'll just show the assigned role and maybe a "Demo Switch" option.

    const roles = [user.role, "CEO", "CFO", "COO", "HR"] // Allow switching for demo purposes
    const uniqueRoles = [...new Set(roles)]

    return (
        <div className="flex items-center justify-center h-screen bg-dark">
            <div className="glass-panel p-8 w-96 text-center">
                <h2 className="text-xl font-bold mb-4">Select Role</h2>
                <p className="mb-6 text-gray-400">Welcome, {user.name}</p>

                <div className="space-y-3">
                    {uniqueRoles.map(role => (
                        <button
                            key={role}
                            onClick={() => navigate(`/dashboard/${role}`)}
                            className="w-full p-3 rounded border border-white/10 hover:bg-white/5 transition-colors text-left flex justify-between items-center"
                        >
                            <span>{role} Dashboard</span>
                            {role === user.role && <span className="text-xs bg-primary px-2 py-1 rounded">Assigned</span>}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default RoleSelect
