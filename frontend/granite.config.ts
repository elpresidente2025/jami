import { appsInToss } from "@apps-in-toss/framework/plugins";
import { defineConfig } from "@granite-js/react-native/config";

export default defineConfig({
  appName: "jami-dusu-app",
  plugins: [
    appsInToss({
      brand: {
        displayName: "Jami Dusu Chart"
      }
    })
  ]
});
