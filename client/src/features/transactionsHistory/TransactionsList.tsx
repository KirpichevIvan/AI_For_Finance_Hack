import { FC } from "react"
import { useStyles } from "./styles"
import { TransactionsListItem } from "./TransactionListitem"

export const TransactionsList: FC = () => {
  const classes = useStyles()

  return (
    <div className={classes.transactionList}>
      <TransactionsListItem day="20" month="апреля" />
      <TransactionsListItem day="19" month="апреля" />
    </div>
  )
}
