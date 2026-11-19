import getpass
from database import init_db, get_db
from staff import StaffDB, pwd_context

init_db()
db = next(get_db())
username = input("Superadmin username: ").strip()
full_name = input("Magaca buuxa: ").strip()
password = getpass.getpass("Password (ugu yaraan 8 xaraf): ")
if len(password) < 8:
    raise SystemExit("Password-ku aad buu u gaaban yahay")
if db.query(StaffDB).filter(StaffDB.username == username).first():
    raise SystemExit("Username-kan hore ayuu u jiray")
db.add(StaffDB(username=username, full_name=full_name,
               password_hash=pwd_context.hash(password), role="superadmin"))
db.commit()
print("Superadmin waa la abuuray")
