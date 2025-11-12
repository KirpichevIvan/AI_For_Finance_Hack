export interface ChatMessageParams {
  message: string
  redir: boolean | string
  values?: string | Record<string, string>
}

export interface ChatData {
  code: string
  id: number
  message: string
  sender: boolean
  theme_id: number
  time: string
  type: string
  targetedActions?: Record<string, string>
}

export interface ChatResponse {
  data: ChatData[]
  message: string
  status: boolean
}
