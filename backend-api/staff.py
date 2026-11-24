from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import Base, get_db
from ranks import RANK_BY_CODE, can_manage

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ROLES = ("superadmin", "admin", "officer")


class StaffDB(Base):
    __tablename__ = "staff"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="officer")
    rank_code = Column(String, nullable=True)
    office = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    access_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class StaffIn(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2)
    role: str = "officer"
    rank_code: Optional[str] = None
    office: Optional[str] = None
    is_active: bool = True
    access_expires_at: Optional[datetime] = None


class StaffUpdate(BaseModel):
    password: Optional[str] = Field(default=None, min_length=8)
    full_name: Optional[str] = Field(default=None, min_length=2)
    role: Optional[str] = None
    rank_code: Optional[str] = None
    office: Optional[str] = None
    is_active: Optional[bool] = None
    access_expires_at: Optional[datetime] = None


def staff_to_dict(s: StaffDB) -> dict:
    return {
        "id": s.id,
        "username": s.username,
        "full_name": s.full_name,
        "role": s.role,
        "rank_code": s.rank_code,
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


def _actor(db: Session, user: dict) -> StaffDB:
    """Xuquuqda waxaa lagu xaqiijiyaa database-ka, ma aha token-ka oo keliya."""
    a = db.query(StaffDB).filter(StaffDB.username == user.get("username")).first()
    if not a or not a.is_active or a.role not in ("superadmin", "admin"):
        raise HTTPException(status_code=403, detail="Ma haysatid oggolaansho")
    return a


def _may_touch(actor: StaffDB, target: StaffDB) -> bool:
    """Superadmin wuu maamulaa qof walba. Admin wuxuu maamulaa officer darajadiisu hooseyso."""
    if actor.role == "superadmin":
        return True
    if target.role != "officer":
        return False
    return can_manage("admin", actor.rank_code, target.rank_code)


def _may_assign(actor: StaffDB, role: str, rank_code: Optional[str]) -> bool:
    """Admin ma dhigi karo officer darajo ka sarreysa ama ka siman tiisa."""
    if actor.role == "superadmin":
        return True
    if role != "officer":
        return False
    return can_manage("admin", actor.rank_code, rank_code)


def _check_rank_value(role: str, rank_code: Optional[str]):
    if rank_code is not None and rank_code not in RANK_BY_CODE:
        raise HTTPException(status_code=400, detail="Darajadan ma jirto")
    if role != "superadmin" and not rank_code:
        raise HTTPException(status_code=400, detail="Darajada waa loo baahan yahay")


def build_router(get_current_user):
    router = APIRouter(prefix="/staff", tags=["staff"])

    @router.get("/")
    def list_staff(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
        actor = _actor(db, user)
        q = db.query(StaffDB)
        if actor.role == "admin":
            q = q.filter(StaffDB.role == "officer")
        rows = []
        for s in q.order_by(StaffDB.id).all():
            d = staff_to_dict(s)
            d["can_manage"] = _may_touch(actor, s)
            rows.append(d)
        return rows

    @router.post("/")
    def create_staff(body: StaffIn, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
        actor = _actor(db, user)
        if body.role not in ROLES:
            raise HTTPException(status_code=400, detail="Door aan sax ahayn")
        if actor.role == "admin" and body.role != "officer":
            raise HTTPException(status_code=403, detail="Admin wuxuu abuuri karaa officer kaliya")
        _check_rank_value(body.role, body.rank_code)
        if not _may_assign(actor, body.role, body.rank_code):
            raise HTTPException(status_code=403, detail="Darajadan ma abuuri kartid")
        if db.query(StaffDB).filter(StaffDB.username == body.username).first():
            raise HTTPException(status_code=409, detail="Username-kan hore ayuu u jiray")
        s = StaffDB(
            username=body.username,
            full_name=body.full_name,
            password_hash=pwd_context.hash(body.password),
            role=body.role,
            rank_code=body.rank_code,
            office=body.office,
            is_active=body.is_active,
            access_expires_at=body.access_expires_at,
        )
        db.add(s)
        db.commit()
        db.refresh(s)
        return staff_to_dict(s)

    @router.put("/{staff_id}")
    def update_staff(staff_id: int, body: StaffUpdate, db: Session = Depends(get_db),
                     user: dict = Depends(get_current_user)):
        actor = _actor(db, user)
        s = db.query(StaffDB).filter(StaffDB.id == staff_id).first()
        if not s:
            raise HTTPException(status_code=404, detail="Lama helin")
        if not _may_touch(actor, s):
            raise HTTPException(status_code=403, detail="Qofkan ma maamuli kartid")

        data = body.model_dump(exclude_unset=True)
        if "role" in data and data["role"] not in ROLES:
            raise HTTPException(status_code=400, detail="Door aan sax ahayn")
        if "full_name" in data and not data["full_name"]:
            raise HTTPException(status_code=400, detail="Magaca buuxa waa loo baahan yahay")
        if "is_active" in data and data["is_active"] is False and s.id == actor.id:
            raise HTTPException(status_code=400, detail="Naftaada ma joojin kartid")

        new_role = data.get("role", s.role)
        new_rank = data["rank_code"] if "rank_code" in data else s.rank_code
        if "role" in data or "rank_code" in data:
            if actor.role == "admin" and new_role != "officer":
                raise HTTPException(status_code=403, detail="Admin wuxuu maareyn karaa officer kaliya")
            _check_rank_value(new_role, new_rank)
            if not _may_assign(actor, new_role, new_rank):
                raise HTTPException(status_code=403, detail="Darajadan ma dhigi kartid")

        if "password" in data and data["password"]:
            s.password_hash = pwd_context.hash(data["password"])
        if "role" in data:
            s.role = new_role
        if "rank_code" in data:
            s.rank_code = new_rank
        for field in ("full_name", "office", "is_active", "access_expires_at"):
            if field in data:
                setattr(s, field, data[field])
        db.commit()
        db.refresh(s)
        return staff_to_dict(s)

    @router.delete("/{staff_id}")
    def delete_staff(staff_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
        actor = _actor(db, user)
        s = db.query(StaffDB).filter(StaffDB.id == staff_id).first()
        if not s:
            raise HTTPException(status_code=404, detail="Lama helin")
        if s.id == actor.id:
            raise HTTPException(status_code=400, detail="Naftaada ma tirtiri kartid")
        if not _may_touch(actor, s):
            raise HTTPException(status_code=403, detail="Qofkan ma tirtiri kartid")
        db.delete(s)
        db.commit()
        return {"deleted": staff_id}

    return router
