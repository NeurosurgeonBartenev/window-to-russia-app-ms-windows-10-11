import React from 'react'

const TodayThemePage: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Today's Theme Collection</h1>
      
      <section className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Theme Description</h2>
        <p className="text-gray-700 text-lg">
          Discover the wonders of Moscow, the heart of Russia...
        </p>
      </section>

      <section>
        <h2 className="text-2xl font-bold mb-6">Available Wallpapers</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
          {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((i) => (
            <div key={i} className="bg-white rounded-lg shadow hover:shadow-lg transition-shadow cursor-pointer">
              <div className="aspect-video bg-gray-300 mb-3">
                <img src={`/placeholder-${i}.jpg`} alt={`Wallpaper ${i}`} className="w-full h-full object-cover" />
              </div>
              <div className="p-3">
                <h3 className="font-semibold text-sm mb-1">Location {i}</h3>
                <p className="text-xs text-gray-600 mb-2">Description of the place...</p>
                <div className="flex gap-2">
                  <button className="flex-1 text-xs bg-blue-500 text-white py-1 rounded hover:bg-blue-600">
                    ❤️ Like
                  </button>
                  <button className="flex-1 text-xs bg-gray-200 py-1 rounded hover:bg-gray-300">
                    📍 Visit
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default TodayThemePage
