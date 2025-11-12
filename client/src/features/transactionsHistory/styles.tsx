import { Theme } from "@mui/material"
import { makeStyles } from "@mui/styles"

export const useStyles = makeStyles((theme: Theme) => ({
  filter: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    borderBottom: "1px solid grey",
  },
  filterText: {
    fontSize: "14px",
  },
  select: {
    height: "30px",
    borderColor: "green",
    borderRadius: "10px",
    fontSize: "12px",
  },
  transactionList: {
    overflowY: "scroll",
    height: "80vh",
  },
  transactionListItem: {
    position: "relative",
  },
  date: {
    display: "flex",
    flexDirection: "row",
    height: "30px",
    alignItems: "center",
    color: "grey",
  },
  day: { padding: "0", margin: "0" },
  month: { padding: "0 0 0 10px", margin: "0" },
  transactionContainer: {
    height: "100%",
  },
  transactionContainerItem: {
    display: "flex",
    flexDirection: "row",
    marginBottom: "12px",
    height: "50px",
    padding: "12px 12px 0px",
    alignItems: "center",
    // border: "1px solid red",
  },
  img: {
    // border: "1px solid red",
    height: "50px",
  },
  transactionContainerItemDesc: {
    position: "relative",
    marginLeft: "12px",
    width: "100%",
    height: "100%",
    borderBottom: "1px solid #E0E0E0",
  },
  category: {
    margin: "0px",
    position: "absolute",
    top: "0",
    left: "0px",
    color: "grey",
    fontWeight: "400",
    fontSize: "12px",
  },
  organisation: {
    position: "absolute",
    margin: "0px",
    bottom: "0",
    left: "0px",
    fontSize: "12px",
  },
  opration: {
    display: "flex",
    position: "absolute",
    margin: "0px",
    top: "0",
    right: "0",
    fontSize: "12px",
  },
  oprationType: {
    margin: "0px",
  },
  oprationAmount: {
    margin: "0px",
  },
  backBtn: {
    marginLeft: "50%",
    transform: "translateX(-50%)",
    backgroundColor: theme.palette.primary.main,
    color: "white",
    fontSize: "16px",
    padding: "5px 43px",
    borderRadius: "20px",
  },
}))
