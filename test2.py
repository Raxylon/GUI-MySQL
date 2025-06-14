import mysql.connector

def get_databases_as_dict():
    # Verbindung ohne spezifische Datenbank, nur zum Auflisten
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost"
    )
    cursor = conn.cursor()

    cursor.execute("SHOW DATABASES")
    databases = cursor.fetchall()  # Ergebnis: Liste von Tupeln [('information_schema',), ('mysql',), ...]

    # Erstelle ein Dictionary mit Zahlen als Schlüssel und Datenbanknamen als Wert
    db_dict = {str(i+1): db[0] for i, db in enumerate(databases)}

    cursor.close()
    conn.close()

    return db_dict

# Beispiel Nutzung:
dbs = get_databases_as_dict()
print(dbs)
# Ausgabe z.B.: {'1': 'information_schema', '2': 'mysql', '3': 'test', ...}
