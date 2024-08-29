from fastapi import APIRouter,status,HTTPException
import logging
import colorlog
logger = colorlog.getLogger()
logger.setLevel(logging.DEBUG)
from models.classmodels import WriterInfo
from helperfunctions.htmlloader import load_html_content
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

@router.post("/returnwriterinfo")
async def return_writer_info(writer_info:WriterInfo):
    urls=[f"https://scholar.google.com/citations?hl=en&user={writer_info.author_id}"]
    documents=await load_html_content(urls)
    return documents