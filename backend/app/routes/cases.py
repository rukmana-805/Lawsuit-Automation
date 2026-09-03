from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.case_service import process_cases


router = APIRouter(
    prefix="/cases",
    tags=["Cases"]
)


class CaseDownloadRequest(BaseModel):
    csv_path: str
    output_path: str


@router.post("/download")
def download_cases(request: CaseDownloadRequest):

    try:

        result = process_cases(
            csv_path=request.csv_path,
            output_path=request.output_path
        )

        return {
            "status": "completed",
            "result": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )