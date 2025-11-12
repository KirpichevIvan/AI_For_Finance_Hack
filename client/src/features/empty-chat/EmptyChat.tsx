import { Grid, Typography } from "@mui/material"

export const EmptyChat = () => {
  return (
    <Grid
      height="100%"
      container
      direction="column"
      justifyContent="center"
      alignContent="center"
      maxWidth="900px"
      margin="0 auto"
    >
      <Typography variant="h2">
        Привет, меня зовут
        <Typography color="primary" display="inline" variant="h2">
          {" "}
          Kнопа!
        </Typography>
      </Typography>
      <Typography mt={2}>
        Рада знакомству с тобой! Ты можешь написать мне или записать голосовое сообщение.
        Чтобы перейти полностью на голосовое общение, воспользуйся переключателем вверху
      </Typography>
    </Grid>
  )
}
