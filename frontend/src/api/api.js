const BASE_URL = "http://localhost:8000"

// Token related functions

export const getToken = () => {
    return localStorage.getItem("token");   
}

export const setToken = () => {
    return localStorage.setItem("token", token);
}