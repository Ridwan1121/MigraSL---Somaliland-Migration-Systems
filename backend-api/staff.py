from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import Base, get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ROLES = ("superadmin", "admin", "officer")


class StaffDB(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="officer")
    office = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    access_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class StaffIn(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)
    full_name: str
    role: str = "officer"
    office: Optional[str] = None
    is_active: bool = True
    access_expires_at: Optional[datetime] = None


class StaffUpdate(BaseModel):
    password: Optional[str] = Field(default=None, min_length=8)
    full_name: Optional[str] = None
    role: Optional[str] = None
    office: Optional[str] = None
    is_active: Optional[bool] = None
    access_expires_at: Optional[datetime] = None


def staff_to_dict(s: StaffDB) -> dict:
    return {
        "id": s.id,
        "username": s.username,
        "full_name": s.full_name,
        "role": s.role,
        "office": s.office,
        "is_active": s.is_active,
        "access_expires_at": s.access_expires_at.isoformat() if s.access_expires_at else None,
    }


def authenticate_staff(db: Session, username: str, password: str):
    """Soo celi dict-ka user-ka haddii login-ku sax yahay, haddii kale None."""
    s = db.query(StaffDB).filter(StaffDB.username == username).first()
    if not s or not s.is_active:
        return None
    if not pwd_context.verify(password, s.password_hash):
        return None
    if s.role == "officer" and s.access_expires_at and s.access_expires_at < datetime.utcnow():
        return None
    return staff_to_dict(s)


def build_router(get_current_user):
    router = APIRouter(prefix="/staff", tags=["staff"])

    def manager(user: dict = Depends(get_current_user)):
        if user.get("role") not in ("superadmin", "admin"):
            raise HTTPException(status_code=403, detail="Ma haysatid oggolaansho")
        return user

    def check_role(user: dict, role: str):
        if role not in ROLES:
            raise HTTPException(status_code=400, detail="Door aan sax ahayn")
        if user["role"] == "admin" and role != "officer":
            raise HTTPException(status_code=403, detail="Admin wuxuu maareyn karaa officer kaliya")

    @router.get("/")
    def list_staff(db: Session = Depends(get_db), user: dict = Depends(manager)):
        q = db.query(StaffDB)
        if user["role"] == "admin":
            q = q.filter(StaffDB.role == "officer")
        return [staff_to_dict(s) for s in q.order_by(StaffDB.id).all()]

    @router.post("/")
    def create_staff(body: StaffIn, db: Session = Depends(get_db), user: dict = Depends(manager)):
        check_role(user, body.role)
        if db.query(StaffDB).filter(StaffDB.username == body.username).first():
            raise HTTPException(status_code=409, detail="Username-kan hore ayuu u jiray")
        s = StaffDB(
            username=body.username,
            full_name=body.full_name,
            password_hash=pwd_context.hash(body.password),
            role=body.role,
            office=body.office,
            is_active=body.is_active,
            access_expires_at=body.access_expires_at,
        )
        db.add(s)
        db.commit()
        db.refresh(s)
        return staff_to_dict(s)

    @router.put("/{staff_id}")
    def update_staff(staff_id: int, body: StaffUpdate, db: Session = Depends(get_db), user: dict = Depends(manager)):
        s = db.query(StaffDB).filter(StaffDB.id == staff_id).first()
        if not s:
            raise HTTPException(status_code=404, detail="Lama helin")
        check_role(user, s.role)
        data = body.model_dump(exclude_unset=True)
        if "role" in data:
            check_role(user, data["role"])
            s.role = data["role"]
        if "password" in data and data["password"]:
            s.password_hash = pwd_context.hash(data["password"])
        for field in ("full_name", "office", "is_active", "access_expires_at"):
            if field in data:
                setattr(s, field, data[field])
        db.commit()
        db.refresh(s)
        return staff_to_dict(s)

    @router.delete("/{staff_id}")
    def delete_staff(staff_id: int, db: Session = Depends(get_db), user: dict = Depends(manager)):
        s = db.query(StaffDB).filter(StaffDB.id == staff_id).first()
        if not s:
            raise HTTPException(status_code=404, detail="Lama helin")
        if s.username == user.get("username"):
            raise HTTPException(status_code=400, detail="Naftaada ma tirtiri kartid")
        check_role(user, s.role)
        db.delete(s)
        db.commit()
        return {"deleted": staff_id}

    return router
