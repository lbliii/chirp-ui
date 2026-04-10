import { defineConfig } from "vitest/config";
import path from "path";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["tests/js/**/*.test.js"],
  },
  resolve: {
    alias: {
      "/static/islands": path.resolve(
        __dirname,
        "src/chirp_ui/templates/islands"
      ),
    },
  },
});
