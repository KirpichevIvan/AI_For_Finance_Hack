import { Theme } from "@mui/material"
import { makeStyles } from "@mui/styles"

export const useStyles = makeStyles((theme: Theme) => ({
  chat: {
    height: "calc(100vh - 100px)",
    padding: "12px 0px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "flex-end",
  },
  messagesField: {
    overflowY: "scroll",
    height: "100%",
  },
  usersMessage: {
    marginLeft: "auto",
    paddingLeft: "43%",
  },

  usersMessageText: {
    color: "white",
    padding: "10px",
    borderRadius: "20px",
    marginBottom: "4px",
    textAlign: "justify",
    backgroundColor: theme.palette.success.main,
  },

  usersMessageTime: {
    display: "block",
    paddingLeft: "12px",
    fontSize: "10px",
  },

  botsMessage: {
    position: "relative",
    width: "fit-content",
    marginLeft: "0px",
    marginRight: "35%",
  },
  botsMessageText: {
    width: "fit-content",
    color: "black",
    padding: "10px",
    marginLeft: "50px",
    borderRadius: "20px",
    marginBottom: "4px",
    textAlign: "justify",
    backgroundColor: "#F5F5F5",
  },
  botsMessageTime: {
    display: "block",
    marginLeft: "55px",
    fontSize: "10px",
  },
  botAvatar: {
    position: "absolute",
    transform: "translateY(-55px)",
  },
  textBar: {
    display: "flex",
    flexDirection: "row",
    gap: "10px",
    alignItems: "flex-end",
    position: "relative",
  },
  messageInput: {
    flexGrow: "1",
    position: "relative",
    marginRight: "70px",
    // display: "flex",
    // flexDirection: "row",
    // gap: "10px",
    // alignItems: "flex-end",
  },
  messageTextInput: {
    width: "100%",
    backgroundColor: "#F5F5F5",
    borderStyle: "none",
    height: "32px",
    borderRadius: "20px",
    paddingLeft: "15px",
  },
  submitBtn: {
    position: "absolute",
    width: "26px",
    right: "0px",
    top: "50%",
    transform: "translateY(-50%)",
  },
  avatar: {
    position: "absolute",
    width: "60px",
    height: "90px",
    objectFit: "cover",
    right: "0",
    transform: "translateY(10px)",
  },
}))
