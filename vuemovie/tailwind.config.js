/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#E50914',
        secondary: '#141414',
        dark: '#0a0a0a',
        light: '#f5f5f5',
        gray: {
          100: '#f3f3f3',
          200: '#e5e5e5',
          300: '#cccccc',
          400: '#999999',
          500: '#666666',
          600: '#333333',
          700: '#222222',
          800: '#1a1a1a',
          900: '#141414',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
