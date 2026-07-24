import React from 'react'

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen">
      <section className="hero bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4">Window to RUSSIA</h1>
          <p className="text-xl mb-8">Discover the beauty and heritage of Russia through daily wallpapers</p>
          <button className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">
            Explore Today's Theme
          </button>
        </div>
      </section>

      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-8 text-center">Today's Featured Theme</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white rounded-lg shadow-lg overflow-hidden">
              <img src="/placeholder.jpg" alt="Theme" className="w-full h-64 object-cover" />
              <div className="p-6">
                <h3 className="text-xl font-bold mb-2">Moscow - The Heart of Russia</h3>
                <p className="text-gray-600 mb-4">
                  Explore the beautiful capital city and discover its rich history and culture.
                </p>
                <p className="text-sm text-gray-500">Available wallpapers: 10</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default HomePage
