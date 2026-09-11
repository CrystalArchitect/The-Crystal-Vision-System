/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ink: {
          50: '#f9f7f4',
          100: '#f3efe8',
          200: '#e7dfd3',
          300: '#dccfbe',
          400: '#b5a799',
          500: '#8e7f74',
          600: '#6b5d52',
          700: '#483d35',
          800: '#2a1e18',
          900: '#0d0a08',
        },
        accent: {
          50: '#fff3e0',
          100: '#ffe0b2',
          200: '#ffd99e',
          300: '#ffb74d',
          400: '#ffa726',
          500: '#fb8c00',
          600: '#f57c00',
          700: '#e65100',
          800: '#bf360c',
          900: '#ff6f00',
        },
      },
      fontFamily: {
        sans: ['system-ui', 'sans-serif'],
        mono: ['Menlo', 'Monaco', 'Courier New', 'monospace'],
      },
    },
  },
  plugins: [],
};
