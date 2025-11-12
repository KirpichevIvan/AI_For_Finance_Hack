import eslintPlugin from "@nabla/vite-plugin-eslint"
import svgPlugin from "@neodx/svg/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"
import checkerPlugin from "vite-plugin-checker"
import svgr from "vite-plugin-svgr"
import tsconfigPaths from "vite-tsconfig-paths"

// https://vitejs.dev/config/
export default defineConfig(({ isPreview }) => ({
  plugins: [
    react(),
    eslintPlugin(),
    tsconfigPaths(),
    svgr(),
    svgPlugin({
      root: "assets",
      output: "public/sprites",
      group: true,
      fileName: !isPreview ? undefined : "{name}.{hash:8}.svg", // add to prod
      resetColors: {
        replaceUnknown: "currentColor",
      },
      metadata: {
        path: "src/shared/ui/icon/sprite.gen.ts",
        // generate metadata
        runtime: {
          size: true,
          viewBox: true,
        },
      },
    }),
    checkerPlugin({
      typescript: true,
      eslint: {
        lintCommand: "eslint .",
      },
    }),
  ],
}))
