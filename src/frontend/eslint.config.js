import js from "@eslint/js";
import babelParser from "@babel/eslint-parser";
import boundaries from "eslint-plugin-boundaries";
import importPlugin from "eslint-plugin-import";
import jsxA11y from "eslint-plugin-jsx-a11y";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";

export default [
  { ignores: ["dist"] },
  {
    ...js.configs.recommended,
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parser: babelParser,
      parserOptions: {
        babelOptions: {
          presets: ["@babel/preset-react", "@babel/preset-typescript"],
        },
        requireConfigFile: false,
      },
    },
    plugins: {
      boundaries,
      import: importPlugin,
      "jsx-a11y": jsxA11y,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...jsxA11y.flatConfigs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
      "boundaries/element-types": [
        "error",
        {
          default: "disallow",
          rules: [
            {
              from: "app",
              allow: ["pages", "widgets", "features", "entities", "shared"],
            },
            {
              from: "pages",
              allow: ["widgets", "features", "entities", "shared"],
            },
            { from: "widgets", allow: ["features", "entities", "shared"] },
            { from: "features", allow: ["entities", "shared"] },
            { from: "entities", allow: ["shared"] },
            { from: "shared", allow: ["shared"] },
          ],
        },
      ],
      "import/no-cycle": "error",
      "import/no-duplicates": "error",
      "import/no-self-import": "error",
      "react-refresh/only-export-components": [
        "warn",
        { allowConstantExport: true },
      ],
    },
  },
  {
    settings: {
      "boundaries/elements": [
        { type: "app", pattern: "app", mode: "folder" },
        { type: "pages", pattern: "pages/*", mode: "folder" },
        { type: "widgets", pattern: "widgets/*", mode: "folder" },
        { type: "features", pattern: "features/*", mode: "folder" },
        { type: "entities", pattern: "entities/*", mode: "folder" },
        { type: "shared", pattern: "shared", mode: "folder" },
      ],
    },
  },
];
