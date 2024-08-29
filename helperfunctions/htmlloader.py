from langchain_community.document_loaders import AsyncHtmlLoader
from fastapi import HTTPException
from typing import List
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])
from langchain.schema import Document
async def load_html_content(url:str):
    try:
        loader=AsyncHtmlLoader(url)
        docs= loader.load()
        return docs
    except ValueError as e:  # Catch issues related to URL formatting or validation
        logging.error(str(e))
        raise HTTPException(status_code=400, detail=f"Invalid URL: {str(e)}")
        
    except ConnectionError as e:  # Handle connection-related errors
        logging.error(str(e))
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
        
    except TimeoutError as e:  # Handle timeout errors
        logging.error(str(e))
        raise HTTPException(status_code=504, detail=f"Request timed out: {str(e)}")
    except Exception as e:  # Catch-all for other exceptions
        logging.error(str(e))
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")