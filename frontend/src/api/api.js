const BASE_URL = "http://localhost:8000"

// Token related functions
export const setToken = () => {
    return localStorage.setItem("token", token);
}

export const getToken = () => {
    return localStorage.getItem("token");   
}

export const removeItwm = () => {
    return localStorage.removeItem("token");
}

// Backend communicating function (Main)

const request = async (endpoint, options = {}) => {
    const token = getToken();

    const headers = {
        "Content-type": "application/json",
        ...(token && { Authorization: `bearer ${token}`})
    }

    const response = await (`${BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });
}   