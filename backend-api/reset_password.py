import getpass
from database import init_db, get_db
from staff import StaffDB, pwd_context

init_db()
db = next(get_db())
username = input("Username (tusaale: Ridwan Farah): ").strip()
s = db.query(StaffDB).filter(StaffDB.username == username).first()
if not s:
    raise SystemExit("Username-kan lama helin")
pw = getpass.getpass("Password cusub (ugu yaraan 8 xaraf): ")
if len(pw) < 8:
    raise SystemExit("Password-ku aad buu u gaaban yahay")
s.password_hash = pwd_context.hash(pw)
s.is_active = True
db.commit()
print("Password-ka waa la beddelay")
