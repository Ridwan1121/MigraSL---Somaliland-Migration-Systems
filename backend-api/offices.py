from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session

from database import Base, get_db

KINDS = ("office", "embassy", "border")


class OfficeDB(Base):
    __tablename__ = "offices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    city = Column(String, nullable=True)
    kind = Column(String, nullable=False, default="office")
    is_active = Column(Boolean, default=True)


class OfficeIn(BaseModel):
    name: str = Field(min_length=2)
    country: str = Field(min_length=2)
    city: Optional[str] = None
    kind: str = "office"
    is_active: bool = True


class OfficeUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    kind: Optional[str] = None
    is_active: Optional[bool] = None


def office_to_dict(o: OfficeDB) -> dict:
    return {"id": o.id, "name": o.name, "country": o.country,
            "city": o.city, "kind": o.kind, "is_active": o.is_active}


def build_router(get_current_user):
    router = APIRouter(prefix="/offices", tags=["offices"])

    def manager(user: dict = Depends(get_current_user)):
        if user.get("role") not in ("superadmin", "admin"):
            raise HTTPException(status_code=403, detail="Ma haysatid oggolaansho")
        return user

    def superadmin_only(user: dict = Depends(get_current_user)):
        if user.get("role") != "superadmin":
            raise HTTPException(status_code=403, detail="Superadmin keliya ayaa tirtiri kara")
        return user

    def check_kind(kind: str):
        if kind not in KINDS:
            raise HTTPException(status_code=400, detail="Nooca xafiiska waa khaldan")

    @router.get("/")
    def list_offices(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
        return [office_to_dict(o) for o in db.query(OfficeDB).order_by(OfficeDB.country, OfficeDB.name).all()]

    @router.post("/")
    def create_office(body: OfficeIn, db: Session = Depends(get_db), user: dict = Depends(manager)):
        check_kind(body.kind)
        o = OfficeDB(**body.model_dump())
        db.add(o)
        db.commit()
        db.refresh(o)
        return office_to_dict(o)

    @router.put("/{office_id}")
    def update_office(office_id: int, body: OfficeUpdate, db: Session = Depends(get_db), user: dict = Depends(manager)):
        o = db.query(OfficeDB).filter(OfficeDB.id == office_id).first()
        if not o:
            raise HTTPException(status_code=404, detail="Lama helin")
        data = body.model_dump(exclude_unset=True)
        if "kind" in data:
            check_kind(data["kind"])
        for k, v in data.items():
            setattr(o, k, v)
        db.commit()
        db.refresh(o)
        return office_to_dict(o)

    @router.delete("/{office_id}")
    def delete_office(office_id: int, db: Session = Depends(get_db), user: dict = Depends(superadmin_only)):
        o = db.query(OfficeDB).filter(OfficeDB.id == office_id).first()
        if not o:
            raise HTTPException(status_code=404, detail="Lama helin")
        db.delete(o)
        db.commit()
        return {"deleted": office_id}

    return router
