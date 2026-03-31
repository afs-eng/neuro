import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#f3f0e4',
        foreground: '#1a1a1a',
        card: {
          DEFAULT: '#f6f4ed',
          foreground: '#1a1a1a',
        },
        primary: {
          DEFAULT: '#1a1a1a',
          foreground: '#ffffff',
        },
        secondary: {
          DEFAULT: '#e8e4d6',
          foreground: '#1a1a1a',
        },
        muted: {
          DEFAULT: '#d6d0c8',
          foreground: '#525252',
        },
        accent: {
          DEFAULT: '#cbb79d',
          foreground: '#1a1a1a',
        },
        destructive: {
          DEFAULT: '#ef4444',
          foreground: '#ffffff',
        },
        border: '#d4d0c8',
        input: '#e8e4d6',
        ring: '#1a1a1a',
      },
      borderRadius: {
        '2xl': '28px',
        '3xl': '36px',
      },
    },
  },
  plugins: [],
}
export default config