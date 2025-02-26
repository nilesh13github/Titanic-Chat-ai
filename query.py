import sqlite3
from query_fixer import fix_sql_spacing
# Connect to the SQLite database


def sqlite_query(query):
    try:
        conn = sqlite3.connect('titanic.db', check_same_thread=False)
        cur = conn.cursor()
        cur.execute(query)
        data = cur.fetchall()
        conn.close()
        print(data)
        return data, query
    except Exception as e :
        print(e)
        cf_msg = "error"
        return None,  cf_msg
#print(sqlite_query("SELECT COUNT(*) FROM Observation WHERE sex_id = 1, COUNT(*) FROM Observation WHERE sex_id = 0"))