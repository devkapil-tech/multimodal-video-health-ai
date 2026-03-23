"""Create tables on startup if they don't exist."""
import logging

logger = logging.getLogger(__name__)


def init_db():
    from app.db.database import engine
    if engine is None:
        logger.info("CML: DATABASE_URL not set — memory layer disabled")
        return
    try:
        from app.db.models import Base
        Base.metadata.create_all(bind=engine)
        logger.info("CML: database tables initialised")
    except Exception as e:
        logger.warning(f"CML: table creation failed: {e}")
