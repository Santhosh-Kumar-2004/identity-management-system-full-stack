import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Navigate } from "react-router";
import { getToken } from "../api/api";

const ProtectedRoute = ({ children }) => {
    const {loading, isAuthenticated }= useContext(AuthContext)

    if (!getToken) {
        return <Navigate to="/login" replace/>
    }

    if (loading) {
        return <p>The App is Loading...</p>
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace/>
    }

    return children;
}

export default ProtectedRoute;