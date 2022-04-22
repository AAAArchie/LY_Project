import {defineConfig} from 'vite'
// @ts-ignore
import commonjs from "rollup-plugin-commonjs";
// @ts-ignore
import externalGlobals from "rollup-plugin-external-globals";
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    server: {port: 7453},
    plugins: [vue()],
    build: {
        emptyOutDir: true,
        outDir: 'dist',
        rollupOptions: {
            plugins: [
                commonjs(),
                externalGlobals({})
            ]
        }
    },
})
