import { Theme } from "@mui/material"
import { makeStyles } from "@mui/styles"

export const useStyles = makeStyles((theme: Theme) => ({
  header: {
    color: theme.palette.primary.main,
    padding: "15px",
    fontSize: "16px",
    fontWeight: "400",
    borderBottom: "2px solid #EEEEEE",
  },
}))
