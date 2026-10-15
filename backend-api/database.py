"""
MigraSL---Somaliland-Migration-Systems - Database (SQLite local + PostgreSQL production)
"""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from pathlib import Path
import sqlite3
import os


def _migrate_legacy_sqlite_database(legacy_path: Path, current_path: Path) -> None:
    if legacy_path.is_file() and not current_path.exists():
        with sqlite3.connect(legacy_path) as source_db:
            with sqlite3.connect(current_path) as target_db:
                source_db.backup(target_db)
        print(f"SQLite database waa loo raray: {current_path.name}")


# Database URL (PostgreSQL production ama SQLite local)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    legacy_db_path = Path.cwd() / "diwaanka_ajaanibka.db"
    current_db_path = Path.cwd() / "migrasl_somaliland_migration_systems.db"
    _migrate_legacy_sqlite_database(legacy_db_path, current_db_path)

    DATABASE_URL = "sqlite:///./migrasl_somaliland_migration_systems.db"
    print("DATABASE_URL lama helin - SQLite ayaa la isticmaalayaa")
else:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    print("DATABASE_URL waa la helay")

# SQLite wuxuu u baahan yahay connect_args
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# ============================================================
# MODELS
# ============================================================
class ImmigrantDB(Base):
    __tablename__ = "immigrants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    region = Column(String)
    entry_point = Column(String)
    district = Column(String)
    passport = Column(String, nullable=True)
    status = Column(String, default="registered")
    face_encoding = Column(Text, nullable=True)
    registered_at = Column(DateTime, default=datetime.utcnow)


class OfficerDB(Base):
    __tablename__ = "officers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    office = Column(String)
    border = Column(String)
    country = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class AdminDB(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    role = Column(String)
    office = Column(String)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.utcnow)


class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    role = Column(String, default="officer")
    disabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScanHistoryDB(Base):
    __tablename__ = "scan_history"
    id = Column(Integer, primary_key=True, index=True)
    faces_detected = Column(Integer)
    scan_type = Column(String)
    scanned_by = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


# ============================================================
# INIT
# ============================================================
def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
