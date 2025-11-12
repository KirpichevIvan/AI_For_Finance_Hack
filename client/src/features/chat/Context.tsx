/* eslint-disable react/jsx-no-constructed-context-values */

import {
  createContext,
  Dispatch,
  ReactNode,
  SetStateAction,
  useContext,
  useState,
} from "react"
import { ChatData } from "@/entities/chat"

interface ContextParams {
  isVoice: boolean
  toggleVoice: () => void
  chatMessages: ChatData[]
  setChatMessages: Dispatch<SetStateAction<ChatData[]>>
  code: string
  setCode: Dispatch<SetStateAction<string>>
}

const ChatContext = createContext<ContextParams | null>(null)

interface Props {
  children: ReactNode
}

export const ChatContextProvider = ({ children }: Props) => {
  const [isVoice, setIsVoice] = useState(false)
  const [chatMessages, setChatMessages] = useState<ChatData[]>([])
  const [code, setCode] = useState("000")

  const toggleVoice = () => setIsVoice(prevState => !prevState)

  const value = {
    isVoice,
    toggleVoice,
    chatMessages,
    setChatMessages,
    code,
    setCode,
  }

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>
}

// eslint-disable-next-line react-refresh/only-export-components
export const useChatContext = () => {
  const state = useContext(ChatContext)

  if (!state) throw new Error("provider not found")
  return state
}
