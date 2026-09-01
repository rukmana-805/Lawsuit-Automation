from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.report import router as report_router

app = FastAPI()

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

@app.get("/")
def root():
    return {
        "message": "Claim Automation API Running"
    }

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routes.cases import router as cases_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown lifecycle.
    """

    print("Starting Lawsuit Automation API...")

    # Startup logic can be added here later.
    # Example:
    # - initialize database
    # - initialize shared resources
    # - validate configuration

    yield

    print("Shutting down Lawsuit Automation API...")

    # Cleanup logic can be added here later.
    # Example:
    # - close database connections
    # - cleanup shared resources


app = FastAPI(
    title="Lawsuit Automation API",
    description="API for automated case searching and PDF downloading.",
    version="1.0.0",
    lifespan=lifespan,
)


# Register API routes
app.include_router(cases_router)


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "Lawsuit Automation API is running",
    }