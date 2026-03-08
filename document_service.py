from sqlalchemy.orm import Session
from models import Document, DocumentException
from schemas import DocumentExceptionResponse
from typing import List, Optional
from uuid import UUID
from datetime import datetime


class DocumentService:
    def __init__(self, db: Session):
        self.db = db

    async def add_document(self, document: Document) -> Document:
        """Add a new document to the database"""
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    async def get_documents(
        self,
        status_ids: Optional[List[int]] = None,
        tags: Optional[List[str]] = None,
        areas: Optional[List[str]] = None,
        name: Optional[str] = None
    ) -> List[Document]:
        """Get documents with optional filtering"""
        query = self.db.query(Document)

        if status_ids:
            query = query.filter(Document.StatusId.in_(status_ids))

        if tags:
            query = query.filter(Document.Tag.in_([t.lower() for t in tags]))

        if areas:
            query = query.filter(Document.Area.in_([a.lower() for a in areas]))

        if name:
            query = query.filter(Document.Name.ilike(f"%{name}%"))

        return query.all()

    async def get_document(self, document_id: UUID) -> Optional[Document]:
        """Get a document by ID"""
        return self.db.query(Document).filter(Document.Id == document_id).first()

    async def update_document(self, document: Document) -> bool:
        """Update an existing document"""
        existing = self.db.query(Document).filter(Document.Id == document.Id).first()
        if existing:
            self.db.merge(document)
            self.db.commit()
            return True
        return False

    async def resolve_exception(self, exception_id: UUID) -> bool:
        """Resolve a document exception"""
        exception = self.db.query(DocumentException).filter(DocumentException.Id == exception_id).first()
        if exception:
            exception.StatusId = 2
            exception.ResolvedAt = datetime.utcnow()
            self.db.commit()
            return True
        return False

    async def get_exceptions(
        self,
        document_id: Optional[UUID] = None,
        status_ids: Optional[List[int]] = None
    ) -> List[DocumentExceptionResponse]:
        """Get document exceptions with optional filtering"""
        query = self.db.query(
            DocumentException.Id,
            DocumentException.Priority,
            DocumentException.StatusId,
            DocumentException.Description,
            DocumentException.AddedAt,
            DocumentException.ResolvedAt,
            DocumentException.DocumentId,
            Document.Name.label("DocumentName")
        ).join(Document, DocumentException.DocumentId == Document.Id)

        if document_id:
            query = query.filter(DocumentException.DocumentId == document_id)

        if status_ids:
            query = query.filter(DocumentException.StatusId.in_(status_ids))

        results = query.all()
        
        return [
            DocumentExceptionResponse(
                Id=r.Id,
                Priority=r.Priority,
                StatusId=r.StatusId,
                Description=r.Description,
                AddedAt=r.AddedAt,
                ResolvedAt=r.ResolvedAt,
                DocumentId=r.DocumentId,
                DocumentName=r.DocumentName
            )
            for r in results
        ]

    async def add_exceptions(self, exceptions: List[DocumentException]):
        """Add multiple exceptions"""
        self.db.add_all(exceptions)
        self.db.commit()
