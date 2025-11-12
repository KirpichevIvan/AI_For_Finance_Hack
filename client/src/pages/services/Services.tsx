import { Button, Grid, TextField, Typography } from "@mui/material"
import { FC } from "react"
import { useNavigate } from "react-router-dom"
import { Header } from "@/features/header"
import { useStyles } from "./styles"

export const Services: FC = () => {
  const classes = useStyles()

  const navigate = useNavigate()

  const onGoHome = () => navigate("/")

  return (
    <Grid p={4}>
      <Header text="Автокредит" />
      <Grid className={classes.group} container direction="column" gap={3}>
        <Grid item>
          <Typography className={classes.field}>Стоимость автомобиля</Typography>
          <TextField fullWidth />
        </Grid>
        <Grid item>
          <Typography className={classes.field}>Первоначальный взнос</Typography>
          <TextField fullWidth />
        </Grid>
        <Grid item>
          <Typography className={classes.field}>Срок</Typography>
          <TextField fullWidth />
        </Grid>
      </Grid>
      <Grid container direction="column" gap={2} mt={2}>
        <Grid item>
          <Typography className={classes.field}>Наименование</Typography>
          <TextField fullWidth variant="filled" />
        </Grid>
        <Grid item>
          <Typography className={classes.field}>ИНН</Typography>
          <TextField fullWidth variant="filled" />
        </Grid>
        <Grid item>
          <Typography className={classes.field}>Фактический адрес</Typography>
          <TextField fullWidth variant="filled" />
        </Grid>
        <Grid item>
          <Typography className={classes.field}>Среднемесячный доход</Typography>
          <TextField fullWidth variant="filled" />
        </Grid>
      </Grid>
      <Grid container gap={8} mt={8} justifyContent="center">
        <Button variant="contained" onClick={onGoHome}>
          Подтвердить
        </Button>
        <Button variant="contained" onClick={onGoHome}>
          Отклонить
        </Button>
      </Grid>
    </Grid>
  )
}
