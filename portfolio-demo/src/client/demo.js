const SEED = [
  {
    id: 1001,
    customer_id: "CUST-DEMO",
    sku: "PUMP-A",
    quantity: 2,
    status: "accepted",
  },
];

let orders = SEED.map((row) => ({ ...row }));
let nextId = 1002;

function clone(rows) {
  return rows.map((row) => ({ ...row }));
}

export const demoClient = {
  mode: "demo",

  async getSystemStatus() {
    return {
      application: "healthy",
      health: "ok",
      ready: "ready",
      persistence: "In-browser deterministic state",
      povImplementation: "SQLite locally via DATABASE_URL",
      environment: "public-deterministic-demo",
    };
  },

  async listOrders() {
    return clone(orders);
  },

  async createOrder({ customer_id, sku, quantity }) {
    const order = {
      id: nextId,
      customer_id,
      sku,
      quantity,
      status: "accepted",
    };
    nextId += 1;
    orders = [...orders, order];
    return { ...order };
  },
};
