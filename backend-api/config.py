"""Application environment configuration and production validation."""
from collections.abc import Mapping
import os


PRODUCTION_ENVIRONMENT_VARIABLES = (
    "SECRET_KEY",
    "DATABASE_URL",
    "ADMIN_USERNAME",
    "ADMIN_PASSWORD",
    "OFFICER_USERNAME",
    "OFFICER_PASSWORD",
)


def require_production_environment(environment: Mapping[str, str]) -> None:
    missing = [
        name for name in PRODUCTION_ENVIRONMENT_VARIABLES
        if not environment.get(name, "").strip()
    ]
    if missing:
        raise RuntimeError(
            "Missing required production environment variables: "
            + ", ".join(missing)
        )

    database_url = environment["DATABASE_URL"].strip()
    postgresql_prefixes = (
        "postgres://",
        "postgresql://",
        "postgresql+psycopg://",
        "postgresql+psycopg2://",
    )
    if not database_url.startswith(postgresql_prefixes):
        raise RuntimeError("DATABASE_URL must use PostgreSQL in production.")


APP_ENV = os.getenv("APP_ENV", "development")
if APP_ENV.lower() == "production":
    require_production_environment(os.environ)
    SECRET_KEY = os.environ["SECRET_KEY"]
else:
    SECRET_KEY = os.getenv("SECRET_KEY", "migrasl-secret-key-2026-very-secure")
