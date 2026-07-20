import { Outlet } from 'react-router-dom'
import Header from './Header.jsx'
import Footer from './Footer.jsx'

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col bg-bg">
      <Header />
      <main className="flex-grow pt-[80px]">
        <Outlet />
      </main>
      <Footer />
    </div>
  )
}
