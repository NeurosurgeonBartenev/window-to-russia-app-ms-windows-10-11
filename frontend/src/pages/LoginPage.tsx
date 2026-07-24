import React from 'react'

const LoginPage: React.FC = () => {
  const providers = [
    'Google', 'Yandex', 'VK', 'X (Twitter)', 'Apple', 'Microsoft',
    'WeChat', 'QQ', 'WhatsApp', 'Telegram', 'Snapchat', 'Instagram',
    'LINE', 'KakaoTalk', 'Facebook'
  ]

  return (
    <div className="min-h-screen bg-gradient-to-r from-blue-600 to-purple-600 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md w-full">
        <h1 className="text-3xl font-bold text-center mb-2">Window to RUSSIA</h1>
        <p className="text-center text-gray-600 mb-8">Sign in to your account</p>

        <div className="space-y-3">
          {providers.map((provider) => (
            <button
              key={provider}
              className="w-full bg-gray-100 hover:bg-gray-200 text-gray-800 font-semibold py-3 px-4 rounded-lg transition-colors"
            >
              Sign in with {provider}
            </button>
          ))}
        </div>

        <p className="text-center text-sm text-gray-600 mt-8">
          By signing in, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  )
}

export default LoginPage
