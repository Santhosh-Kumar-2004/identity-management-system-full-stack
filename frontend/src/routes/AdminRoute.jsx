import { AuthContext } from "../context/AuthContext";
import { Navigate } from "react-router";
import { useContext } from "react";

const AdminRoute = ({ children }) => {
    const { loading, user, isAuthenticated } = useContext(AuthContext)

    if (loading) {
        return <p>The App is Loading, Plz Wait Admin...</p>
    }

    if (!isAuthenticated) {
        return <Navigate to="/register" replace/>
    }

    if (user?.role !== "admin") {
        return <Navigate to="/" replace/>
    }
}

export default AdminRoute;