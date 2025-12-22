import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Navigate } from "react-router";

const ProtectedRoute = ({ children }) => {
    const {loading, isAuthenticated }= useContext(AuthContext)

    if (loading) {
        return <p>The App is Loading...</p>
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace/>
    }
}