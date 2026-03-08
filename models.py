from sqlalchemy import Column, String, Integer, BigInteger, DateTime, ForeignKey, Text, Boolean, Float
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from database import Base
import uuid
from datetime import datetime


class Document(Base):
    __tablename__ = "Document"

    Id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    Name = Column(String(500), nullable=False)
    StatusId = Column(Integer, nullable=False)
    ClientId = Column(UNIQUEIDENTIFIER, nullable=False)
    ExtractedJson = Column(Text, nullable=True)
    UploadedAt = Column(DateTime, nullable=False)
    ExtractedAt = Column(DateTime, nullable=True)
    ProcessingTime = Column(BigInteger, nullable=False, default=0)
    ConfidenceScore = Column(Integer, nullable=False, default=0)
    ProcessedAt = Column(DateTime, nullable=True)
    Tag = Column(String(100), nullable=False)
    Area = Column(String(100), nullable=False)
    Size = Column(BigInteger, nullable=False)


class DocumentException(Base):
    __tablename__ = "DocumentException"

    Id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    Description = Column(String(500), nullable=False)
    Priority = Column(Integer, nullable=False)
    StatusId = Column(Integer, nullable=False)
    DocumentId = Column(UNIQUEIDENTIFIER, ForeignKey("Document.Id"), nullable=False)
    AddedAt = Column(DateTime, nullable=False)
    ResolvedAt = Column(DateTime, nullable=True)


class Vendor(Base):
    __tablename__ = "Vendor"

    Id = Column(String(50), primary_key=True)
    Name = Column(String(200), nullable=False)
    GSTIN = Column(String(50), nullable=True)
    IsActive = Column(Boolean, default=True)


class Customer(Base):
    __tablename__ = "Customer"

    Id = Column(String(50), primary_key=True)
    Name = Column(String(200), nullable=False)
    GSTIN = Column(String(50), nullable=True)
    IsActive = Column(Boolean, default=True)


class HSN(Base):
    __tablename__ = "HSN"

    Code = Column(String(50), primary_key=True)
    Description = Column(String(500), nullable=False)
    TaxRate = Column(Float, nullable=False)


class Client(Base):
    __tablename__ = "Client"

    Id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    Name = Column(String(200), nullable=False)


class Tag(Base):
    __tablename__ = "Tag"

    Id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    SortOrder = Column(Integer, nullable=False)


class DocumentStatus(Base):
    __tablename__ = "DocumentStatus"

    Id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)


class ExceptionStatus(Base):
    __tablename__ = "ExceptionStatus"

    Id = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
