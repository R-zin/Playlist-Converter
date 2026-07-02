from dotenv import load_dotenv

load_dotenv(verbose=True)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.Authentication import router as auth_router
from routes.Converter import router as converter

app = FastAPI(title="Song Parser")

app.include_router(auth_router)
app.include_router(converter)

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}