import database

COLUMNS = {
    "visit_reason": "VARCHAR(30)",
    "visit_reason_details": "VARCHAR(300)",
}


def run():
    """Ku dar columns-ka cusub immigrants table-ka haddii uu hore u jiray (SQLite iyo PostgreSQL)."""
    from sqlalchemy import inspect, text
    engine = getattr(database, "engine", None)
    if engine is None:
        print("migrations: engine lama helin, waa la ordi waayay")
        return
    insp = inspect(engine)
    if "immigrants" not in insp.get_table_names():
        return
    existing = {c["name"] for c in insp.get_columns("immigrants")}
    with engine.begin() as conn:
        for name, ddl in COLUMNS.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE immigrants ADD COLUMN {name} {ddl}"))
                print(f"migrations: {name} waa lagu daray immigrants")
