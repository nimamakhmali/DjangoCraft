import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'

type Summary = {
	users_total: number
	services_total: number
	services_pending: number
	services_approved: number
	services_rejected: number
	payments_total: number
	payments_completed: number
	revenue_total: number
}

export default function AdminPage() {
	const { data, isLoading, error } = useQuery({
		queryKey: ['admin-summary'],
		queryFn: async () => (await api.get('/services/admin/summary/')).data as Summary,
	})

    if (isLoading) return <div>Loading summary…</div>
    if (error) return <div className="text-red-600">Admins only. Please login with a staff user.</div>

	return (
		<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
			{Object.entries(data || {}).map(([k,v]) => (
				<div key={k} className="bg-white rounded border p-4">
					<div className="text-xs uppercase text-gray-500">{k.replaceAll('_',' ')}</div>
					<div className="text-2xl font-semibold">{String(v)}</div>
				</div>
			))}
		</div>
	)
}


