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
        darkbg: '#1a1736',
        'darkbg-elevated': '#242047',
        cardbg: {
          DEFAULT: '#ffffff',
          dark: '#2e2854',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
      },
    },
  },
  plugins: [],
};
