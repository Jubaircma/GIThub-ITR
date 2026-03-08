import httpx
from config import settings
from typing import Optional, Tuple
import asyncio


class OpenAIService:
    def __init__(self):
        self.endpoint = settings.openai_api_endpoint
        self.api_key = settings.openai_api_key

    async def start_analyzer(self, file_content: bytes, filename: str) -> Optional[Tuple[str, str]]:
        """Start document analysis and return (analyzer_id, status)"""
        url = f"{self.endpoint}contentunderstanding/analyzers/prebuilt-documentFields:analyzeBinary?stringEncoding=codePoint&api-version=2025-11-01"
        
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
        }
        
        files = {"file": (filename, file_content, "application/octet-stream")}
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(url, headers=headers, files=files)
                
                if response.status_code in [200, 202]:
                    result = response.json()
                    analyzer_id = result.get("id")
                    status = result.get("status")
                    
                    if analyzer_id and status:
                        return (analyzer_id, status)
            except Exception as e:
                print(f"Error starting analyzer: {e}")
                return None
        
        return None

    async def get_analyzer_result(self, analyzer_id: str) -> Optional[dict]:
        """Get analysis result for given analyzer ID"""
        url = f"{self.endpoint}contentunderstanding/analyzerResults/{analyzer_id}?api-version=2025-11-01"
        
        headers = {
            "Ocp-Apim-Subscription-Key": self.api_key,
            "Accept": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                print(f"Error getting analyzer result: {e}")
                return None
        
        return None
