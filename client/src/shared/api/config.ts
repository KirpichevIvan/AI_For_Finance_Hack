import axios from "axios"

type Tokens = {
  accessToken: string
  refreshToken: string
}

export class TokenStorage {
  static getTokens(): Tokens | null {
    const stored = localStorage.getItem("authTokens")
    return stored ? JSON.parse(stored) : null
  }

  static setTokens(tokens: Tokens): void {
    localStorage.setItem("authTokens", JSON.stringify(tokens))
  }

  static removeTokens(): void {
    localStorage.removeItem("authTokens")
  }

  static getAccessToken(): string | null {
    return this.getTokens()?.accessToken || null
  }

  static getRefreshToken(): string | null {
    return this.getTokens()?.refreshToken || null
  }
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

api.interceptors.request.use(
  config => {
    const token = TokenStorage.getAccessToken()
    if (!token) return config

    return {
      ...config,
      headers: {
        ...(config.headers || {}),
        Authorization: `Bearer ${token}`,
      },
    } as typeof config
  },
  error => Promise.reject(error)
)

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest.headers?.["x-retry"]) {
      const refreshToken = TokenStorage.getRefreshToken()
      if (!refreshToken) {
        TokenStorage.removeTokens()
        window.location.href = "/login"
        return Promise.reject(error)
      }

      try {
        const formData = new FormData()
        formData.append("refresh_token", refreshToken)

        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/api/auth/refresh`,
          formData
        )

        if (response.data.status) {
          const tokens = {
            accessToken: response.data.data.access_token,
            refreshToken: response.data.data.refresh_token,
          }
          TokenStorage.setTokens(tokens)

          return await api({
            ...originalRequest,
            headers: {
              ...(originalRequest.headers || {}),
              Authorization: `Bearer ${tokens.accessToken}`,
              "x-retry": "1",
            },
          })
        }
      } catch (refreshError) {
        TokenStorage.removeTokens()
        window.location.href = "/login"
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)
