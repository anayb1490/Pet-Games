# app/db.py
from sqlmodel import SQLModel, Session, create_engine

# SQLite file next to your server folder; change later to Postgres by swapping this URL
DATABASE_URL = "sqlite:///./dev.db"

# echo=False to keep logs quiet; set True to see SQL logs while debugging
engine = create_engine(DATABASE_URL, echo=False)

def init_db() -> None:
    """Create all tables if they don't exist yet."""
    # IMPORTANT: make sure your models are imported before this runs
    from app.models import Pet, Task  # noqa: F401
    SQLModel.metadata.create_all(engine)

def get_session():
    """FastAPI dependency: yields a DB session and cleans it up automatically."""
    with Session(engine) as session:
        yield session
