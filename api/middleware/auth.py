import os
from fastapi import Header, HTTPException

API_KEY = os.getenv("API_KEY", "dev-key")


def require_api_key(x_api_key: str = Header(...)) -> str:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api key")
    return x_api_key
