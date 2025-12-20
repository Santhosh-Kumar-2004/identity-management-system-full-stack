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
}