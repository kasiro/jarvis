// vite.config.ts
import { defineConfig } from "file:///home/kasiro/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/jarvis/frontend/node_modules/.pnpm/vite@5.4.21_@types+node@25.3.0_sass@1.97.3/node_modules/vite/dist/node/index.js";
import { svelte } from "file:///home/kasiro/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/jarvis/frontend/node_modules/.pnpm/@sveltejs+vite-plugin-svelte@3.1.2_svelte@4.2.20_vite@5.4.21_@types+node@25.3.0_sass@1.97.3_/node_modules/@sveltejs/vite-plugin-svelte/src/index.js";
import sveltePreprocess from "file:///home/kasiro/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/jarvis/frontend/node_modules/.pnpm/svelte-preprocess@5.1.4_postcss@8.5.6_sass@1.97.3_svelte@4.2.20_typescript@5.9.3/node_modules/svelte-preprocess/dist/index.js";
import tsconfigPaths from "file:///home/kasiro/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/jarvis/frontend/node_modules/.pnpm/vite-tsconfig-paths@4.3.2_typescript@5.9.3_vite@5.4.21_@types+node@25.3.0_sass@1.97.3_/node_modules/vite-tsconfig-paths/dist/index.mjs";
import routify from "file:///home/kasiro/%D0%94%D0%BE%D0%BA%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D1%8B/jarvis/frontend/node_modules/.pnpm/@roxi+routify@3.6.4_@sveltejs+vite-plugin-svelte@3.1.2_svelte@4.2.20_vite@5.4.21_@types_3f5af8eff005cc02cbf3456fa3fdb115/node_modules/@roxi/routify/lib/extra/vite-plugin/vite-plugin.js";
var vite_config_default = defineConfig({
  plugins: [
    svelte({
      preprocess: [
        sveltePreprocess({
          typescript: true
        })
      ],
      onwarn: (warning, handler) => {
        const { code, frame } = warning;
        if (code === "css-unused-selector")
          return;
        handler(warning);
      }
    }),
    routify(),
    tsconfigPaths()
  ],
  clearScreen: false,
  server: {
    port: 1420,
    strictPort: true
  },
  envPrefix: ["VITE_", "TAURI_"],
  build: {
    target: process.env.TAURI_PLATFORM == "windows" ? "chrome105" : "safari13",
    minify: !process.env.TAURI_DEBUG ? "esbuild" : false,
    sourcemap: !!process.env.TAURI_DEBUG
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvaG9tZS9rYXNpcm8vXHUwNDE0XHUwNDNFXHUwNDNBXHUwNDQzXHUwNDNDXHUwNDM1XHUwNDNEXHUwNDQyXHUwNDRCL2phcnZpcy9mcm9udGVuZFwiO2NvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9maWxlbmFtZSA9IFwiL2hvbWUva2FzaXJvL1x1MDQxNFx1MDQzRVx1MDQzQVx1MDQ0M1x1MDQzQ1x1MDQzNVx1MDQzRFx1MDQ0Mlx1MDQ0Qi9qYXJ2aXMvZnJvbnRlbmQvdml0ZS5jb25maWcudHNcIjtjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfaW1wb3J0X21ldGFfdXJsID0gXCJmaWxlOi8vL2hvbWUva2FzaXJvLyVEMCU5NCVEMCVCRSVEMCVCQSVEMSU4MyVEMCVCQyVEMCVCNSVEMCVCRCVEMSU4MiVEMSU4Qi9qYXJ2aXMvZnJvbnRlbmQvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tIFwidml0ZVwiO1xuaW1wb3J0IHsgc3ZlbHRlIH0gZnJvbSBcIkBzdmVsdGVqcy92aXRlLXBsdWdpbi1zdmVsdGVcIjtcbmltcG9ydCBzdmVsdGVQcmVwcm9jZXNzIGZyb20gXCJzdmVsdGUtcHJlcHJvY2Vzc1wiO1xuaW1wb3J0IHRzY29uZmlnUGF0aHMgZnJvbSAndml0ZS10c2NvbmZpZy1wYXRocydcbmltcG9ydCByb3V0aWZ5IGZyb20gJ0Byb3hpL3JvdXRpZnkvdml0ZS1wbHVnaW4nXG5cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG4gIHBsdWdpbnM6IFtcbiAgICBzdmVsdGUoe1xuICAgICAgcHJlcHJvY2VzczogW1xuICAgICAgICBzdmVsdGVQcmVwcm9jZXNzKHtcbiAgICAgICAgICB0eXBlc2NyaXB0OiB0cnVlLFxuICAgICAgICB9KSxcbiAgICAgIF0sXG4gICAgICBvbndhcm46ICh3YXJuaW5nLCBoYW5kbGVyKSA9PiB7XG4gICAgICAgIGNvbnN0IHsgY29kZSwgZnJhbWUgfSA9IHdhcm5pbmc7XG4gICAgICAgIGlmIChjb2RlID09PSBcImNzcy11bnVzZWQtc2VsZWN0b3JcIilcbiAgICAgICAgICAgIHJldHVybjtcblxuICAgICAgICBoYW5kbGVyKHdhcm5pbmcpO1xuICAgICAgfSxcbiAgICB9KSxcbiAgICByb3V0aWZ5KCksXG4gICAgdHNjb25maWdQYXRocygpXG4gIF0sXG5cbiAgY2xlYXJTY3JlZW46IGZhbHNlLFxuICBzZXJ2ZXI6IHtcbiAgICBwb3J0OiAxNDIwLFxuICAgIHN0cmljdFBvcnQ6IHRydWUsXG4gIH0sXG4gIGVudlByZWZpeDogW1wiVklURV9cIiwgXCJUQVVSSV9cIl0sXG4gIGJ1aWxkOiB7XG4gICAgdGFyZ2V0OiBwcm9jZXNzLmVudi5UQVVSSV9QTEFURk9STSA9PSBcIndpbmRvd3NcIiA/IFwiY2hyb21lMTA1XCIgOiBcInNhZmFyaTEzXCIsXG4gICAgbWluaWZ5OiAhcHJvY2Vzcy5lbnYuVEFVUklfREVCVUcgPyBcImVzYnVpbGRcIiA6IGZhbHNlLFxuICAgIHNvdXJjZW1hcDogISFwcm9jZXNzLmVudi5UQVVSSV9ERUJVRyxcbiAgfSxcbn0pOyJdLAogICJtYXBwaW5ncyI6ICI7QUFBaVYsU0FBUyxvQkFBb0I7QUFDOVcsU0FBUyxjQUFjO0FBQ3ZCLE9BQU8sc0JBQXNCO0FBQzdCLE9BQU8sbUJBQW1CO0FBQzFCLE9BQU8sYUFBYTtBQUVwQixJQUFPLHNCQUFRLGFBQWE7QUFBQSxFQUMxQixTQUFTO0FBQUEsSUFDUCxPQUFPO0FBQUEsTUFDTCxZQUFZO0FBQUEsUUFDVixpQkFBaUI7QUFBQSxVQUNmLFlBQVk7QUFBQSxRQUNkLENBQUM7QUFBQSxNQUNIO0FBQUEsTUFDQSxRQUFRLENBQUMsU0FBUyxZQUFZO0FBQzVCLGNBQU0sRUFBRSxNQUFNLE1BQU0sSUFBSTtBQUN4QixZQUFJLFNBQVM7QUFDVDtBQUVKLGdCQUFRLE9BQU87QUFBQSxNQUNqQjtBQUFBLElBQ0YsQ0FBQztBQUFBLElBQ0QsUUFBUTtBQUFBLElBQ1IsY0FBYztBQUFBLEVBQ2hCO0FBQUEsRUFFQSxhQUFhO0FBQUEsRUFDYixRQUFRO0FBQUEsSUFDTixNQUFNO0FBQUEsSUFDTixZQUFZO0FBQUEsRUFDZDtBQUFBLEVBQ0EsV0FBVyxDQUFDLFNBQVMsUUFBUTtBQUFBLEVBQzdCLE9BQU87QUFBQSxJQUNMLFFBQVEsUUFBUSxJQUFJLGtCQUFrQixZQUFZLGNBQWM7QUFBQSxJQUNoRSxRQUFRLENBQUMsUUFBUSxJQUFJLGNBQWMsWUFBWTtBQUFBLElBQy9DLFdBQVcsQ0FBQyxDQUFDLFFBQVEsSUFBSTtBQUFBLEVBQzNCO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K
