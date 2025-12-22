import { useState } from 'react'
import { Route, Routes } from 'react-router'

import ProtectedRoute from './routes/ProtectedRoute'
import AdminRoute from './routes/AdminRoute'

import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import Home from './pages/public/Home'
import AllUsers from './pages/admin/UserDetails'


function App() {

  return (
    <>
      <Routes>
        {/* public auth Pages */}
        <Route path='/login' element={<Login />} />
        <Route path='/register' element={<Register />} />
        
      </Routes>
    </>
  )
}

export default App
