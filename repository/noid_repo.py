from models.data.models import Noid
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

#Config logger
logging.basicConfig(level=logging.INFO,handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

class NoidRepository:

    async def insert_noid(
        self,
        session:AsyncSession,
        noid:str,
        schema:str,
        naan:str
            ) -> bool:
        """
        Create a noid record.

        Returns:
            bool: Returns True if the  creation is successful, otherwise raises an exception.
        """

        try:
            new_noid = Noid(
                noid = noid,
                schema_ = schema,
                naan = naan
            )
            session.add(new_noid)
            await session.commit()
            return True
        except Exception as e:
            await session.rollback()
            logger.error(f"Failed to insert a noid: {e}", exc_info=True)
            raise RuntimeError(f"Failed to insert a noid,please check logger for detail")
     
        
    