import { useState, useEffect, useContext, createContext } from "react"; 
import { 
    loginUser,
    registerUser,
    getCurrentUser,
    setToken,
    removeToken,
    updateUser
} from "../api/api";

export const AuthContext = createContext(null)

