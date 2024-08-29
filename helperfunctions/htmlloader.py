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
    # content is already html(in almost all I saw) so I am not using content.html directly parsing the content
    """
    What if this content(to return) becomes much big-> In that case lazy loading etc.?? or entire
    
    """
    soup=BeautifulSoup(content,'html.parser')
    author_name = soup.find('div', id='gsc_prf_in')
    work_place= soup.find('div', class_='gsc_prf_il')
    verified_email_at=soup.find('div', id='gsc_prf_ivh', class_='gsc_prf_il')
    interests = soup.find_all('a', class_='gsc_prf_inta gs_ibl')
    research_title = soup.find_all('a', class_='gsc_a_at')
    citations_corresponding = soup.find_all('a', class_='gsc_a_ac gs_ibl')
    years_corresponding = soup.find_all('span', class_='gsc_a_h gsc_a_hc gs_ibl')
    authorAchievements= soup.find_all('td', class_='gsc_rsb_std')
    response = {
            "Name": author_name.get_text(strip=True) if author_name else None,
            "WorkPlace": work_place.get_text(strip=True) if work_place else None,
            "Verified Email":verified_email_at.get_text(strip=True) if verified_email_at else None,
            "Interests": [link.get_text(strip=True) for link in interests] if interests else [],
            "Research Title": [link.get_text(strip=True) for link in research_title] if research_title else [],
            "Corresponding Citations": [link.get_text(strip=True) for link in citations_corresponding] if citations_corresponding else [],
            "Corresponding Years": [span.get_text(strip=True) for span in years_corresponding] if years_corresponding else [],
            # sc1 not required isme bas headings hai
            "Author Achievements": [td.get_text(strip=True) for td in authorAchievements] if authorAchievements else []  # Extract text from the gsc_rsb_std elements
            
        }
        
    return response