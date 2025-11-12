import React from "react"
import ReactDOM from "react-dom/client"
import { App } from "@/app"
import { AuthProvider } from "@/features/auth/context"
import { api } from "@/shared/api"

const tokens = api.defaults.Authorization?.replace('Bearer ', '') || null;

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
)
