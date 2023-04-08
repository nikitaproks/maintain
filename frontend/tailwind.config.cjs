/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    theme: {
        extend: {},
    },
    daisyui: {
        themes: [
            "light",
            "dark",
            {
                mytheme: {
                    "primary": "#FFDF22",

                    "secondary": "#2B4047",

                    "accent": "#F56565",

                    "neutral": "#A1B1B5",

                    "base-100": "#E2E8F0",

                    "info": "#5EC5D9",

                    "success": "#28E27E",

                    "warning": "#F38816",

                    "error": "#F74A2B",
                },
            }
        ]
    },
    plugins: [require("daisyui")],
}
