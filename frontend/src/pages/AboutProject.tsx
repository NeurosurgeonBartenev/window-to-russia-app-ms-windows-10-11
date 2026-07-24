import React from 'react'

const AboutProject: React.FC = () => {
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">About Window to RUSSIA</h1>
      
      <div className="prose max-w-4xl">
        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Our Mission</h2>
          <p className="text-gray-700 text-lg">
            Window to RUSSIA is dedicated to showcasing the beauty, culture, and heritage of Russia through 
            carefully curated daily wallpapers. We believe that every corner of Russia has a story to tell.
          </p>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Features</h2>
          <ul className="list-disc list-inside text-gray-700 space-y-2">
            <li>Daily themed wallpaper collections</li>
            <li>High-resolution images (4K+)</li>
            <li>Educational content about Russian regions and heritage sites</li>
            <li>Personal favorites and wishlist</li>
            <li>Multi-language support (8 languages)</li>
            <li>Automatic wallpaper rotation</li>
          </ul>
        </section>

        <section className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Supported Languages</h2>
          <p className="text-gray-700">
            Russian • English • Chinese • German • Italian • French • Japanese • Spanish
          </p>
        </section>
      </div>
    </div>
  )
}

export default AboutProject
