import { ArrowUp, ArrowDown, Minus } from 'lucide-react'

function RoleKPI({ label, value, trend }) {
    const isPositive = trend.includes('+')
    const isNegative = trend.includes('-')

    return (
        <div className="glass-panel p-4 flex flex-col justify-between h-32">
            <h3 className="text-gray-400 text-sm font-medium uppercase tracking-wider">{label}</h3>
            <div className="flex items-end justify-between">
                <span className="text-3xl font-bold text-white">{value}</span>
                <div className={`flex items-center text-sm ${isPositive ? 'text-green-400' : isNegative ? 'text-red-400' : 'text-gray-400'}`}>
                    {isPositive && <ArrowUp size={16} />}
                    {isNegative && <ArrowDown size={16} />}
                    {!isPositive && !isNegative && <Minus size={16} />}
                    <span className="ml-1">{trend}</span>
                </div>
            </div>
        </div>
    )
}

export default RoleKPI
