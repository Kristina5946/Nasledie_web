/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/*.py',
    './static/js/**/*.js',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      screens: {
        xs: '480px',
      },
      colors: {
        primary: '#8b5cf6',
        secondary: '#3b82f6',
        accent: '#d946ef',
        lightbg: '#f8fafc',
        darkbg: '#090514',
        cardbg: {
          DEFAULT: '#ffffff',
          dark: '#120b29',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
