# Control Assessment API (FastAPI)

Fast, minimal backend for your GPT Actions–driven **Control Engineer Assessment**.
- **POST** `/submit_answer` – record a single answer + model assessment
- **GET** `/results` – fetch rollup when enough answers are in
- **GET** `/healthz` – health check

## Quick start (local)
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export API_KEY=dev-key   # set your real key in prod
uvicorn main:app --reload
# test:
curl -H "x-api-key: $API_KEY" http://127.0.0.1:8000/healthz
```

## Deploy: Koyeb (free, recommended)
1. Push this repo to GitHub.
2. In Koyeb: **Create Web Service → GitHub → select this repo**.
3. Set **Run command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add **Environment Variable**: `API_KEY` → your secret.
5. Deploy. Your API will be at `https://<service>.<region>.koyeb.app`.

> **OpenAPI for GPT “Import from URL”**: Update `openapi.yaml` `servers.url` to your Koyeb URL and push. Then in GPT Builder → **Configure → Actions → Add action → Import from URL** and paste the raw URL to your `openapi.yaml` (e.g., GitHub raw link).

## Deploy: Render (free web service, cold starts possible)
1. Create **Web Service** from this repo.
2. Set **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
3. Add `API_KEY` env var. Deploy. Your API will be at `https://<service>.onrender.com`.
   - Note: Free tier may sleep; first request can take ~30–60s.

## Endpoints
- `GET /healthz` → `{"ok": true}`
- `POST /submit_answer` (requires `x-api-key`)
  ```json
  {
    "assessment_id": "abc123",
    "question_id": "Q_01",
    "answer_text": "Ladder uses OTE with seal-in...",
    "model_score": 0.86,
    "rubric": {"clarity": 0.9},
    "meta": {"duration_ms": 42000, "difficulty": "advanced"}
  }
  ```
- `GET /results?assessment_id=abc123&include_details=false`

## cURL smoke test
```bash
export BASE=https://YOUR-SERVICE.koyeb.app
export KEY=YOUR-API-KEY

curl -s -H "x-api-key: $KEY" "$BASE/healthz"

curl -s -X POST "$BASE/submit_answer"   -H "x-api-key: $KEY" -H "Content-Type: application/json"   -d '{"assessment_id":"abc123","question_id":"Q1","answer_text":"42","model_score":0.9,"meta":{"difficulty":"basic"}}'

curl -s -H "x-api-key: $KEY" "$BASE/results?assessment_id=abc123"
```

## Notes
- Keep requests fast (<45s) to satisfy GPT Actions timeouts.
- `API_KEY` is checked via `x-api-key` header.
- Storage is in-memory for simplicity; swap `DB` with a real store when ready.
