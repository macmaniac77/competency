from fastapi import FastAPI

from .routers import answers, results, admin
from .middleware.idempotency import IdempotencyMiddleware

app = FastAPI(title="Control Assessment API", version="1.0.1")

app.include_router(answers.router)
app.include_router(results.router)
app.include_router(admin.router)

app.add_middleware(IdempotencyMiddleware)


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
