from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app import models
from app.routers import comics, chapters

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Webtoon Reader API",
    description="A Manhwa Clan style comic reader backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(comics.router, prefix="/api/comics", tags=["comics"])
app.include_router(chapters.router, prefix="/api/chapters", tags=["chapters"])

@app.get("/")
def root():
    return {"message": "Welcome to Webtoon Reader API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
