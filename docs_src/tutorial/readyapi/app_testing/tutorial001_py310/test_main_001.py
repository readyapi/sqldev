from readyapi.testclient import TestClient
from sqldev import Session, SQLDev, create_engine

from .main import app, get_session  # (1)!


def test_create_hero():
    engine = create_engine(
        "sqlite:///testing.db", connect_args={"check_same_thread": False}
    )
    SQLDev.metadata.create_all(engine)

    with Session(engine) as session:

        def get_session_override():
            return session

        app.dependency_overrides[get_session] = get_session_override

        client = TestClient(app)  # (2)!

        response = client.post(  # (3)!
            "/heroes/", json={"name": "Deadpond", "secret_name": "Nx Pkg"}
        )
        app.dependency_overrides.clear()
        data = response.json()  # (4)!

        assert response.status_code == 200  # (5)!
        assert data["name"] == "Deadpond"  # (6)!
        assert data["secret_name"] == "Nx Pkg"  # (7)!
        assert data["age"] is None  # (8)!
        assert data["id"] is not None  # (9)!
