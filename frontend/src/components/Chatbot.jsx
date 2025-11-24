import { useState, useRef, useEffect } from 'react'
import { MessageSquare, X, Send, Bot, User } from 'lucide-react'
import axios from 'axios'

const API_URL = "http://localhost:8000"

function Chatbot({ role, userId }) {
    const [isOpen, setIsOpen] = useState(false)
    const [messages, setMessages] = useState([
        { type: 'bot', text: `Hello! I am your ${role} Assistant. Ask me about ${role === 'CEO' ? 'strategy and risk' : role === 'COO' ? 'production and downtime' : 'data'}.` }
    ])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const [suggestions, setSuggestions] = useState([])
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const handleSend = async (text = input) => {
        if (!text.trim()) return

        const userMsg = { type: 'user', text }
        setMessages(prev => [...prev, userMsg])
        setInput('')
        setLoading(true)

        try {
            const res = await axios.post(`${API_URL}/chat/`, {
                user_id: userId || "demo",
                role: role,
                query: text
            })

            const botMsg = {
                type: 'bot',
                text: res.data.answer,
                sources: res.data.sources
            }
            setMessages(prev => [...prev, botMsg])
            setSuggestions(res.data.suggested_followups || [])
        } catch (err) {
            setMessages(prev => [...prev, { type: 'bot', text: "Sorry, I encountered an error connecting to the server." }])
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="fixed bottom-6 right-6 z-50">
            {!isOpen && (
                <button
                    onClick={() => setIsOpen(true)}
                    className="bg-primary hover:bg-blue-600 text-white p-4 rounded-full shadow-lg transition-all transform hover:scale-110"
                >
                    <MessageSquare size={24} />
                </button>
            )}

            {isOpen && (
                <div className="glass-panel w-96 h-[500px] flex flex-col shadow-2xl animate-in fade-in slide-in-from-bottom-10 duration-300">
                    {/* Header */}
                    <div className="p-4 border-b border-white/10 flex justify-between items-center bg-white/5 rounded-t-xl">
                        <div className="flex items-center gap-2">
                            <Bot size={20} className="text-primary" />
                            <h3 className="font-semibold">AI Assistant ({role})</h3>
                        </div>
                        <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-white">
                            <X size={20} />
                        </button>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {messages.map((msg, idx) => (
                            <div key={idx} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                                <div className={`max-w-[80%] p-3 rounded-lg text-sm ${msg.type === 'user'
                                        ? 'bg-primary text-white rounded-br-none'
                                        : 'bg-white/10 text-gray-100 rounded-bl-none'
                                    }`}>
                                    <p>{msg.text}</p>
                                    {msg.sources && msg.sources.length > 0 && (
                                        <div className="mt-2 pt-2 border-t border-white/10 text-xs text-gray-400">
                                            Sources: {msg.sources.join(', ')}
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                        {loading && (
                            <div className="flex justify-start">
                                <div className="bg-white/10 p-3 rounded-lg rounded-bl-none flex gap-1">
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75" />
                                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150" />
                                </div>
                            </div>
                        )}
                        <div ref={messagesEndRef} />
                    </div>

                    {/* Suggestions */}
                    {suggestions.length > 0 && !loading && (
                        <div className="p-2 border-t border-white/10 overflow-x-auto flex gap-2 no-scrollbar">
                            {suggestions.map((s, i) => (
                                <button
                                    key={i}
                                    onClick={() => handleSend(s)}
                                    className="whitespace-nowrap px-3 py-1 bg-white/5 hover:bg-white/10 rounded-full text-xs text-primary border border-primary/30 transition-colors"
                                >
                                    {s}
                                </button>
                            ))}
                        </div>
                    )}

                    {/* Input */}
                    <div className="p-4 border-t border-white/10 flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                            placeholder="Ask a question..."
                            className="flex-1 bg-dark/50 border border-white/20 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary"
                        />
                        <button
                            onClick={() => handleSend()}
                            disabled={loading || !input.trim()}
                            className="p-2 bg-primary hover:bg-blue-600 rounded-lg text-white disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                        >
                            <Send size={18} />
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}

export default Chatbot
