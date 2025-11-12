export const formatDate = (date: string) => {
  const instance = new Date(date)

  return instance.toLocaleString()
}
