from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from datastore.session import SessionLocal


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        if session:
            session.close()

