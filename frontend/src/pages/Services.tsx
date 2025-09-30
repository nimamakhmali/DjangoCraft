import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { api } from '../lib/api'

type Service = {
	id: number
	title: string
	description: string
	price: string
	category?: number
}

export default function ServicesPage() {
	const { data, isLoading, error } = useQuery({
		queryKey: ['services'],
		queryFn: async () => (await api.get('/services/list/')).data.services as Service[],
	})

	const queryClient = useQueryClient()
	const createOrder = useMutation({
		mutationFn: async (items: { title: string; price: number; qty: number }[]) => {
			const { data } = await api.post('/orders/create/', { items })
			return data as { order_id: number; total: number }
		},
	})

	const initiatePayment = useMutation({
		mutationFn: async (order_id: number) => {
			const { data } = await api.post('/payments/initiate/', { order_id, payment_method: 'mock' })
			return data as { payment_id: string; confirmation_code?: string }
		},
	})

	if (isLoading) return <div>Loading services…</div>
	if (error) return <div className="text-red-600">Failed to load services</div>

	return (
		<div>
			<h1 className="text-xl font-semibold mb-4">Services</h1>
			<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
				{data?.map(s => (
					<div key={s.id} className="bg-white rounded border p-4">
						<h3 className="font-medium">{s.title}</h3>
						<p className="text-sm text-gray-600 line-clamp-3">{s.description}</p>
						<div className="mt-2 font-semibold">${s.price}</div>
						<button
							className="mt-3 w-full text-sm border rounded px-3 py-1"
							onClick={async ()=>{
								try {
									const order = await createOrder.mutateAsync([{ title: s.title, price: Number(s.price), qty: 1 }])
									const pay = await initiatePayment.mutateAsync(order.order_id)
									if ((pay as any).confirmation_code) {
										const code = prompt('Enter confirmation code shown (mock):', (pay as any).confirmation_code)
										if (code) await api.post('/payments/confirm/', { payment_id: (pay as any).payment_id, confirmation_code: code })
										alert('Payment flow finished (mock).')
									}
								} catch (e) { alert('Failed to purchase') }
							}}
						>
							Quick Buy
						</button>
					</div>
				))}
			</div>
		</div>
	)
}


