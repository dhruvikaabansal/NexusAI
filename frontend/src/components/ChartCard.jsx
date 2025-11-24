import {
    ResponsiveContainer, LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
    PieChart, Pie, Cell, AreaChart, Area, RadarChart, Radar, PolarGrid, PolarAngleAxis,
    PolarRadiusAxis, ComposedChart, ScatterChart, Scatter, Legend
} from 'recharts'

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']

function ChartCard({ title, type, data, x, y, keys, barKey, lineKey, colors }) {
    const chartColors = colors || COLORS

    return (
        <div className="glass-panel p-6 h-80 flex flex-col">
            <h3 className="text-lg font-semibold mb-4 text-white">{title}</h3>
            <div className="flex-1 w-full min-h-0">
                <ResponsiveContainer width="100%" height="100%">
                    {type === 'line' && (
                        <LineChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey={x} stroke="#94a3b8" fontSize={12} />
                            <YAxis stroke="#94a3b8" fontSize={12} />
                            <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                            <Line type="monotone" dataKey={y} stroke={chartColors[0]} strokeWidth={2} dot={false} />
                        </LineChart>
                    )}
                    {type === 'bar' && (
                        <BarChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey={x} stroke="#94a3b8" fontSize={12} />
                            <YAxis stroke="#94a3b8" fontSize={12} />
                            <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                            <Bar dataKey={y} fill={chartColors[0]} radius={[4, 4, 0, 0]} />
                        </BarChart>
                    )}
                    {type === 'pie' && (
                        <PieChart>
                            <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey={y}>
                                {data.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                                ))}
                            </Pie>
                            <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                            <Legend />
                        </PieChart>
                    )}
                    {type === 'area' && (
                        <AreaChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey={x} stroke="#94a3b8" fontSize={12} />
                            <YAxis stroke="#94a3b8" fontSize={12} />
                            <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                            <Legend />
                            {keys.map((key, idx) => (
                                <Area key={key} type="monotone" dataKey={key} stackId="1" stroke={chartColors[idx]} fill={chartColors[idx]} fillOpacity={0.6} />
                            ))}
                        </AreaChart>
                    )}
                    {type === 'radar' && (
                        <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
                            <PolarGrid stroke="#334155" />
                            <PolarAngleAxis dataKey="subject" stroke="#94a3b8" fontSize={10} />
                            <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#94a3b8" />
                            <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                            <Legend />
                            {keys.map((key, idx) => (
                                <Radar key={key} name={key} dataKey={key} stroke={chartColors[idx]} fill={chartColors[idx]} fillOpacity={0.4} />
                            ))}
                        </RadarChart>
                    )}
                    {type === 'composed' && (
                        <ComposedChart data={data}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis dataKey={x} stroke="#94a3b8" fontSize={12} />
                            <YAxis yAxisId="left" stroke="#94a3b8" fontSize={12} />
                            <YAxis yAxisId="right" orientation="right" stroke="#94a3b8" fontSize={12} />
                            <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                            <Legend />
                            <Bar yAxisId="left" dataKey={barKey} fill={chartColors[0]} radius={[4, 4, 0, 0]} />
                            <Line yAxisId="right" type="monotone" dataKey={lineKey} stroke={chartColors[1]} strokeWidth={2} />
                        </ComposedChart>
                    )}
                    {type === 'scatter' && (
                        <ScatterChart>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                            <XAxis type="number" dataKey={x} name={x} stroke="#94a3b8" fontSize={12} />
                            <YAxis type="number" dataKey={y} name={y} stroke="#94a3b8" fontSize={12} />
                            <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff' }} />
                            <Scatter name="Data" data={data} fill={chartColors[0]} />
                        </ScatterChart>
                    )}
                </ResponsiveContainer>
            </div>
        </div>
    )
}

export default ChartCard
