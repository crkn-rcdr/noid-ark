from fastapi import APIRouter,Depends,HTTPException
from utils.settings import CRKN_PREFIX_TEMPLATE_MAPPING
from models.request.noid_request import NoidRequest
from models.response.noid_response import NoidResponse
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from db_config.sqlalchemy_async_connect import async_get_db
from utils.noid_generator import NoidGenerator
from utils.error_handlers import InvalidTemplateError
import logging
from repository.counter import CounterRepository

router = APIRouter(
    tags=["Noid"]
)

#Initialize an asyncio lock
noid_lock = asyncio.Lock()

# Initialize the NOIDGenerator instance
noid_generator = NoidGenerator()

#Config logger
logging.basicConfig(level=logging.INFO,handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

@router.post("/generate_noids",response_model = NoidResponse)
async def generate_noids(request:NoidRequest,session: AsyncSession = Depends(async_get_db)):
    """
    Generate a specified number of NOIDs based on the provided type, scheme, and NAAN.

    Args:
        request (NOIDRequest): The request body containing generation parameters.
        session (AsyncSession): The database session (injected by FastAPI).

    Returns:
        NOIDResponse: A list of generated NOIDs.
    """
    m = request.m
    type_ = request.type_
    schema_ = request.schema_
    naan  = request.naan
    # Retrieve the corresponding prefix and mask based on type
    mapping = CRKN_PREFIX_TEMPLATE_MAPPING.get(type_)
    if not mapping:
        raise HTTPException(
            status_code=400,
            detail="Invalid type. Valid types are 'generic', 'canvas', 'collection', 'manifest','canvases','collections','manifests'."
        )
    prefix,mask = mapping
    # Construct the template, e.g., 'm.reedeedeedk'
    template = f"{prefix}.{mask}"
    counter_instance = CounterRepository()

    noids = []
    try:
        async with noid_lock:
            for _ in range(m):
                noid = await noid_generator.mint(template = template,schema = schema_,naan = naan,session = session,counter_instance = counter_instance)
                noids.append(noid)
    except InvalidTemplateError  as e:
        logger.error(f"Invalid template: {e}")
        raise HTTPException(status_code=400,detail="Invalid Template")
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error,check the log for detail")
    
    return NoidResponse(noids=noids)


