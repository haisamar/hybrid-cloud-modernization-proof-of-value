const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8080";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, options);
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(body.error || `Request failed (${response.status})`);
  }
  return body;
}

export const realClient = {
  mode: "real",

  async getSystemStatus() {
    const root = await request("/");
    const health = await request("/health");
    const ready = await request("/ready");
    return {
      application: root.service || "order-intake",
      health: health.status,
      ready: ready.status,
      persistence: root.persistence_mode || "sqlite",
      environment: root.environment || "local",
    };
  },

  async listOrders() {
    return request("/orders");
  },

  async createOrder({ customer_id, sku, quantity }) {
    return request("/orders", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customer_id, sku, quantity }),
    });
  },
};
