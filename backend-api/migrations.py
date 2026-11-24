"""Column-ka cusub ku dar table-yada jira (SQLite iyo PostgreSQL). Server-ku marka uu bilowdo ayuu socdaa."""
import database

TABLES = {
    "immigrants": {
        "visit_reason": "VARCHAR(30)",
        "visit_reason_details": "VARCHAR(300)",
    },
    "staff": {
        "rank_code": "VARCHAR(30)",
    },
}


def run():
    from sqlalchemy import inspect, text
    engine = getattr(database, "engine", None)
    if engine is None:
        print("migrations: engine lama helin, waa la ordi waayay")
        return
    insp = inspect(engine)
    existing_tables = set(insp.get_table_names())
    with engine.begin() as conn:
        for table, columns in TABLES.items():
            if table not in existing_tables:
                continue
            existing = {c["name"] for c in insp.get_columns(table)}
            for name, ddl in columns.items():
                if name not in existing:
                    conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"))
                    print(f"migrations: {table}.{name} waa lagu daray")
