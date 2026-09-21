import { demoClient } from "./demo";
import { realClient } from "./real";

export const DEMO_MODE = import.meta.env.VITE_DEMO_MODE === "true";

export function getOrderIntakeClient() {
  return DEMO_MODE ? demoClient : realClient;
}
