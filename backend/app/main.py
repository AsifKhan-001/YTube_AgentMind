from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routers import auth_routes, chat_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="YTubeAgentMind API")

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)

# Anything your pipeline writes to outputs/pdf/ becomes reachable at /files/pdf/<filename>
app.mount("/files/pdf", StaticFiles(directory="outputs/pdf"), name="pdf_files")

@app.get("/")
def health_check():
    return {"status": "ok"}