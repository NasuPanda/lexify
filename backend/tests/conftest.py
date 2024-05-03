import pytest
from sqlalchemy.orm import sessionmaker
from app.core.database import engine

class TestSessionContext:
    """Context to hold the current session."""
    session = None

@pytest.fixture(
    scope='function',
#   autouse=True,
)
def db():
    """Creates a SQLAlchemy session with a SAVEPOINT for testing."""
    connection = engine.connect()
    trans = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()
    session.begin_nested()  # SAVEPOINT

    TestSessionContext.session = session  # Store the session in the context

    yield session

    session.close()
    trans.rollback()
    connection.close()
    TestSessionContext.session = None  # Clear the session from the context after test
