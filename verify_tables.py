import sqlite3
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name NOT LIKE 'django_%' AND name NOT LIKE 'auth_%' AND name NOT LIKE 'admin_%' AND name NOT LIKE 'sessions_%' AND name NOT LIKE 'contenttypes_%'")
tables = [row[0] for row in cursor.fetchall()]
print('Application Tables Found:', len(tables))
for t in sorted(tables):
    print(f'  - {t}')
conn.close()