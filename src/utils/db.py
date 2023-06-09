import aioredis
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


REDIS_URI = "redis://localhost:6379"
POSTGRES_URI = "postgresql://tyler:thefightclub@localhost:5433/pyauthdb"

Base = declarative_base()

engine = create_engine(POSTGRES_URI)


async def get_redis_conn():
    try:
        # Create a pool to reuse the same connection and reduce the number
        # of connections for multiple operations
        pool = aioredis.ConnectionPool(max_connections=5).from_url(REDIS_URI)

        # Yield the connection to avoid closing it
        r = aioredis.Redis(connection_pool=pool, ssl=False, decode_responses=True)

        yield r

    finally:
        await r.close()
        await pool.disconnect()


def init_db():
    Base.metadata.create_all(bind=engine)


def get_pg_conn():
    try:
        session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        sess = session()
        yield sess
    finally:
        sess.close()
