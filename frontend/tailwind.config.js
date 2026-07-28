/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        paper: '#FAFAF7',
        ink: '#14151A',
        surface: '#FFFFFF',
        muted: '#6B6F76',
        border: '#E7E5DF',
        accent: {
          DEFAULT: '#3D5AFE',
          hover: '#2F46D6',
          soft: '#EEF0FF',
        },
        success: {
          DEFAULT: '#00B37E',
          soft: '#E3FBF3',
        },
        danger: {
          DEFAULT: '#DC3545',
          soft: '#FDECEE',
        },
      },
      fontFamily: {
        display: ['Fraunces', 'ui-serif', 'Georgia', 'serif'],
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        mono: ['IBM Plex Mono', 'ui-monospace', 'SFMono-Regular', 'monospace'],
      },
      borderRadius: {
        card: '14px',
      },
      boxShadow: {
        card: '0 1px 2px rgba(20,21,26,0.04), 0 1px 12px rgba(20,21,26,0.04)',
        popover: '0 8px 30px rgba(20,21,26,0.12)',
      },
    },
  },
  plugins: [],
}