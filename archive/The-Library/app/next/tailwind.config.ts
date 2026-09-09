import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        library: {
          bg: "#0d0803",
          surface: "#1a1209",
          border: "#2d1f0f",
          text: "#d4c4a8",
          muted: "#8b7355",
          accent: "#c4a882",
        },
        clementine: {
          flame: "#ff6b35",
          glow: "#ffcc80",
          warm: "#c4a882",
        },
        rex: {
          stone: "#7a8b6e",
          moss: "#8b9a7d",
          cool: "#9aaa8e",
        },
      },
      fontFamily: {
        serif: ["Georgia", "serif"],
      },
    },
  },
  plugins: [],
};

export default config;
