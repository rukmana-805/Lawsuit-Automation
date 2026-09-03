from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI

from config import CSV_PATH, OUTPUT_PATH
from app.services.case_service import process_cases


@asynccontextmanager
async def lifespan(app: FastAPI):

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(
            process_cases,
            CSV_PATH,
            OUTPUT_PATH
        )

        future.result()

    yield