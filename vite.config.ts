import preact from "@preact/preset-vite";
import * as vite from "vite";
import * as cdn from "./lib/build/cdn";
import * as sass from "./lib/build/sass";

export default vite.defineConfig(({ mode }) => {
  let defaults: vite.UserConfig = {
    logLevel: mode === "prod" ? "silent" : "info",
    appType: "mpa",
    plugins: [preact()],
    css: {
      devSourcemap: mode === "dev",
      preprocessorOptions: {
        scss: sass.options,
      },
    },
    json: {
      stringify: true,
    },
    server: {
      open: true,
    },
    esbuild: {
      legalComments: "none",
    },
    build: {
      outDir: "dist/client",
      target: "modules",
      assetsInlineLimit: 0,
      copyPublicDir: true,
      cssMinify: true,
      minify: mode === "prod" ? "terser" : "esbuild",
      assetsDir: "",
      terserOptions: {
        format: { comments: false },
      },
      rollupOptions: {
        input: ["./index.html"],
        preserveEntrySignatures: "allow-extension",
        output: {
          preserveModules: false,
        },
      },
      manifest: "manifest.json",
    },
  };

  let productionDefaults: vite.UserConfig = {
    resolve: {
      alias: cdn.aliases,
    },
  };

  if (mode === "prod") return Object.assign(defaults, productionDefaults);

  return defaults;
});
