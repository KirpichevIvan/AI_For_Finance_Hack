import { FC } from "react"
import { useStyles } from "./styles"
import { TransactionsContainerItem } from "./TransactionContainer"

interface TransactionsListItemProps {
  day: string
  month: string
}

const data = [
  {
    img: "/img/transportpic.png",
    category: "Транспорт",
    organisation: "Автоперевозки",
    operatioType: false,
    amount: "25",
  },
  {
    img: "/img/basket.png",
    category: "Супермаркеты",
    organisation: "Семерочка",
    operatioType: false,
    amount: "2515",
  },
  {
    img: "/img/transportpic.png",
    category: "Транспорт",
    organisation: "Автоперевозки",
    operatioType: false,
    amount: "25",
  },
]

const render = data.map(operation => (
  <TransactionsContainerItem
    img={operation.img}
    category={operation.category}
    organisation={operation.organisation}
    operatioType={operation.operatioType}
    amount={operation.amount}
  />
))

export const TransactionsListItem: FC<TransactionsListItemProps> = ({ day, month }) => {
  const classes = useStyles()
  return (
    <div className={classes.transactionListItem}>
      <div className={classes.date}>
        <p className={classes.day}>{day}</p>
        <p className={classes.month}>{month}</p>
      </div>
      <div className={classes.transactionContainer}>
        {/* <TransactionsContainerItem
          img="/img/cactus.png"
          category="Транспорт"
          organisation="Автоперевозки"
          operatioType={false}
          amount="25"
        /> */}
        {render}
      </div>
    </div>
  )
}
