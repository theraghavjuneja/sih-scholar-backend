from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
import time
loader = AsyncHtmlLoader(["https://www.wsj.com"])
start=time.time()
html = loader.load()
end=time.time()
print(html)
print(end-start)
loader2=AsyncChromiumLoader(["https://www.wsj.com"])
start=time.time()
html2=loader2.load()
end=time.time()
print(end-start)
print(html2)
print(html==html2)