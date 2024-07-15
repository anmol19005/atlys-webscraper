import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import config
from schemas import ScrapeSettings, ScrapeResponse
from scraper import Scraper

load_dotenv()

app = FastAPI()
security = HTTPBearer()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != config.Config.API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing token")


@app.post("/scrape", response_model=ScrapeResponse)
def scrape(scrape_settings: ScrapeSettings, token: str = Depends(verify_token)):
    try:
        scraper = Scraper(scrape_settings)
        results = scraper.scrape()
        return results
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise HTTPException(status_code=500, detail="Scraping failed")
