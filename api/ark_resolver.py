from fastapi import APIRouter,HTTPException,status,Request
import logging
from fastapi.responses import RedirectResponse

router = APIRouter(
    tags=["Ark Reslover"],
    prefix="/ark:"
)

#Config logger
logging.basicConfig(level=logging.INFO,handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

@router.get("/{ark:path}")
async def get_url(ark:str,request:Request):
    solr = getattr(request.app.state,"solr",None)
    if not solr:
        logger.error("Solr is not available")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Solr not available")

    # Get a corresponding ark
    query = f"ark:{ark}"
    try:
        result = solr.search(query)
        if result.hits == 0:
            logger.warning(f"No documents found for ark: {ark}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Slug not found")
        
        document =  result.docs[0]
        slug = document["slug"]
        # Split slug for getting  a redirect url
        slug_split = slug.split(".")
        match slug_split:
            case [first,*rest]:
                match first:
                    case "oocihm" | "aeu" | "mw" | "sfu" | "sru" | "ooe":
                        url = "https://www.canadiana.ca/view/"
                    case "ooga":
                        url = "https://nrcan.canadiana.ca/view/"
                    case "ams" | "osmsdga":
                        url = "https://pub.canadiana.ca/view/"
                    case "carl":
                        url = "https://sve.canadiana.ca/view/"
                    case "oop":
                        url = "https://parl.canadiana.ca/view/"
                    case "oocihm":
                        url = "https://heritage.canadiana.ca/view/"
                    case "qmma":
                        if len(rest) >= 1:
                            second = rest[0]
                            match second:
                                case "NTSSNRC":
                                    url = "https://www.canadiana.ca/view/"
                                case "McGillAC":
                                    url = "https://mcgillarchives.canadiana.ca/view/"

        return {"url" :f"{url}{slug}" }             
        
    except Exception as e:
        logger.error(f"Error querying Solr: {e}",exc_info=True)
        raise
        
        