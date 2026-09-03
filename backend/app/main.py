from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.report import router as report_router
from app.routes.cases import router as cases_router

from app.startup.automation import lifespan

app = FastAPI(
    title="Lawsuit Automation API",
    version="1.0.0",
    lifespan=lifespan,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(report_router)
app.include_router(cases_router)

@app.get("/")
def root():
    return {
        "message": "Claim Automation API Running"
    }

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Lawsuit Automation API Running"
    }