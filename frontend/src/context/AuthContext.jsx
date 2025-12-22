import { useState, useEffect, useContext, createContext, Children } from "react"; 
import { 
    loginUser,
    registerUser,
    getCurrentUser,
    setToken,
    removeToken,
    updateUser
} from "../api/api";

export const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {

    const [user, setUser] = useState(null)

    const [isAuthenticated, setIsAuthenticated] = useState(false)

    const [loading, setLoading] = useState(true)

    const login = async (email, password) => {
        const response = loginUser({ email, password })

        setToken(response.access_token)

        const userData = getCurrentUser()

        setUser(userData)
        setIsAuthenticated(true)
    }

    const logout = () => {
        removeToken()
        setIsAuthenticated(false)
        setUser(null)
    }
}

