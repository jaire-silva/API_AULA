from fastapi import FastAPI
from routers.ola_mundo_router import router as ola_mundo_router
from routers.firebase_router import router as firebase_router


"uvicorn app:app --host 127.0.0.1 --port 8080 --reload"

app = FastAPI()

app.include_router(ola_mundo_router)
app.include_router(firebase_router)