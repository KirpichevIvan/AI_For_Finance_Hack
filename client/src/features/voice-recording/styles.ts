import { makeStyles } from "@mui/styles"

export const useStyles = makeStyles(() => ({
  container: {
    position: "relative",
    display: "flex",
    flexDirection: "column",
    width: "100%",
    height: "100%",
    alignItems: "center",
    justifyContent: "center",
  },
  icon: {
    position: "absolute",
    top: 20,
    right: 20,
  },
  img: {
    position: "absolute",
    bottom: 0,
    transform: "translateY(100%)",
  },
}))
