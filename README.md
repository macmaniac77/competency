# Control Engineer Assessment System

This project delivers a lightweight yet durable platform for evaluating control engineers. It pairs a FastAPI service (for GPT Actions) with a Next.js admin dashboard. The system records answers, rolls up results, and lets reviewers override and export outcomes.

## Mission
- Ask technical questions and score responses in real time.
- Post each answer and model score to the API via GPT Actions.
- Roll up the results and produce a clean report.
- Give reviewers a dashboard to audit, override, and export data.

## Architecture
```
GPT ↔ Actions (OpenAPI) → FastAPI service → DB
Admin Dashboard (Next.js + Tailwind + shadcn/ui) → API (read + admin routes)
```
- **Public API**: `/submit_answer`, `/results`, `/healthz`
- **Admin API**: `/sessions`, `/admin/answers/{assessment_id}/{answer_id}`, `/export/csv`
- **Dashboard**: lists sessions, drills into answers, overrides scores, exports CSV, regenerates summaries.
- **Hosting**: Koyeb (API) and Vercel (dashboard). `openapi.yaml` is served statically for GPT “Import from URL”.

## Repo structure
```
/api
  main.py
  models.py
  db.py
  routers/
    answers.py
    results.py
    admin.py
  middleware/
    auth.py
    idempotency.py
  openapi.yaml
  requirements.txt
/web
  app/
    page.tsx        # sessions list
    s/[id]/page.tsx # session detail
    policy/page.tsx
  components/*      # shadcn/ui
  lib/api.ts
  .env.example
```

## Quick start – API
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r api/requirements.txt
export API_KEY=dev-key   # set your real key in prod
uvicorn api.main:app --reload
# smoke test
curl -H "x-api-key: $API_KEY" http://127.0.0.1:8000/healthz
```

## Quick start – Dashboard
The dashboard is a basic Next.js skeleton.
```bash
cd web
npm install
npm run dev
```

## Deploying
1. Push this repo to GitHub.
2. **API** on Koyeb:
   - Run command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
   - Env var: `API_KEY` with your secret.
3. **Dashboard** on Vercel:
   - Set `NEXT_PUBLIC_API_BASE` to your deployed API URL.
4. Update `api/openapi.yaml` `servers.url` to your API base and expose the raw file for GPT “Import from URL”.

## API surface (excerpt)
- `POST /submit_answer` – record a single answer + model score.
- `GET /results?assessment_id=...&include_details=true`
- `GET /healthz` – health check.
- `GET /sessions` – list sessions with basic stats.
- `GET /sessions/{assessment_id}` – fetch answers in a session.
- `PATCH /admin/answers/{assessment_id}/{answer_id}` – override an answer.
- `GET /export/csv?assessment_id=...` – CSV export.

All data endpoints require `x-api-key` authentication. Health checks are open. `Idempotency-Key` headers are supported on write routes.

## Notes
- Storage is in-memory for now; swap in Postgres or SQLite for production.
- Keep request handling under 45s to satisfy GPT Action timeouts.
- Privacy policy lives at `/policy` on the dashboard and should be hosted on the same domain.
