import psycopg2
DSN = "postgresql://postgres.ljvmdzjbrmodpmheugie:C7JjqMazeea49LQw@aws-1-us-west-1.pooler.supabase.com:6543/postgres"
conn = psycopg2.connect(DSN, connect_timeout=10)
cur = conn.cursor()

# Full column list for all public tables
cur.execute("""SELECT table_name, column_name, data_type FROM information_schema.columns
               WHERE table_schema='public' ORDER BY table_name, ordinal_position""")
last=None
for t,c,d in cur.fetchall():
    if t != last:
        print(f"\n-- {t} --")
        last=t
    print(f"  {c} ({d})")

# Dump small tables
for t in ("users","accounts","payments","transactions"):
    print(f"\n=== {t} ===")
    cur.execute(f"SELECT * FROM public.{t} ORDER BY 1")
    cols=[d.name for d in cur.description]
    print(" | ".join(cols))
    for row in cur.fetchall():
        print(row)

# Check auth.users for anything
print("\n=== auth.users ===")
cur.execute("SELECT id,email,raw_user_meta_data,raw_app_meta_data FROM auth.users LIMIT 30")
for row in cur.fetchall():
    print(row)

cur.close(); conn.close()
