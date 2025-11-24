// Centralized configuration
// Handles Render's "host" only environment variable by prepending https://

const getApiUrl = () => {
    let url = import.meta.env.VITE_API_URL || "http://localhost:8000"

    // If it's just a hostname (no protocol), assume https
    if (!url.startsWith("http")) {
        url = `https://${url}`
    }

    // Remove trailing slash if present
    if (url.endsWith("/")) {
        url = url.slice(0, -1)
    }

    return url
}

export const API_URL = getApiUrl()
