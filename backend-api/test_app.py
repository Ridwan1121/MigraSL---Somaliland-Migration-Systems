"""
MigraSL---Somaliland-Migration-Systems - Unit Tests
"""
import sqlite3

import pytest
from fastapi.testclient import TestClient
from app import app
from config import require_production_environment
from database import _migrate_legacy_sqlite_database, get_db, init_db
from staff import StaffDB, pwd_context

client = TestClient(app)


@pytest.fixture(autouse=True)
def ensure_test_user():
    init_db()
    db = next(get_db())
    try:
        user = db.query(StaffDB).filter(StaffDB.username == "Ridwan").first()
        if not user:
            db.add(
                StaffDB(
                    username="Ridwan",
                    full_name="Ridwan Farah",
                    password_hash=pwd_context.hash("AKIID12345"),
                    role="superadmin",
                    is_active=True,
                )
            )
            db.commit()
        elif not user.is_active or not pwd_context.verify("AKIID12345", user.password_hash):
            user.password_hash = pwd_context.hash("AKIID12345")
            user.is_active = True
            db.commit()
    finally:
        db.close()
    yield


def test_production_environment_requires_all_credentials():
    with pytest.raises(RuntimeError, match="SECRET_KEY, DATABASE_URL, ADMIN_USERNAME"):
        require_production_environment({})


def test_production_environment_accepts_complete_configuration():
    environment = {
        "SECRET_KEY": "secret",
        "DATABASE_URL": "postgresql://user:password@host/database",
        "ADMIN_USERNAME": "Ridwan",
        "ADMIN_PASSWORD": "strong-admin-password",
        "OFFICER_USERNAME": "officer",
        "OFFICER_PASSWORD": "strong-officer-password",
    }
    require_production_environment(environment)


def test_production_environment_rejects_non_postgresql_database():
    environment = {
        "SECRET_KEY": "secret",
        "DATABASE_URL": "sqlite:///./database.db",
        "ADMIN_USERNAME": "Ridwan",
        "ADMIN_PASSWORD": "strong-admin-password",
        "OFFICER_USERNAME": "officer",
        "OFFICER_PASSWORD": "strong-officer-password",
    }
    with pytest.raises(RuntimeError, match="DATABASE_URL must use PostgreSQL"):
        require_production_environment(environment)


def test_migrate_legacy_sqlite_database(tmp_path):
    legacy_path = tmp_path / "diwaanka_ajaanibka.db"
    current_path = tmp_path / "migrasl_somaliland_migration_systems.db"
    with sqlite3.connect(legacy_path) as legacy_db:
        legacy_db.execute("CREATE TABLE migration_check (value TEXT)")
        legacy_db.execute("INSERT INTO migration_check VALUES ('preserved')")

    _migrate_legacy_sqlite_database(legacy_path, current_path)

    with sqlite3.connect(current_path) as current_db:
        row = current_db.execute("SELECT value FROM migration_check").fetchone()
    assert row == ("preserved",)
    assert legacy_path.exists()


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_login_success():
    response = client.post("/token", data={
        "username": "Ridwan",
        "password": "AKIID12345"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_fail():
    response = client.post("/token", data={
        "username": "wrong",
        "password": "wrong"
    })
    assert response.status_code == 401


def test_unauthorized_scan():
    response = client.post("/scan-face/")
    assert response.status_code == 401


def test_authorized_scan():
    login = client.post("/token", data={
        "username": "Ridwan",
        "password": "AKIID12345"
    })
    token = login.json()["access_token"]
    response = client.get("/stats/", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
