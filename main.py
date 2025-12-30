import uvicorn
from fastapi import FastAPI

from app.api.logs import router as log_router
from app.core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Log Analyzer API")

app.include_router(log_router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
