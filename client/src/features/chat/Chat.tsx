import SendIcon from "@mui/icons-material/Send"
import { ChangeEvent, FC, useEffect, useState } from "react"
import { ChatResponse, sendMessage } from "@/entities/chat"
import { useChatContext } from "@/features/chat/Context.tsx"
import { api } from "@/shared/api"
import { isCodeString } from "@/shared/lib/guards.ts"
import { MessageField } from "./MessageField"
import { useStyles } from "./styles"
import { VoiceToggle } from "./voiceToggle"

export const Chat: FC = () => {
  const classes = useStyles()
  const { isVoice, setChatMessages, chatMessages, code, setCode } = useChatContext()

  const [message, setMessage] = useState("")

  const onChange = ({ target }: ChangeEvent<HTMLInputElement>) => setMessage(target.value)

  const onSubmit = async () => {
    setMessage("")

    setChatMessages(prevState => [
      ...prevState,
      {
        message,
        code,
        type: "",
        time: new Date().toString(),
        id: 1,
        sender: false,
        theme_id: 0,
      },
    ])

    const data = new FormData()
    data.append("user_id", String(1))
    data.append("message", message)
    data.append("type", isVoice ? "1" : "0")
    data.append("code", code)

    const res = await sendMessage({ code, type: isVoice ? "1" : "0", message })

    setChatMessages(prevState => [
      ...prevState,
      {
        message: res.message,
        code,
        type: "",
        time: new Date().toString(),
        id: 1,
        sender: true,
        theme_id: 0,
        targetedActions: !isCodeString(res.values) ? res.values : undefined,
      },
    ])
    if (!isCodeString(res.values)) return
    setCode(res.values)
  }

  useEffect(() => {
    api
      .get<ChatResponse>("/api/messages")
      .then(res => setChatMessages(res.data.data))
      .catch(() => setChatMessages([]))
  }, [])

  return (
    <div className={classes.chat}>
      <VoiceToggle />
      <MessageField messages={chatMessages} />
      <div className={classes.textBar}>
        <form className={classes.messageInput}>
          <input
            placeholder="Введите сообщение"
            type="text"
            className={classes.messageTextInput}
            onChange={onChange}
            value={message}
          />
          <SendIcon className={classes.submitBtn} onClick={onSubmit} />
        </form>
        <img className={classes.avatar} src="/img/cactus.png" alt="" />
      </div>
    </div>
  )
}
