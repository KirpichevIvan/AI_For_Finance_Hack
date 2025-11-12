export const getCodeWithValues = (value?: string | Record<string, string>): string => {
  return typeof value === "string" ? value : "000"
}

export const isCodeString = (
  values?: string | Record<string, string>
): values is string => {
  return typeof values === "string"
}
