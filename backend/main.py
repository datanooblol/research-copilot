"""FastAPI application entry point for Research Copilot."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.search.endpoint import router as search_router
from routers.dashboard.endpoint import router as dashboard_router
from routers.papers.endpoint import router as papers_router

app = FastAPI(title="Research Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)
app.include_router(dashboard_router)
app.include_router(papers_router)

@app.get("/")
def root():
    """Root endpoint.
    
    Returns:
        Welcome message.
    """
    return {"message": "Research Copilot API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)