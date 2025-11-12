import CancelOutlinedIcon from "@mui/icons-material/CancelOutlined"
import { Button, Typography } from "@mui/material"
import { useCallback, useEffect, useRef } from "react"
import { sendMessage } from "@/entities/chat"
import { useChatContext } from "@/features/chat"
import { useStyles } from "./styles.ts"

export const VoiceRecording = () => {
  const { toggleVoice, code } = useChatContext()
  const classes = useStyles()

  const voice = useRef<Blob[]>([])
  const mediaRecorder = useRef<MediaRecorder | null>(null)

  const onStartVoice = useCallback((event: BlobEvent) => {
    voice.current.push(event.data)
  }, [])

  const onStop = () => {
    mediaRecorder.current?.stop()
    mediaRecorder.current?.removeEventListener("dataavailable", onStartVoice)
  }

  useEffect(() => {
    navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
      mediaRecorder.current = new MediaRecorder(stream)

      mediaRecorder.current.addEventListener("dataavailable", onStartVoice)
      mediaRecorder.current.start()
      mediaRecorder.current.addEventListener("stop", () => {
        const voiceBlob = new Blob(voice.current, {
          type: "audio/wav",
        })

        const file = new File([voiceBlob], "voice.wav", { type: "audio/wav;codecs=0" })

        sendMessage({
          type: "1",
          message: file,
          code,
        })
        onStop()
      })
    })

    return () => {
      mediaRecorder.current?.removeEventListener("dataavailable", onStartVoice)
      onStop()
    }
  }, [])

  return (
    <div className={classes.container}>
      <CancelOutlinedIcon
        onClick={toggleVoice}
        color="primary"
        className={classes.icon}
      />
      <Typography variant="h2" mt={8}>
        Поговори со мной
      </Typography>
      <Button onClick={onStop} data-message="Завершить голосовой ввод">
        <img src="/img/cactus.png" alt="Изображение кактуса" className={classes.img} />
      </Button>
    </div>
  )
}
