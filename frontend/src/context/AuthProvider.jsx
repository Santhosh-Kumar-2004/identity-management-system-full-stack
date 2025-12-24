import { useState, useEffect } from "react"; 
import { 
    loginUser,
    getCurrentUser,
    setToken,
    removeToken,
} from "../api/api";
import { AuthContext } from "./AuthContext";

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

    useEffect(() => {
        const loadUser = async () => {
            try {
                const userData = await getCurrentUser()
                setUser(userData)
                setIsAuthenticated(true)
            } catch (error) {
                setUser(null)
                setIsAuthenticated(false)
                console.log(error)
            } finally {
                setLoading(false)
            }
        }

        loadUser()
    }, [])

    return (
        <AuthContext.Provider
            value={{
                user,
                isAuthenticated,
                login,
                logout,
                loading
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};


