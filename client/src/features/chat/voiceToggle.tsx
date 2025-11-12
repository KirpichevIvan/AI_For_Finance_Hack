import { FormControlLabel, Switch } from "@mui/material"
import { FC } from "react"
import { useChatContext } from "@/features/chat"

export const VoiceToggle: FC = () => {
  const { isVoice, toggleVoice } = useChatContext()

  return (
    <FormControlLabel
      value="start"
      control={<Switch color="primary" checked={isVoice} onChange={toggleVoice} />}
      label="Голос"
      labelPlacement="start"
    />
  )
}
