import { RouterProvider } from "react-router-dom"
import { ThemeProvider } from "@/app/providers"
import { router } from "@/app/router"
import { ChatContextProvider } from "@/features/chat"

export const App = () => {
  return (
    <ThemeProvider>
      <ChatContextProvider>
        <RouterProvider router={router} />
      </ChatContextProvider>
    </ThemeProvider>
  )
}
