import { FC } from "react"
import { Chat, useChatContext } from "@/features/chat"
import { Header } from "@/features/header"
import { Navigation } from "@/features/navigation"
import { VoiceRecording } from "@/features/voice-recording"

export const MainPage: FC = () => {
  const { isVoice } = useChatContext()
  return (
    <>
      <Header text="Чат с банком" />
      {isVoice && <VoiceRecording />}
      {!isVoice && (
        <>
          <Chat />
          <Navigation />
        </>
      )}
    </>
  )
}
