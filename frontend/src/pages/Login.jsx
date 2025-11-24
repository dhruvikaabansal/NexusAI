import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { signInWithPopup } from 'firebase/auth'
import { auth, googleProvider } from '../firebase'

import { API_URL } from '../config'

function Login({ setUser }) {
    const [email, setEmail] = useState('alice@acme.com')
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const navigate = useNavigate()

    const handleBackendLogin = async (email) => {
        try {
            // Exchange email for Role/User details from our backend DB
            const res = await axios.post(`${API_URL}/auth/login`, { email, password: 'firebase-auth' })
            setUser(res.data)
            navigate(`/dashboard/${res.data.role}`)
        } catch (err) {
            console.error(err)
            setError('Login failed. User might not exist in NexusAI DB.')
        } finally {
            setLoading(false)
        }
    }

    const handleDemoLogin = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError('')
        await handleBackendLogin(email)
    }

    const handleGoogleLogin = async () => {
        setLoading(true)
        setError('')
        try {
            const result = await signInWithPopup(auth, googleProvider)
            const userEmail = result.user.email
            await handleBackendLogin(userEmail)
        } catch (error) {
            console.error(error)
            setError('Google Sign-In failed.')
            setLoading(false)
        }
    }

    return (
        <div className="flex items-center justify-center h-screen bg-dark">
            <div className="glass-panel p-8 w-96">
                <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-primary/20 rounded-2xl flex items-center justify-center mx-auto mb-4 backdrop-blur-md border border-primary/30">
                        <span className="text-3xl">🧠</span>
                    </div>
                    <h1 className="text-3xl font-bold text-white mb-2">NexusAI</h1>
                    <p className="text-gray-400">Enterprise Intelligence Portal</p>
                </div>

                {/* Google Login */}
                <button
                    onClick={handleGoogleLogin}
                    disabled={loading}
                    className="w-full bg-white text-gray-900 font-bold py-2 px-4 rounded mb-4 flex items-center justify-center gap-2 hover:bg-gray-100 transition-colors"
                >
                    <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" className="w-5 h-5" />
                    Sign in with Google
                </button>

                <div className="relative my-6">
                    <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t border-white/10"></div>
                    </div>
                    <div className="relative flex justify-center text-sm">
                        <span className="px-2 bg-[#1e293b] text-gray-400">Or use demo account</span>
                    </div>
                </div>

                <form onSubmit={handleDemoLogin} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-1">Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="w-full bg-dark/50 border border-white/20 rounded p-2 focus:outline-none focus:border-primary"
                        />
                    </div>
                    {error && <p className="text-red-400 text-sm">{error}</p>}
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full btn-primary disabled:opacity-50"
                    >
                        {loading ? 'Logging in...' : 'Demo Login'}
                    </button>
                </form>

                <div className="mt-4 text-xs text-gray-400">
                    <p>Demo Accounts:</p>
                    <ul className="list-disc pl-4 mt-1">
                        <li>alice@acme.com (CEO)</li>
                        <li>bob@acme.com (CFO)</li>
                        <li>carol@acme.com (COO)</li>
                        <li>dana@acme.com (HR)</li>
                    </ul>
                </div>
            </div>
        </div>
    )
}

export default Login
