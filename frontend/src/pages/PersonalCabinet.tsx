import React from 'react'

const PersonalCabinet: React.FC = () => {
  const [activeTab, setActiveTab] = React.useState<'profile' | 'favorites' | 'places' | 'archive' | 'subscription'>('profile')

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Personal Cabinet</h1>

      <div className="flex gap-4 mb-8 border-b">
        {(['profile', 'favorites', 'places', 'archive', 'subscription'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 capitalize font-semibold border-b-2 ${
              activeTab === tab ? 'border-blue-600 text-blue-600' : 'border-transparent text-gray-600 hover:text-gray-800'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      <div className="bg-white rounded-lg shadow p-8">
        {activeTab === 'profile' && (
          <div>
            <h2 className="text-2xl font-bold mb-4">User Profile</h2>
            <p className="text-gray-600">Profile information will be displayed here</p>
          </div>
        )}
        {activeTab === 'favorites' && (
          <div>
            <h2 className="text-2xl font-bold mb-4">Favorite Wallpapers</h2>
            <p className="text-gray-600">Your favorite wallpapers will appear here</p>
          </div>
        )}
        {activeTab === 'places' && (
          <div>
            <h2 className="text-2xl font-bold mb-4">Places to Visit</h2>
            <p className="text-gray-600">Your wishlist of places will appear here</p>
          </div>
        )}
        {activeTab === 'archive' && (
          <div>
            <h2 className="text-2xl font-bold mb-4">Collection Archive</h2>
            <p className="text-gray-600">Previous themes will appear here</p>
          </div>
        )}
        {activeTab === 'subscription' && (
          <div>
            <h2 className="text-2xl font-bold mb-4">Subscription</h2>
            <p className="text-gray-600">Your subscription details will appear here</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default PersonalCabinet
