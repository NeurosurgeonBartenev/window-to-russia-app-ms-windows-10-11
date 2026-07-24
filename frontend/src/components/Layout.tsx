import React from 'react'
import { Link, Outlet } from 'react-router-dom'

const Layout: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false)

  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-40">
        <nav className="container mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/" className="text-2xl font-bold text-blue-600">
            🪟 RUSSIA
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center gap-6">
            <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">
              Dashboard
            </Link>
            <Link to="/today-theme" className="text-gray-700 hover:text-blue-600 font-medium">
              Today's Theme
            </Link>
            <Link to="/personal-cabinet" className="text-gray-700 hover:text-blue-600 font-medium">
              Personal Cabinet
            </Link>
            <Link to="/about" className="text-gray-700 hover:text-blue-600 font-medium">
              About Project
            </Link>
            <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-medium">
              Login
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            ☰
          </button>
        </nav>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t bg-white">
            <div className="container mx-auto px-4 py-4 flex flex-col gap-4">
              <Link to="/" className="text-gray-700 hover:text-blue-600 font-medium">
                Dashboard
              </Link>
              <Link to="/today-theme" className="text-gray-700 hover:text-blue-600 font-medium">
                Today's Theme
              </Link>
              <Link to="/personal-cabinet" className="text-gray-700 hover:text-blue-600 font-medium">
                Personal Cabinet
              </Link>
              <Link to="/about" className="text-gray-700 hover:text-blue-600 font-medium">
                About Project
              </Link>
              <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-medium w-full">
                Login
              </button>
            </div>
          </div>
        )}
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-lg mb-4">Window to RUSSIA</h3>
              <p className="text-gray-400">Discover Russian beauty through daily wallpapers</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Features</a></li>
                <li><a href="#" className="hover:text-white">Pricing</a></li>
                <li><a href="#" className="hover:text-white">Download</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">About</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
                <li><a href="#" className="hover:text-white">Contact</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Privacy</a></li>
                <li><a href="#" className="hover:text-white">Terms</a></li>
                <li><a href="#" className="hover:text-white">License</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 pt-8 text-center text-gray-400">
            <p>&copy; 2026 Window to RUSSIA. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Layout
