from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base
import ssl
from utils.settings import DATABASE_URL

ssl_context = ssl.create_default_context(cafile="DigiCertGlobalRootG2.crt.pem")
engine = create_async_engine(
    DATABASE_URL,
    future=True,
    echo=False,
    connect_args={"ssl":ssl_context}
)

AsyncSessionFactory = sessionmaker(engine,expire_on_commit=False,class_=AsyncSession)
Base = declarative_base()

async def async_get_db():
    async with AsyncSessionFactory() as db:
        yield db

