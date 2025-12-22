import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Navigate } from "react-router";

const ProtectedRoute = ({ children }) => {
    const {loading, isAuthenticated }= useContext(AuthContext)
}