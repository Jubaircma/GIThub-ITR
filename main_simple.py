from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Dict
from datetime import datetime, timedelta
from uuid import uuid4
import uvicorn
import os

app = FastAPI(
    title="Audit Evidence Extractor API - Demo",
    description="Demo version with sample data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    """Serve the dashboard"""
    dashboard_path = os.path.join(os.path.dirname(__file__), "static", "dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path)
    return {"message": "Audit Evidence Extractor API is running", "status": "healthy"}


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"message": "Audit Evidence Extractor API is running", "status": "healthy"}


@app.get("/api/document")
async def get_documents():
    """Get documents - Returns sample data"""
    return [
        {
            "Id": str(uuid4()),
            "Name": "Invoice_2024_001.pdf",
            "StatusId": 3,
            "ClientId": str(uuid4()),
            "UploadedAt": (datetime.utcnow() - timedelta(days=2)).isoformat(),
            "ExtractedAt": (datetime.utcnow() - timedelta(days=2)).isoformat(),
            "ProcessingTime": 45,
            "ConfidenceScore": 92,
            "ProcessedAt": (datetime.utcnow() - timedelta(days=2)).isoformat(),
            "Tag": "Sales Invoice",
            "Area": "Income",
            "Size": 245
        },
        {
            "Id": str(uuid4()),
            "Name": "PO_20240115.pdf",
            "StatusId": 2,
            "ClientId": str(uuid4()),
            "UploadedAt": (datetime.utcnow() - timedelta(hours=3)).isoformat(),
            "ExtractedAt": None,
            "ProcessingTime": 0,
            "ConfidenceScore": 0,
            "ProcessedAt": None,
            "Tag": "Purchase Order",
            "Area": "Expenses",
            "Size": 156
        },
        {
            "Id": str(uuid4()),
            "Name": "GRN_2024_045.pdf",
            "StatusId": 4,
            "ClientId": str(uuid4()),
            "UploadedAt": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "ExtractedAt": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "ProcessingTime": 52,
            "ConfidenceScore": 78,
            "ProcessedAt": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            "Tag": "Good Received Note",
            "Area": "Expenses",
            "Size": 198
        },
        {
            "Id": str(uuid4()),
            "Name": "Invoice_2024_002.pdf",
            "StatusId": 3,
            "ClientId": str(uuid4()),
            "UploadedAt": (datetime.utcnow() - timedelta(days=3)).isoformat(),
            "ExtractedAt": (datetime.utcnow() - timedelta(days=3)).isoformat(),
            "ProcessingTime": 38,
            "ConfidenceScore": 95,
            "ProcessedAt": (datetime.utcnow() - timedelta(days=3)).isoformat(),
            "Tag": "Sales Invoice",
            "Area": "Income",
            "Size": 220
        },
        {
            "Id": str(uuid4()),
            "Name": "PO_20240118.pdf",
            "StatusId": 3,
            "ClientId": str(uuid4()),
            "UploadedAt": (datetime.utcnow() - timedelta(days=5)).isoformat(),
            "ExtractedAt": (datetime.utcnow() - timedelta(days=5)).isoformat(),
            "ProcessingTime": 41,
            "ConfidenceScore": 89,
            "ProcessedAt": (datetime.utcnow() - timedelta(days=5)).isoformat(),
            "Tag": "Purchase Order",
            "Area": "Expenses",
            "Size": 180
        }
    ]


@app.get("/api/document/dashboard")
async def get_dashboard():
    """Get dashboard statistics - Returns sample data"""
    return {
        "TotalDocumentsCount": 15,
        "PendingDocumentsCount": 3,
        "ProcessedDocumentsCount": 10,
        "ExceptionDocumentsCount": 2,
        "AverageProcessingTime": 45.5,
        "AverageConfidenceScore": 87.3,
        "DocumentsCountByType": {
            "Sales Invoice": 6,
            "Purchase Order": 4,
            "Good Received Note": 2,
            "Unknown": 1
        }
    }


@app.get("/api/document/exceptions")
async def get_exceptions():
    """Get document exceptions"""
    return []


@app.get("/docs")
async def get_docs():
    """Redirect to API docs"""
    return {"message": "API Documentation", "swagger_ui": "/docs", "redoc": "/redoc"}


if __name__ == "__main__":
    uvicorn.run("main_simple:app", host="0.0.0.0", port=5167, reload=True)
