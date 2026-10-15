# MigraSL - Somaliland Migration Systems

Nidaam loogu talagalay diiwaangelinta ajaanibta, maamulka, xafiisyada, iyo ogaanshaha wejiyada ee Somaliland.

## Local development

This project targets Python 3.12. Use a Python 3.12 interpreter (for example, `python3.12`) for local development and CI. For local development and tests, install `backend-api/requirements-dev.txt` with `pip install -r backend-api/requirements-dev.txt`, then run `python app.py` from the repository root. This includes the backend runtime dependencies plus test-only packages (`httpx` and `pytest`). For deployment/runtime-only installs, use `pip install -r backend-api/requirements.txt`. Local development uses SQLite and the demo accounts `admin` / `admin123` and `officer` / `officer123`; do not use these credentials in production.

The backend requirements allow NumPy 2.x, letting pip select a release with a wheel for your Python version. NumPy 1.26.4 does not provide a wheel for Python 3.14, so pip may try to build it from source and require the MSVC C/C++ toolchain. Use the repository requirements rather than pinning NumPy to 1.26.4.

## Render deployment

Set `APP_ENV` to `production` and configure `SECRET_KEY`, `DATABASE_URL`, `ADMIN_USERNAME`, `ADMIN_PASSWORD`, `OFFICER_USERNAME`, and `OFFICER_PASSWORD` as private Render environment variables. Use a long, randomly generated JWT secret and strong, unique passwords. The service intentionally refuses to start in production if its secret, login credentials, or database URL are missing. `DATABASE_URL` must be a valid PostgreSQL URL without a Python-version prefix.

## Database rename

The local SQLite database now uses `migrasl_somaliland_migration_systems.db`. On startup, if that file does not exist but `diwaanka_ajaanibka.db` does, the backend copies the existing SQLite database to the new filename without deleting the original.

Docker Compose now uses the PostgreSQL database `migrasl_somaliland_migration_systems`. For an existing `postgres_data` volume, changing `POSTGRES_DB` does not rename the database already stored in the volume. Back up the old database, stop the backend, and rename it before starting the backend with the updated configuration:

```powershell
docker compose exec -T db pg_dump -U postgres -d diwaanka_ajaanibka > .\diwaanka_ajaanibka-backup.sql
docker compose stop backend
docker compose exec -T db psql -U postgres -d postgres -c "ALTER DATABASE diwaanka_ajaanibka RENAME TO migrasl_somaliland_migration_systems;"
docker compose up -d
```

For Render, keep using the private `DATABASE_URL` configured for the existing managed database. Change that URL only after migrating/renaming the database in Render; the repository cannot rename a managed database using the URL alone.
