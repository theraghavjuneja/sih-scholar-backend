from langchain_community.document_loaders import AsyncHtmlLoader
from fastapi import HTTPException
from typing import List
import logging
from bs4 import BeautifulSoup
from models.classmodels import AuthorProfile,CitationStats,Article,GraphData,Stats
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),
                        logging.StreamHandler()
                    ])
import requests

# Use your Web Unblocker credentials here.
USERNAME, PASSWORD = 'raghavj_icnHh', '~Raghav00112'

# Define proxy dict.
proxiesn = {
  'http': f'http://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
  'https': f'https://{USERNAME}:{PASSWORD}@unblock.oxylabs.io:60000',
}
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
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extracting basic profile information
    name = soup.find('div', id='gsc_prf_in').get_text(strip=True)
    affiliation = soup.find('div', class_='gsc_prf_il').get_text(strip=True)
    verified_email = soup.find('div', id='gsc_prf_ivh', class_='gsc_prf_il').get_text(strip=True)
    interests = [a.get_text(strip=True) for a in soup.find_all('a', class_='gsc_prf_inta gs_ibl')]
    
    # Extracting author achievements (citations, h-index, i10-index)
    author_achievements = [td.get_text(strip=True) for td in soup.find_all('td', class_='gsc_rsb_std')]
    
    # Extracting research articles information
    research_titles = [a.get_text(strip=True) for a in soup.find_all('a', class_='gsc_a_at')]
    citations_corresponding = [a.get_text(strip=True) for a in soup.find_all('a', class_='gsc_a_ac gs_ibl')]
    years_corresponding = [span.get_text(strip=True) for span in soup.find_all('span', class_='gsc_a_h gsc_a_hc gs_ibl')]
    citation_stats = CitationStats(
        all=int(author_achievements[0]),
        since2019=int(author_achievements[1])
    )
    
    stats = Stats(
        h_index=author_achievements[2],
        i10_index=author_achievements[4],
        citations=author_achievements[0],
        publication=str(len(research_titles))
    )
    
    
    
    articles = [
        Article(title=title, cited_by=cited_by, year=year)
        for title, cited_by, year in zip(research_titles, citations_corresponding, years_corresponding)
    ]
    articles = [
        Article(title=title, cited_by=cited_by, year=year)
        for title, cited_by, year in zip(research_titles, citations_corresponding, years_corresponding)
    ]

    year_to_publication_count = {}
    for year in years_corresponding:
        if year.isdigit():
            year = int(year)
            if year in year_to_publication_count:
                year_to_publication_count[year] += 1
            else:
                year_to_publication_count[year] = 1
    
    graph_data = [
        GraphData(year=year, publications=publications)
        for year, publications in sorted(year_to_publication_count.items())
    ]
    
    author_profile = AuthorProfile(
        name=name,
        affiliation=affiliation,
        verified_email=verified_email,
        interests=interests,
        citation_stats=citation_stats,
        articles=articles,
        graph_data=graph_data,
        # ai_description=ai_description,
        stats=stats
    )
    
    return author_profile
