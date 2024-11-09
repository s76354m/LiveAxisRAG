from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import projects, competitors, users, documents

app = FastAPI(
    title="NDAR API",
    description="API for NDAR Project Management",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(competitors.router, prefix="/api/v1", tags=["competitors"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}