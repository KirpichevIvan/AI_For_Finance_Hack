import { Theme } from "@mui/material"
import { makeStyles } from "@mui/styles"

export const useStyles = makeStyles((theme: Theme) => ({
  group: {
    border: `1px solid ${theme.palette.primary.main} `,
    borderRadius: 10,
    padding: theme.spacing(1, 2),
  },
  field: {
    color: "#9E9E9E",
    background: theme.palette.background.paper,
  },
}))
