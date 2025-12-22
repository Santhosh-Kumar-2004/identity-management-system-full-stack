import { useState } from 'react'
import { Route, Routes } from 'react-router'

import ProtectedRoute from './routes/ProtectedRoute'
import AdminRoute from './routes/AdminRoute'

import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import Home from './pages/public/Home'
import AllUsers from './pages/admin/UserDetails'
import Profile from './pages/user/Profile'


function App() {

  return (
    <>
      <Routes>
        {/* public auth Pages */}
        <Route path='/login' element={<Login />} />
        <Route path='/register' element={<Register />} />

        {/* prontected route pages */}
        <Route 
          path='/'
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />

        <Route 
          path='/profile'
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />

        {/* admin route pages are here */}
        
      </Routes>
    </>
  )
}

export default App
