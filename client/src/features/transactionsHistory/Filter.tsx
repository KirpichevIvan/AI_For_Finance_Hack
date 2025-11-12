import { FC } from "react"
import { useStyles } from "./styles"

export const Filter: FC = () => {
  const classes = useStyles()
  return (
    <div className={classes.filter}>
      <p className={classes.filterText}>История операций</p>
      <select className={classes.select} name="period" id="">
        <option value="wholePeriod">Все время</option>
        <option value="week">Неделя</option>
        <option value="month">Месяц</option>
        <option value="year">Год</option>
      </select>
      <select className={classes.select} name="type" id="">
        <option value="all">Все операции</option>
        <option value="increase">Зачисления</option>
        <option value="descrease">Списания</option>
      </select>
      {/* <img src="/img/preferences.svg" alt="" /> */}
    </div>
  )
}
