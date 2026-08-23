from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.schemas.report import ReportRequest
from scripts.playwright.detail_report import download_report


router = APIRouter()


@router.post("/download-csv")
def download_csv(data: ReportRequest):

    file_path = download_report(
        data.from_date,
        data.to_date
    )

    print(f"Sending file: {file_path}")

    return FileResponse(
        path=file_path,
        filename="report.csv",
        media_type="text/csv"
    )