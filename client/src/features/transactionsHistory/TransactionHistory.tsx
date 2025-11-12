import { FC } from "react"
import { Header } from "../header"
import { BackBtn } from "./BackBtn"
import { Filter } from "./Filter"
import { TransactionsList } from "./TransactionsList"

export const TransactionHistory: FC = () => {
  return (
    <>
      <Header text="Мои финансы" />
      <Filter />
      <TransactionsList />
      <BackBtn />
    </>
  )
}
