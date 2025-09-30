import { useQuery } from '@tanstack/react-query'
import { api } from '../lib/api'
import { useEffect } from 'react'

type Conversation = {
	conversation_id: string
	title: string
	last_message_at?: string
	unread_count: number
}

export default function MessagingPage() {
    useEffect(()=>{
        // Soft-guard: if unauthorized, API will 401; page will show prompt via data undefined
    },[])
	const { data, isLoading } = useQuery({
		queryKey: ['conversations'],
		queryFn: async () => (await api.get('/messaging/conversations/')).data.results as Conversation[],
	})

	return (
		<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
			<div className="md:col-span-1">
				<h2 className="font-semibold mb-2">Conversations</h2>
				{isLoading ? 'Loading…' : (
					<div className="space-y-2">
						{data?.map(c => (
							<div key={c.conversation_id} className="bg-white rounded border p-3">
								<div className="flex items-center justify-between">
									<div className="font-medium">{c.title || 'Untitled'}</div>
									{c.unread_count > 0 && (
										<span className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full">{c.unread_count}</span>
									)}
								</div>
								<div className="text-xs text-gray-500">{c.last_message_at || ''}</div>
							</div>
						))}
					</div>
				)}
			</div>
            <div className="md:col-span-2">
                <div className="bg-white rounded border p-4 text-gray-500">
                    {isLoading ? 'Loading…' : (!data ? 'Please login to view your conversations.' : 'Select a conversation')}
                </div>
            </div>
		</div>
	)
}


