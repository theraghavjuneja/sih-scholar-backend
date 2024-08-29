from langchain_community.document_loaders import AsyncHtmlLoader
from fastapi import HTTPException
from typing import List
from langchain.schema import Document
async def load_html_content(url:str)->List[Document]:
    try:
        loader=AsyncHtmlLoader(url)
        docs=await loader.load()
        return docs
    except ValueError as e:  # Catch issues related to URL formatting or validation
        raise HTTPException(status_code=400, detail=f"Invalid URL: {str(e)}")
    except ConnectionError as e:  # Handle connection-related errors
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
    except TimeoutError as e:  # Handle timeout errors
        raise HTTPException(status_code=504, detail=f"Request timed out: {str(e)}")
    except Exception as e:  # Catch-all for other exceptions
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")