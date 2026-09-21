# Interactive PoV case study

Vite + React. Root directory for a later Vercel deploy: `portfolio-demo`.

- `VITE_DEMO_MODE=true` (production): in-browser deterministic Order Intake client. No fetch, no Flask.
- Local (`npm run dev`): `RealOrderIntakeClient` → `VITE_API_BASE_URL` (default `http://127.0.0.1:8080`).

This is not a live OpenShift application.
