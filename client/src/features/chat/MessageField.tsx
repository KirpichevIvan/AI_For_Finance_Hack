import { FC } from "react"
import { ChatData } from "@/entities/chat"
import { EmptyChat } from "@/features/empty-chat"
import { BotsMessage } from "./botsMessage"
import { useStyles } from "./styles"
import { UsersMessage } from "./UsersMessage"

interface Props {
  messages: ChatData[]
}

export const MessageField: FC<Props> = ({ messages = [] }) => {
  const classes = useStyles()

  if (!messages.length) return <EmptyChat />
  return (
    <div className={classes.messagesField}>
      {messages.map(message =>
        !message.sender ? (
          <UsersMessage key={message.id} text={message.message} time={message.time} />
        ) : (
          <BotsMessage
            key={message.id}
            text={message.message}
            time={message.time}
            targetedActions={message.targetedActions}
          />
        )
      )}
    </div>
  )
}
