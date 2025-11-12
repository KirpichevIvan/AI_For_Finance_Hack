export interface SpritesMap {
  common: "bank_avatar" | "mike" | "react" | "send-mail"
}
export const SPRITES_META: {
  [Key in keyof SpritesMap]: {
    filePath: string
    items: Record<
      SpritesMap[Key],
      {
        viewBox: string
        width: number
        height: number
      }
    >
  }
} = {
  common: {
    filePath: "common.svg",
    items: {
      bank_avatar: {
        viewBox: "0 0 43 43",
        width: 43,
        height: 43,
      },
      mike: {
        viewBox: "0 0 26 26",
        width: 26,
        height: 26,
      },
      react: {
        viewBox: "0 0 256 228",
        width: 35.93,
        height: 32,
      },
      "send-mail": {
        viewBox: "0 0 27 27",
        width: 27,
        height: 27,
      },
    },
  },
}
