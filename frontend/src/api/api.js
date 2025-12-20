const BASE_URL = "http://localhost:8000"

// Token related functions
export const setToken = () => {
    return localStorage.setItem("token", token);
}

export const getToken = () => {
    return localStorage.getItem("token");   
}

export const removeToken = () => {
    return localStorage.removeItem("token");
}

// Backend communicating function (Main)

const request = async (endpoint, options = {}) => {
    const token = getToken();

    const headers = {
        "Content-type": "application/json",
        ...(token && { Authorization: `bearer ${token}`})
    }

    const response = await fetch(`${BASE_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail() || "Request Failed, Try Again...")
    }

    return response.json();
}   

// Auth related functions

export const loginUser = (data) => {
    return request("/auth/login", {
        method: "POST",
        body: JSON.stringify(data)
    })
}

export const registerUser = (data) => {
    return request("auth/register", {
        method: "POST",
        body: JSON.stringify(data)
    })
}

export const getCurrentUser = () => {
    return request("auth/user", {
        method: "GET",
    })
}

export const updateUser = (data) => {
    return request("auth/update-user", {
        method: "PUT",
        body: JSON.stringify(data)
    })
}

export const logoutUser = () => {
    return request("auth/logout", {
        method: "POST",
        removeItem()
    })
}