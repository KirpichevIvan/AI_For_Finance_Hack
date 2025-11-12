import { FC } from "react"
import { useStyles } from "./styles"

export const BackBtn: FC = () => {
  const classes = useStyles()
  return (
    <button type="submit" className={classes.backBtn}>
      Назад
    </button>
  )
}
