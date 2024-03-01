"use strict";
import { type Config } from prettier

export default const config: Config = {
  plugins: [
    "@prettier/plugin-xml",
    "prettier-plugin-jsdoc",
    "prettier-plugin-organize-imports",
  ],
  printWidth: 88,
  htmlWhitespaceSensitivity: "strict",
  jsdocDescriptionWithDot: true,
  jsdocPreferCodeFences: true,
};