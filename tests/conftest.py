# Imports
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.database import Base, get_db
import models.formats as format_models
from main import app

# Test Database Configuration
TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Fixtures
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    default_formats = [
        format_models.Format(name="Vinilo LP", description="Edicion estandar en vinilo 12 pulgadas"),
        format_models.Format(name="CD Digipak", description="Edicion en disco compacto digipak"),
        format_models.Format(name="Cassette", description="Cinta de cassette vintage analogica"),
        format_models.Format(name="Vinilo 7 Single", description="Single de 7 pulgadas a 45 RPM"),
    ]
    db.add_all(default_formats)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
