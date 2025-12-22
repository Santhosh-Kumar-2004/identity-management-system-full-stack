import { AuthContext } from "../context/AuthContext";
import { Navigate } from "react-router";
import { useContext } from "react";

const AdminRoute = ({ children }) => {
    const { loading, user, isAuthenticated } = useContext(AuthContext)
}