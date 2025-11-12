import { FC } from "react"
import { useStyles } from "./styles"

interface TransactionsContainerItemProps {
  img: string
  category: string
  organisation: string
  operatioType: boolean
  amount: string
}

export const TransactionsContainerItem: FC<TransactionsContainerItemProps> = ({
  img,
  category,
  organisation,
  operatioType,
  amount,
}) => {
  const classes = useStyles()
  return (
    <div className={classes.transactionContainerItem}>
      <img className={classes.img} src={img} alt="" />
      <div className={classes.transactionContainerItemDesc}>
        <p className={classes.category}> {category}</p>
        <div className={classes.organisation}> {organisation}</div>
        <div className={classes.opration}>
          <p className={classes.oprationType}>{operatioType ? "+" : "-"}</p>
          <p className={classes.oprationAmount}>{amount}</p>
        </div>
      </div>
    </div>
  )
}
