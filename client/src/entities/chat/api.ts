import { ChatMessageParams } from "@/entities/chat/model.ts"
import { api } from "@/shared/api"

export const sendMessage = async ({
  message,
  code,
  type,
  // todo: заменить на пользователя
  userId = 1,
}: {
  message: string | Blob
  code: string
  type: "0" | "1"
  userId?: number
}): Promise<ChatMessageParams> => {
  try {
    const data = new FormData()
    data.append("user_id", String(userId))
    data.append("message", message)
    data.append("type", type)
    data.append("code", code)

    const res = await api.post<ChatMessageParams>("/api/messages/", data, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    return res.data
  } catch {
    return {
      message: "Ошибка",
      redir: false,
    }
  }
}
