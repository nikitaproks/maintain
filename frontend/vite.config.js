import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [sveltekit()],
    server: {
        watch: {
            usePolling: true,
        },
        host: true, // needed for the DC port mapping to work
        strictPort: true,
        port: 3000,
    },
    resolve: {
        alias: [
            {
                find: /^~(.*)$/,
                replacement: 'node_modules/$1',
            },
        ],
    },
});
