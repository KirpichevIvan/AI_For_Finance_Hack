import SendIcon from "@mui/icons-material/Send"
import { FC } from "react"
import { useStyles } from "./styles"

export const TextBar: FC = () => {
  const classes = useStyles()

  return (
    <div className={classes.textBar}>
      <form className={classes.messageInput} action="submit">
        <input
          placeholder="Введите сообщение"
          type="text"
          className={classes.messageTextInput}
        />
        <SendIcon className={classes.submitBtn} />
      </form>
      <img className={classes.avatar} src="/img/cactus.png" alt="" />
    </div>
  )
}
