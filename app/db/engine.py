from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# local
engine = create_engine(str(settings.DATABASE_URI))

# prod
# dbUrl = f"sqlite+{str(settings.TURSO_DATABASE_URL)}/?authToken={str(settings.TURSO_AUTH_TOKEN)}&secure=true"
# engine = create_engine(dbUrl, connect_args={'check_same_thread': False}, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



