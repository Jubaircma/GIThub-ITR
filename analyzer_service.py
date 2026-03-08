from sqlalchemy.orm import Session
from models import Document, DocumentException, Vendor, Customer, HSN
from openai_service import OpenAIService
from document_service import DocumentService
from json_helper import find_first_value_by_key, find_values_by_key
from datetime import datetime
from uuid import UUID, uuid4
import asyncio
import json


class AnalyzerService:
    def __init__(self, db: Session):
        self.db = db
        self.openai_service = OpenAIService()
        self.document_service = DocumentService(db)

    async def analyze_document(self, file_content: bytes, filename: str, client_id: UUID):
        """Analyze a document using Azure OpenAI"""
        start_time = datetime.now()
        
        # Create initial document
        document = Document(
            Id=uuid4(),
            Name=filename,
            StatusId=1,
            UploadedAt=datetime.utcnow(),
            ClientId=client_id,
            Area="Unclassified",
            Tag="Unknown",
            Size=len(file_content) // 1024,
            ProcessingTime=0,
            ConfidenceScore=0
        )
        
        self.db.add(document)
        self.db.commit()
        
        # Process in background
        asyncio.create_task(self._process_document(document, file_content, filename, start_time))

    async def _process_document(self, document: Document, file_content: bytes, filename: str, start_time: datetime):
        """Background processing of document"""
        try:
            # Start analysis
            result = await self.openai_service.start_analyzer(file_content, filename)
            
            if not result:
                document.StatusId = 5  # Failed
                self.db.commit()
                return

            analyzer_id, status = result
            document.StatusId = 2  # Processing
            self.db.commit()

            # Poll for results
            json_result = None
            while status == "Running":
                await asyncio.sleep(2)  # Wait 2 seconds between polls
                json_result = await self.openai_service.get_analyzer_result(analyzer_id)
                
                if json_result:
                    status = find_first_value_by_key(json_result, "status")

            if status == "Succeeded" and json_result:
                document.ExtractedAt = datetime.utcnow()
                document.ExtractedJson = json.dumps(json_result)

                # Extract document type
                fields = json_result.get("result", {}).get("contents", [{}])[0].get("fields", {})
                doc_type = "Unknown"

                # Check for invoice type
                invoice_type = find_first_value_by_key(fields, "InvoiceType")
                if invoice_type and "GST Intra-State B2B" in str(invoice_type):
                    doc_type = document.Tag = "Sales Invoice"
                    document.Area = "Income"

                # Check for Purchase Order
                po_no = find_first_value_by_key(fields, "PurchaseOrderNumber")
                po_date = find_first_value_by_key(fields, "PurchaseOrderDate")
                if po_no and po_date:
                    doc_type = document.Tag = "Purchase Order"
                    document.Area = "Expenses"

                # Check for GRN
                grn_no = find_first_value_by_key(fields, "GRN No")
                grn_date = find_first_value_by_key(fields, "GRN Date")
                if grn_no and grn_date:
                    doc_type = document.Tag = "Good Received Note"
                    document.Area = "Expenses"

                # Get anomalies
                score, exceptions = self._get_anomalies(document.Id, json_result, doc_type)

                if exceptions:
                    document.StatusId = 4  # Exception
                    document.ConfidenceScore = score
                    self.db.add_all(exceptions)
                else:
                    if doc_type == "Unknown":
                        document.StatusId = 5  # Failed
                    else:
                        document.StatusId = 3  # Completed
                        document.ConfidenceScore = score
            else:
                document.StatusId = 5  # Failed

            # Calculate processing time
            end_time = datetime.now()
            document.ProcessingTime = int((end_time - start_time).total_seconds())
            document.ProcessedAt = datetime.utcnow()

            self.db.commit()

        except Exception as e:
            print(f"Error processing document: {e}")
            document.StatusId = 5  # Failed
            self.db.commit()

    def _get_anomalies(self, document_id: UUID, json_result: dict, doc_type: str):
        """Check for anomalies and return (score, exceptions)"""
        vendors = self.db.query(Vendor).all()
        customers = self.db.query(Customer).all()
        hsns = self.db.query(HSN).all()

        fields = json_result.get("result", {}).get("contents", [{}])[0].get("fields", {})
        exceptions = []
        
        # Calculate confidence score
        confidences = find_values_by_key(fields, "confidence")
        score = 0
        if confidences:
            score = int((sum(confidences) * 100) / len(confidences))

        # Check for Purchase Order anomalies
        if doc_type == "Purchase Order":
            seller_name = find_first_value_by_key(fields, "SellerName")
            total_values = find_values_by_key(fields, "TotalPurchaseOrderValue")

            # Mandatory fields check
            if not seller_name or not total_values:
                exceptions.append(DocumentException(
                    Id=uuid4(),
                    Description="MANDATORY_MISSING",
                    Priority=1,
                    StatusId=1,
                    DocumentId=document_id,
                    AddedAt=datetime.utcnow()
                ))

            # Validate vendor
            if seller_name:
                vendor_found = any(v.Name.lower() == str(seller_name).lower() for v in vendors)
                if not vendor_found:
                    exceptions.append(DocumentException(
                        Id=uuid4(),
                        Description="INVALID_VENDOR",
                        Priority=1,
                        StatusId=1,
                        DocumentId=document_id,
                        AddedAt=datetime.utcnow()
                    ))

        # Similar checks can be added for other document types
        
        return score, exceptions
