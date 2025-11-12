import { Button, Grid } from "@mui/material"
import { FC } from "react"
import { sendMessage } from "@/entities/chat"
import { useChatContext } from "@/features/chat"
import { getCodeWithValues, isCodeString } from "@/shared/lib/guards.ts"
import { useStyles } from "./styles"

interface BotsMessageProps {
  text: string
  time: string
  targetedActions?: Record<string, string>
}

export const BotsMessage: FC<BotsMessageProps> = ({
  text,
  time,
  targetedActions = {},
}) => {
  const classes = useStyles()
  const actions = Object.entries(targetedActions)

  const { setChatMessages, isVoice, setCode } = useChatContext()

  const onClick = async (code: string) => {
    const res = await sendMessage({ code, type: isVoice ? "1" : "0", message: "" })

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

    setCode(getCodeWithValues(res.values))
  }

  return (
    <div className={classes.botsMessage}>
      <p className={classes.botsMessageText}>{text}</p>
      <span className={classes.botsMessageTime}>{time}</span>
      <img className={classes.botAvatar} src="/img/bankAvatar.png" alt="" />
      <Grid container gap={2} marginTop={2}>
        {actions.map(([code, title]) => (
          <Grid item key={code}>
            <Button variant="contained" size="small" onClick={() => onClick(code)}>
              {title}
            </Button>
          </Grid>
        ))}
      </Grid>
    </div>
  )
}
