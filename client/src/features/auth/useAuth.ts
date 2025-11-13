import { useContext } from "react"
import { AuthContext } from "./authContext"
import type { AuthContextValue } from "./context"

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext) as AuthContextValue | undefined
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider")
  }
  return context
}
