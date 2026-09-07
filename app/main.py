from fastapi import FastAPI
from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, emails, dashboard

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION
)

app.include_router(auth.router)
app.include_router(emails.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "Welcome to AI Email Analyzer API. Visit /docs for Swagger documentation."}
