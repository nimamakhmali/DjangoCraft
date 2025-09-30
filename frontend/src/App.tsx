import { Link, Route, Routes, NavLink } from 'react-router-dom'
import './App.css'
import ServicesPage from './pages/Services'
import MessagingPage from './pages/Messaging'
import AdminPage from './pages/Admin'
import { useEffect, useState } from 'react'
import { login as apiLogin, logout as apiLogout, signup as apiSignup, me } from './lib/api'

function Layout({ children }: { children: React.ReactNode }) {
	const [user, setUser] = useState<{username: string} | null>(null)

	useEffect(() => { (async () => {
		try { const u = await me(); setUser({ username: u.username }) } catch (_) { setUser(null) }
	})() }, [])

	async function handleLoginDemo() {
		const username = prompt('Username (demo):') || ''
		const password = prompt('Password:') || ''
		try {
			await apiLogin(username, password)
			const u = await me()
			setUser({ username: u.username })
		} catch (e) {
			alert('Login failed')
		}
	}

	async function handleLogout() {
		await apiLogout()
		setUser(null)
	}

	async function handleSignupDemo() {
		const username = prompt('Choose username:') || ''
		const email = prompt('Email (optional):') || ''
		const password = prompt('Choose password (min 6):') || ''
		try {
			await apiSignup(username, password, email || undefined)
			alert('Signup successful. Now login.')
		} catch (e) {
			alert('Signup failed')
		}
	}
	return (
		<div className="min-h-screen flex flex-col">
			<header className="bg-white shadow">
				<div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
					<Link to="/" className="font-semibold">Student Marketplace</Link>
					<nav className="flex gap-4 text-sm">
						<NavLink to="/services" className={({isActive})=> isActive ? 'text-blue-600' : 'text-gray-600'}>Services</NavLink>
						<NavLink to="/messaging" className={({isActive})=> isActive ? 'text-blue-600' : 'text-gray-600'}>Messaging</NavLink>
						<NavLink to="/admin" className={({isActive})=> isActive ? 'text-blue-600' : 'text-gray-600'}>Admin</NavLink>
					</nav>
					<div className="flex items-center gap-3 text-sm">
						{user ? (
							<>
								<span className="text-gray-600">{user.username}</span>
								<button onClick={handleLogout} className="px-2 py-1 border rounded">Logout</button>
							</>
						) : (
							<>
								<button onClick={handleLoginDemo} className="px-2 py-1 border rounded">Login</button>
								<button onClick={handleSignupDemo} className="px-2 py-1 border rounded">Signup</button>
							</>
						)}
					</div>
				</div>
			</header>
			<main className="flex-1 max-w-6xl mx-auto w-full px-4 py-6">{children}</main>
			<footer className="py-6 text-center text-xs text-gray-500">© {new Date().getFullYear()}</footer>
		</div>
	)
}

function Home() { return <div className="prose"><h1>Welcome</h1><p>Explore services, chat, and pay securely.</p></div> }
function Services() { return <ServicesPage/> }
function Messaging() { return <MessagingPage/> }
function Admin() { return <AdminPage/> }

function App() {
	return (
		<Layout>
			<Routes>
				<Route path="/" element={<Home/>} />
				<Route path="/services" element={<Services/>} />
				<Route path="/messaging" element={<Messaging/>} />
				<Route path="/admin" element={<Admin/>} />
			</Routes>
		</Layout>
	)
}

export default App
