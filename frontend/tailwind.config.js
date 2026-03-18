/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#eefbf4',
          100: '#d8f3e3',
          600: '#1d9a62',
          700: '#15744a',
        },
        danger: '#c62f2f',
        slatebg: '#f5f7fa',
      },
      boxShadow: {
        soft: '0 10px 30px rgba(0, 0, 0, 0.08)',
      },
    },
  },
  plugins: [],
}
