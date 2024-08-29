from fastapi import APIRouter,status,HTTPException
from fastapi.responses import RedirectResponse
import logging
import colorlog
from bs4 import BeautifulSoup
logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)
from models.classmodels import WriterInfo
from helperfunctions.htmlloader import load_html_content,scrape_necessary_content
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(levelname)s: %(message)s',
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
router=APIRouter()
@router.get("/", include_in_schema=False)  
async def root():
    return RedirectResponse(url="/docs")
@router.post("/returnwriterinfo")
async def return_writer_info(writer_info:WriterInfo):
    urls=f"https://scholar.google.com/citations?hl=en&user={writer_info.author_id}"
    documents=await load_html_content(urls)
    # further processing this document for scraping purposes
    return scrape_necessary_content(documents)
