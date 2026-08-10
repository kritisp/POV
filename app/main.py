from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import engine, Base

from app.routers import brands, categories, mappings, recommendation, feedback

# Create all tables on startup
# In production, use Alembic for migrations instead
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="POV - AI Fashion Intelligence Platform",
    description="Backend API prototype for cross-brand clothing size translation.",
    version="1.0.0"
)

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(brands.router)
app.include_router(categories.router)
app.include_router(mappings.router)
app.include_router(recommendation.router)
app.include_router(feedback.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "POV MVP API is running!"}
