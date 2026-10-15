# MigraSL - Somaliland Migration Systems

MigraSL - Somaliland Migration Systems waa nidaam loogu talagalay diiwaangelinta dadka ajaanibta ah, maamulka socdaalka iyo xafiisyada, iyo aqoonsiga wejiyada ee Somaliland.

## Local development

This project targets Python 3.12. Use a Python 3.12 interpreter (for example, `python3.12`) for local development and CI. For local development and tests, install `backend-api/requirements-dev.txt` with `pip install -r backend-api/requirements-dev.txt`, then run `python app.py` from the repository root. This includes the backend runtime dependencies plus test-only packages (`httpx2` and `pytest`). For deployment/runtime-only installs, use `pip install -r backend-api/requirements.txt`. Local development uses SQLite and the demo accounts `Ridwan` / `AKIID12345` and `officer` / `officer123`; do not use these credentials in production.

The backend requirements allow NumPy 2.x, letting pip select a release with a wheel for your Python version. NumPy 1.26.4 does not provide a wheel for Python 3.14, so pip may try to build it from source and require the MSVC C/C++ toolchain. Use the repository requirements rather than pinning NumPy to 1.26.4.

## Render deployment

The included `render.yaml` sets `APP_ENV=production`. In the Render dashboard, configure `SECRET_KEY`, `DATABASE_URL`, `ADMIN_PASSWORD`, and `OFFICER_PASSWORD` as private environment variables; `ADMIN_USERNAME` and `OFFICER_USERNAME` are set to `Ridwan` and `officer` by `render.yaml` and can be overridden in the dashboard. Use a long, randomly generated JWT secret and strong, unique passwords. The service refuses to start in production if any required value is missing or blank, and production login accounts are built from these environment variables rather than the local demo credentials. The administrator and officer usernames must differ. `DATABASE_URL` must be a valid PostgreSQL URL.

The current Render service name in `render.yaml` is still `diwaanka-ajaanibka`; this deployment name is separate from the MigraSL branding shown in the application.

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
