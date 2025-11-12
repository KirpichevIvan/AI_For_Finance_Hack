import { Theme } from "@mui/material"
import { makeStyles } from "@mui/styles"

export const useStyles = makeStyles((theme: Theme) => ({
  nav: {},
  navList: {
    width: "100%",
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    listStyle: "none",
    margin: "0px",
    padding: "6px 12px",
    color: theme.palette.primary.main,
    borderTop: "1px solid #EEEEEE",
  },
  navItem: {
    width: "100%",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    transition: "background-color 0.3s, color 0.3s",
  },
  navItemActive: {
    color: theme.palette.success.main,
  },
  navItemPic: {
    display: "block",
    margin: "0 auto",
  },
  navItemText: {
    textAlign: "center",
    margin: "0",
    fontSize: "13px",
  },
}))
