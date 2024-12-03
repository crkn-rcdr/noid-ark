from fastapi import FastAPI,Depends
from contextlib import asynccontextmanager
import pysolr
from utils.settings import SOLR_PASSWORD,SOLR_URL,SOLR_USER
from requests.auth import HTTPBasicAuth
import logging

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler()
    ]
    )
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app:FastAPI):
    # Connect to Solr
    solr = pysolr.Solr(SOLR_URL,always_commit=True,auth=HTTPBasicAuth(SOLR_USER,SOLR_PASSWORD))
    try:
        solr.ping()
        logger.info("Connected to Solr successfully")
        app.state.solr = solr
        yield 
    except pysolr.SolrError as e:
        logger.error(f"Failed to connect to Solr: {e}",exc_info=True)
        raise RuntimeError("Application cannot start without a Solr connection") from e
    finally:
        if solr:
            logger.info("Shutting down Solr client.")
    