from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .controller import agent_router, analysis_router, tips_router, planning_router

app = FastAPI(title="organAIzer API", version="0.1.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent_router, prefix="/api/agent", tags=["agent"])
app.include_router(analysis_router, prefix="/api/analysis", tags=["analysis"])
app.include_router(tips_router, prefix="/api/tips", tags=["tips"])
app.include_router(planning_router, prefix="/api/planning", tags=["planning"])

@app.get("/")
async def root():
    return {"message": "organAIzer API - Personal AI Organization Agent"}
