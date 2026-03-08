from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from uuid import UUID


class DocumentResponse(BaseModel):
    Id: UUID
    Name: str
    StatusId: int
    ClientId: UUID
    UploadedAt: datetime
    ExtractedAt: Optional[datetime] = None
    ProcessingTime: int
    ConfidenceScore: int
    ProcessedAt: Optional[datetime] = None
    Tag: str
    Area: str
    Size: int

    class Config:
        from_attributes = True


class DocumentExceptionResponse(BaseModel):
    Id: UUID
    Priority: int
    StatusId: int
    Description: str
    AddedAt: datetime
    ResolvedAt: Optional[datetime] = None
    DocumentId: UUID
    DocumentName: str

    class Config:
        from_attributes = True


class DashboardResponse(BaseModel):
    TotalDocumentsCount: int
    PendingDocumentsCount: int
    ProcessedDocumentsCount: int
    ExceptionDocumentsCount: int
    AverageProcessingTime: float
    AverageConfidenceScore: float
    DocumentsCountByType: Dict[str, int]


class AnalyzeRequest(BaseModel):
    ClientId: UUID
