import { useEffect, useState } from "react";
import { DEMO_MODE, getOrderIntakeClient } from "./client";

const client = getOrderIntakeClient();

export default function LivePovDemo() {
  const [status, setStatus] = useState(null);
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState("");
  const [customerId, setCustomerId] = useState("CUST-1042");
  const [sku, setSku] = useState("VALVE-B");
  const [quantity, setQuantity] = useState(1);
  const [busy, setBusy] = useState(false);
  const [created, setCreated] = useState(false);

  async function refresh() {
    setError("");
    const nextStatus = await client.getSystemStatus();
    const nextOrders = await client.listOrders();
    setStatus(nextStatus);
    setOrders(nextOrders);
  }

  useEffect(() => {
    refresh().catch((exc) => {
      setError(exc.message || "Unable to load Order Intake status.");
      setStatus(null);
      setOrders([]);
    });
  }, []);

  async function onCreate(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      await client.createOrder({
        customer_id: customerId.trim(),
        sku: sku.trim(),
        quantity: Number(quantity),
      });
      await refresh();
      setCreated(true);
    } catch (exc) {
      setError(exc.message || "Create order failed.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="live-demo" id="live-pov-demo">
      <p className="section-kicker">Live PoV demo</p>
      <h2>Try the application</h2>
      <p className="section-intro">
        Both versions do the same basic job: accept and show customer orders.
        Try it below. The important changes happen behind the screen.
      </p>

      <div className="labels">
        {DEMO_MODE ? (
          <span className="mode-label">Public deterministic PoV demo</span>
        ) : (
          <span className="mode-label mode-real">Connected to local modernized application</span>
        )}
        <span className="mode-label mode-arch">
          Design target: OpenShift-compatible · live cluster not used
        </span>
      </div>

      <div className="cards compare">
        <article>
          <h3>What stayed the same</h3>
          <p>
            <strong>Legacy:</strong> Creating and viewing orders works.
            <br />
            <strong>Modernized:</strong> Creating and viewing orders still works.
          </p>
        </article>
        <article className="selected">
          <h3>What became better</h3>
          <p>
            Settings are no longer buried in the code. The app can report
            whether it works and is ready. Release steps are written down.
          </p>
          <small>Technical: DATABASE_URL · Dockerfile · OpenShift manifests · Terraform</small>
        </article>
      </div>

      {error ? <p className="error">{error}</p> : null}

      <div className="status-grid">
        <div>
          <h3>System status</h3>
          <dl>
            <div>
              <dt>Application</dt>
              <dd>{status ? "Healthy" : (error ? "Unavailable" : "Loading")}</dd>
            </div>
            <div>
              <dt>Ready for users</dt>
              <dd>{status?.ready === "ready" ? "Yes" : "—"}</dd>
            </div>
            <div>
              <dt>Data in this demo</dt>
              <dd>{DEMO_MODE ? "Saved temporarily in this browser" : status?.persistence || "—"}</dd>
            </div>
            <div>
              <dt>Demo mode</dt>
              <dd>{DEMO_MODE ? "Runs in this browser" : "Connected to local app"}</dd>
            </div>
          </dl>
          <div className="technical-status">
            <strong>Technical details</strong>
            <span>Health endpoint: <code>/health</code> = {status?.health || "—"}</span>
            <span>Readiness endpoint: <code>/ready</code> = {status?.ready || "—"}</span>
            {DEMO_MODE ? <span>Storage type: In-browser deterministic state</span> : null}
            <span>
              Real local PoV persistence:{" "}
              {status?.povImplementation || (DEMO_MODE ? "SQLite via DATABASE_URL" : status?.persistence || "—")}
            </span>
          </div>
        </div>

        <form onSubmit={onCreate}>
          <h3>Create order</h3>
          <label>
            Customer ID
            <input value={customerId} onChange={(e) => setCustomerId(e.target.value)} required />
          </label>
          <label>
            SKU
            <input value={sku} onChange={(e) => setSku(e.target.value)} required />
          </label>
          <label>
            Quantity
            <input
              type="number"
              min="1"
              step="1"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              required
            />
          </label>
          <button type="submit" disabled={busy}>
            Create Order
          </button>
        </form>
      </div>

      {created ? (
        <aside className="created-callout">
          <p><strong>Business capability unchanged:</strong> The customer can still submit an order.</p>
          <p><strong>Operating model improved:</strong> The modernized version is easier to configure, monitor, package, and deploy.</p>
        </aside>
      ) : null}

      <h3>Orders</h3>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer</th>
              <th>SKU</th>
              <th>Quantity</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {orders.length === 0 ? (
              <tr>
                <td colSpan={5}>No orders yet.</td>
              </tr>
            ) : (
              orders.map((order) => (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.customer_id}</td>
                  <td>{order.sku}</td>
                  <td>{order.quantity}</td>
                  <td>{order.status}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div className="evidence">
        <h3>What changed behind the scenes?</h3>
        <p>
          <strong>Business capability:</strong> Order intake
        </p>
        <p>
          <strong>Legacy behavior:</strong> Manual startup, settings tied to a
          host, and no signal that says the app is ready for users.
        </p>
        <p>
          <strong>Modernized behavior:</strong> Settings outside the code,
          health and readiness endpoints, structured logs, container-ready
          runtime, and OpenShift-compatible deployment.
        </p>
      </div>
    </section>
  );
}
