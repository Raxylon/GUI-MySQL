import mysql.connector
#import tkinter as tk

def verbindung_mysql(db_name=None):
    if db_name:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=db_name,
        )
    else:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
        )
def show_databases():
    while True:
        db = verbindung_mysql()  # Verbindung ohne Datenbank
        cursor = db.cursor()  # Cursor für Befehle erstellen
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()

        for index, database in enumerate(databases, start=1):
            print(index, database)
        auswahl = int(input("wähle die Nummer einer DB!\nBeende mit 0\n->"))
        if auswahl == 0:
            print("Auf wiedersehen...")
            return None, None, None

        elif 1 <= auswahl <= len(databases):
            db_name = databases[auswahl - 1][0]  # Hier greifst du die Datenbank richtig
            cursor.execute(f"USE {db_name}")
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()[0]
            print(current_db)

            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"{len(tables)} Tables")
            for index, table in enumerate(tables, start=1):
                print(f"{index}: {table}")
            return cursor, tables, db_name, db
        else:
            print("sry. fehler")
            return None, None, None

def show_tables(cursor, tables, db):
    if cursor is None or tables is None:
        return
    while True:
        auswahl_table = int(input("Zahl der Tabelle:\n0 Exit\n->"))
        if auswahl_table == 0:
            print("Auf wiedersehen...")
            break
        elif 1 <= auswahl_table <= len(tables):
            table_name = tables[auswahl_table - 1][0]
            cursor.execute(f"SELECT*FROM {table_name}")
            result = cursor.fetchall()

            spalten = cursor.column_names

            print(" | ".join(spalten))
            print("-" * (len(" | ".join(spalten)) + 10))

            for row in result:
                print(" | ".join(str(item) for item in row))

def main():
    cursor, tables, db_name, db = show_databases()
    show_tables(cursor, tables, db)
if __name__ == "__main__":
    main()
show_databases()