# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from db.session import Base, get_db
import core.security as security

# — Use SQLite in memory for fast, isolated tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def prepare_db():
    # create all tables before tests, drop after
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db):
    # 1) override get_db to use our in‑memory session
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # 2) stub out auth so you don’t need real tokens
    class DummyUser:
        id = 1

    app.dependency_overrides[security.get_current_user] = lambda: DummyUser()
    app.dependency_overrides[security.admin_required]    = lambda: DummyUser()

    return TestClient(app)
