// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  $development: {
    devtools: { enabled: true },
    routeRules: {
      "/api/**": {
        proxy: "http://127.0.0.1:8000/**",
      },
      "/docs": {
        proxy: "http://127.0.0.1:8000/docs",
      },
      "/redoc": {
        proxy: "http://127.0.0.1:8000/redoc",
      },
      "/openapi.json": {
        proxy: "http://127.0.0.1:8000/openapi.json",
      },
    },
  },

  $production: {
    // Production config
  },
  srcDir: "app/",
});
