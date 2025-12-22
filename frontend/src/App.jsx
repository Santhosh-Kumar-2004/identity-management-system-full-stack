import { useState } from 'react'
import { Route, Routes } from 'react-router'

import ProtectedRoute from './routes/ProtectedRoute'
import AdminRoute from './routes/AdminRoute'

import Login from './pages/auth/Login'
import Register from './pages/auth/Register'


function App() {

  return (
    <>
      <h1>Hello World</h1>
    </>
  )
}

export default App
