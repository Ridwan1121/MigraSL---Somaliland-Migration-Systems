import os
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session

from database import Base, get_db, ImmigrantDB
from offices import OfficeDB
from staff import StaffDB

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
MAX_BYTES = 5 * 1024 * 1024
EXT = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}

PERMISSIONS = {
    "superadmin": {
        "manage_admins": True, "manage_officers": True, "manage_offices": True,
        "delete_immigrants": True, "register_immigrants": True, "scan_faces": True,
        "delete_photos": True, "view_senior_admin": True,
    },
    "admin": {
        "manage_admins": False, "manage_officers": True, "manage_offices": True,
        "delete_immigrants": True, "register_immigrants": True, "scan_faces": True,
        "delete_photos": True, "view_senior_admin": True,
    },
    "officer": {
        "manage_admins": False, "manage_officers": False, "manage_offices": False,
        "delete_immigrants": False, "register_immigrants": True, "scan_faces": True,
        "delete_photos": False, "view_senior_admin": False,
    },
}


class PhotoDB(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, index=True)
    immigrant_id = Column(Integer, index=True, nullable=False)
    filename = Column(String, nullable=False)
    uploaded_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def _looks_like_image(data: bytes) -> bool:
    return (
        data[:3] == b"\xff\xd8\xff"
        or data[:8] == b"\x89PNG\r\n\x1a\n"
        or (data[:4] == b"RIFF" and data[8:12] == b"WEBP")
    )


def build_router(get_current_user):
    router = APIRouter(tags=["extras"])

    def manager(user: dict = Depends(get_current_user)):
        if user.get("role") not in ("superadmin", "admin"):
            raise HTTPException(status_code=403, detail="Ma haysatid oggolaansho")
        return user

    @router.get("/dashboard/summary")
    def summary(db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
        role = user.get("role")
        counts = {
            "immigrants": db.query(ImmigrantDB).count(),
            "offices": db.query(OfficeDB).count(),
            "photos": db.query(PhotoDB).count(),
        }
        if role == "superadmin":
            counts["staff"] = db.query(StaffDB).count()
        elif role == "admin":
            counts["staff"] = db.query(StaffDB).filter(StaffDB.role == "officer").count()
        return {
            "user": {
                "username": user.get("username"),
                "full_name": user.get("full_name"),
                "role": role,
                "office": user.get("office"),
                "access_expires_at": user.get("access_expires_at"),
            },
            "permissions": PERMISSIONS.get(role, {}),
            "counts": counts,
        }

    @router.post("/photos/{immigrant_id}")
    async def upload_photo(immigrant_id: int, file: UploadFile = File(...),
                           db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
        ext = EXT.get(file.content_type or "")
        if not ext:
            raise HTTPException(status_code=400, detail="Sawirka waa inuu noqdaa JPG, PNG ama WEBP")
        data = await file.read()
        if len(data) > MAX_BYTES:
            raise HTTPException(status_code=413, detail="Sawirku waa weyn yahay (ugu badnaan 5MB)")
        if not _looks_like_image(data):
            raise HTTPException(status_code=400, detail="Faylku ma aha sawir sax ah")
        if not db.query(ImmigrantDB).filter(ImmigrantDB.id == immigrant_id).first():
            raise HTTPException(status_code=404, detail="Ajaanib lama helin")
        filename = f"{immigrant_id}_{uuid.uuid4().hex}{ext}"
        with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
            f.write(data)
        p = PhotoDB(immigrant_id=immigrant_id, filename=filename, uploaded_by=user.get("username"))
        db.add(p)
        db.commit()
        db.refresh(p)
        return {"id": p.id, "immigrant_id": immigrant_id, "url": f"/photos/file/{p.id}"}

    @router.get("/photos/{immigrant_id}")
    def list_photos(immigrant_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
        rows = db.query(PhotoDB).filter(PhotoDB.immigrant_id == immigrant_id).order_by(PhotoDB.id.desc()).all()
        return [{"id": p.id, "url": f"/photos/file/{p.id}",
                 "created_at": p.created_at.isoformat() if p.created_at else None} for p in rows]

    @router.get("/photos/file/{photo_id}")
    def get_photo_file(photo_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
        p = db.query(PhotoDB).filter(PhotoDB.id == photo_id).first()
        if not p:
            raise HTTPException(status_code=404, detail="Sawir lama helin")
        path = os.path.join(UPLOAD_DIR, p.filename)
        if not os.path.isfile(path):
            raise HTTPException(status_code=404, detail="Faylka sawirka ma jiro")
        return FileResponse(path)

    @router.delete("/photos/{photo_id}")
    def delete_photo(photo_id: int, db: Session = Depends(get_db), user: dict = Depends(manager)):
        p = db.query(PhotoDB).filter(PhotoDB.id == photo_id).first()
        if not p:
            raise HTTPException(status_code=404, detail="Sawir lama helin")
        path = os.path.join(UPLOAD_DIR, p.filename)
        if os.path.isfile(path):
            os.remove(path)
        db.delete(p)
        db.commit()
        return {"deleted": photo_id}

    return router
