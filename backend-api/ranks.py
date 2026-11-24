"""Darajooyinka Ciidanka Qalabka Sida ee Somaliland (Milatariga, Booliska, Asluubta)."""
from typing import Optional

GROUPS = {
    "enlisted": "Askarta iyo Saraakiil-xigeenada",
    "officer": "Saraakiisha Hoose iyo Kuwa Dhexe",
    "general": "Saraakiisha Sare / Janannada",
}

# (level, code, Af-Soomaali, English, group)
_RAW = [
    (1, "dable", "Dable", "Private", "enlisted"),
    (2, "alifle", "Alifle", "Lance Corporal", "enlisted"),
    (3, "laba_alifle", "Laba-Alifle", "Corporal", "enlisted"),
    (4, "saddex_alifle", "Saddex-Alifle", "Sergeant", "enlisted"),
    (5, "xadhigle", "Xadhigle", "Warrant Officer Class 3", "enlisted"),
    (6, "laba_xadhigle", "Laba-Xadhigle", "Warrant Officer Class 2", "enlisted"),
    (7, "saddex_xadhigle", "Saddex-Xadhigle", "Warrant Officer Class 1", "enlisted"),
    (8, "musharax", "Musharax Sarkaal", "Chief Warrant Officer / Officer Cadet", "enlisted"),
    (9, "xiddigle", "Xiddigle", "Second Lieutenant", "officer"),
    (10, "laba_xiddigle", "Laba-Xiddigle", "First Lieutenant", "officer"),
    (11, "dhamme", "Dhamme (Saddex-Xiddigle)", "Captain", "officer"),
    (12, "gaashaanle", "Gaashaanle", "Major", "officer"),
    (13, "gaashaanle_dhexe", "Gaashaanle Dhexe", "Lieutenant Colonel", "officer"),
    (14, "gaashaanle_sare", "Gaashaanle Sare (Korneyl)", "Colonel", "officer"),
    (15, "sareeye_guuto", "Sareeye Guuto", "Brigadier General", "general"),
    (16, "sareeye_gaas", "Sareeye Gaas", "Major General", "general"),
    (17, "sareeye_guud", "Sareeye Guud", "Lieutenant General / General", "general"),
]

RANKS = [
    {"level": lvl, "code": code, "so": so, "en": en, "group": grp, "group_so": GROUPS[grp]}
    for (lvl, code, so, en, grp) in _RAW
]
RANK_BY_CODE = {r["code"]: r for r in RANKS}


def rank_level(code: Optional[str]) -> Optional[int]:
    r = RANK_BY_CODE.get(code or "")
    return r["level"] if r else None


def can_manage(actor_role: str, actor_rank: Optional[str], target_rank: Optional[str]) -> bool:
    """Superadmin wuu maamulaa qof walba. Kuwa kale waxay maamulaan kuwa darajadoodu hooseeyo oo keliya."""
    if actor_role == "superadmin":
        return True
    a, t = rank_level(actor_rank), rank_level(target_rank)
    if a is None or t is None:
        return False
    return a > t


def build_router(get_current_user):
    from fastapi import APIRouter, Depends
    router = APIRouter(tags=["ranks"])

    @router.get("/ranks/")
    def list_ranks(user: dict = Depends(get_current_user)):
        return {"status": "success", "total": len(RANKS), "ranks": RANKS}

    return router
