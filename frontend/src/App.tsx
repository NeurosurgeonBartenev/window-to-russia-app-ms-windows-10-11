import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from '@/components/Layout'
import HomePage from '@/pages/HomePage'
import TodayThemePage from '@/pages/TodayThemePage'
import PersonalCabinet from '@/pages/PersonalCabinet'
import AboutProject from '@/pages/AboutProject'
import LoginPage from '@/pages/LoginPage'
import '@/styles/globals.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/today-theme" element={<TodayThemePage />} />
          <Route path="/personal-cabinet" element={<PersonalCabinet />} />
          <Route path="/about" element={<AboutProject />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
