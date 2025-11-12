module.exports = {
  // Type check TypeScript files
  "**/*.(ts|tsx)": () => "npx tsc --noEmit",

  "*.{js,ts,tsx,jsx}": [
    "prettier --write",
    "eslint --fix"
  ]
}
