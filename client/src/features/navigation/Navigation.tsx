import AccountBalanceWalletOutlinedIcon from "@mui/icons-material/AccountBalanceWalletOutlined"
import ChatOutlinedIcon from "@mui/icons-material/ChatOutlined"
import CurrencyRubleOutlinedIcon from "@mui/icons-material/CurrencyRubleOutlined"
import HomeOutlinedIcon from "@mui/icons-material/HomeOutlined"
import MoreHorizOutlinedIcon from "@mui/icons-material/MoreHorizOutlined"
import { clsx } from "clsx"
import { FC } from "react"
import { useStyles } from "./styles"

export const Navigation: FC = () => {
  const classes = useStyles()

  return (
    <nav>
      <ul className={classes.navList}>
        <li className={clsx(classes.navItem)}>
          <HomeOutlinedIcon className={classes.navItemPic} />
          <p className={classes.navItemText}>Главная</p>
        </li>
        <li className={clsx(classes.navItem)}>
          <AccountBalanceWalletOutlinedIcon className={classes.navItemPic} />
          <p className={classes.navItemText}>Мои финансы</p>
        </li>
        <li className={clsx(classes.navItem, classes.navItemActive)}>
          <ChatOutlinedIcon className={classes.navItemPic} />
          <p className={classes.navItemText}>Чат с банком</p>
        </li>
        <li className={clsx(classes.navItem)}>
          <CurrencyRubleOutlinedIcon className={classes.navItemPic} />
          <p className={classes.navItemText}>Платежи</p>
        </li>
        <li className={clsx(classes.navItem)}>
          <MoreHorizOutlinedIcon className={classes.navItemPic} />
          <p className={classes.navItemText}>Ещё</p>
        </li>
      </ul>
    </nav>
  )
}
