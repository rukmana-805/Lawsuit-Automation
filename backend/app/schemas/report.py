from pydantic import BaseModel


class ReportRequest(BaseModel):
    from_date: str
    to_date: str