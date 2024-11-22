from models.data.models import Counter
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

#Config logger
logging.basicConfig(level=logging.INFO,handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

class CounterRepository:
    def __init__(self) -> None:
        pass

    async def update_counter(self,session:AsyncSession) -> bool:
        """
        Update the `current` field of the unique Counter object and commit the transaction.
        If the Counter object does not exist, create a new record.

        Returns:
            bool: Returns True if the update or creation is successful, otherwise raises an exception.
        """

        try:
            sql = select(Counter)
            result = await session.execute(sql)
            counter = result.scalars().first()

            if counter:
                counter.current += 1
            else:
                counter = Counter(current=1)
                session.add(counter)
            
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.info(f"Failed to update counter: {e}", exc_info=True)
            raise RuntimeError(f"Failed to update counter,please check logger for detail")
        return True
        
    async def get_counter(self,session:AsyncSession) -> int:
        """
        Retrieve the `current` value of the Counter object.

        Returns:
            int: The value of the `current` field. Returns 0 if it does not exist.
        """
        try:
            sql = select(Counter)
            sql.execution_options(synchronize_session="fetch")
            result = await session.execute(sql)
            counter = result.scalar_one_or_none()
            return counter.current if counter else 0
        except Exception as e:
            logger.info(f"Failed to get a counter: {e}", exc_info=True)
            raise RuntimeError(f"Failed to get a counter,please check logger for detail")
    

