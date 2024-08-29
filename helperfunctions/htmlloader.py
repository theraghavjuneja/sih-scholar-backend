from langchain_community.document_loaders import AsyncHtmlLoader
from fastapi import HTTPException
from typing import List
import logging
from bs4 import BeautifulSoup
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
def scrape_necessary_content(content:str):
    soup=BeautifulSoup(content.html,'html.parser')
    gsc_prf_in_content = soup.find('div', id='gsc_prf_in')
    gsc_prf_il_content = soup.find('div', class_='gsc_prf_il')
    response = {
            "gsc_prf_in": gsc_prf_in_content.get_text(strip=True) if gsc_prf_in_content else None,
            "gsc_prf_il": gsc_prf_il_content.get_text(strip=True) if gsc_prf_il_content else None
        }
        
    return response