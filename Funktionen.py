import mysql.connector  # Importiere das MySQL-Connector-Modul für die DB-Verbindung
import tkinter as tk    # Importiere tkinter, falls GUI nötig ist (hier nur vorbereitet)

# Funktion: Verbindung zur MySQL-Datenbank herstellen
def verbindung_mysql(db_name=None):
    """
    Baut eine Verbindung zur MySQL-Datenbank auf.
    Wenn db_name angegeben, wird die Verbindung auf diese DB gesetzt.
    """
    if db_name:
        # Verbindung mit spezifischer Datenbank
        return mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
            database=db_name
        )
    else:
        # Verbindung ohne Datenbank (z.B. für SHOW DATABASES)
        return mysql.connector.connect(
            user="root",
            password="",
            host="localhost",
        )

# Funktion: Datenbanken anzeigen
def show_database():
    db, cursor = conn()         # Verbindung ohne DB herstellen
    cursor.execute("SHOW DATABASES")  # MySQL-Befehl: Alle Datenbanken anzeigen
    databases = cursor.fetchall()      # Alle Ergebnisse holen
    for index, database in enumerate(databases, start=1):  # Nummeriert die DBs
        print(index, database)

# Funktion: Verbindung und Cursor holen
def conn():
    db = verbindung_mysql()     # Verbindung ohne Datenbank
    cursor = db.cursor()        # Cursor für Befehle erstellen
    return db, cursor

# Funktion: Datenbank auswählen und Verbindung herstellen
def select_database(db_name=None):
    db_dict = {"1": "information_schema", "2": "kfz_walter", "3": "klausurvorbereitung",
               "4": "mysql", "5": "performance_schema", "6": 'phpmyadmin',
               "7": 'schulvertretung', "8": 'test'}
    # Liste der verfügbaren DBs mit Nummern anzeigen
    for key, value in db_dict.items():
        print(f"{key} : {value}")
    auswahl = input("Zahl der DB eingeben:\n->")  # Benutzer wählt DB
    if auswahl in db_dict:
        db_name = db_dict[auswahl]
        db = verbindung_mysql(db_name)    # Verbindung zur gewählten DB
        cursor = db.cursor()
        cursor.execute(f"USE {db_name}")  # Setzt aktive DB (meistens optional)
        print(f"{db_name} wurde gewählt.")
        return db, cursor
    else:
        print("Ungültige Auswahl.")
        return None

# Funktion: Zeigt alle Tabellen in der aktuellen DB an und gibt Name zurück
def show_tables(cursor):
    cursor.execute("SHOW TABLES")   # MySQL-Befehl für Tabellenliste
    tables = cursor.fetchall()
    if not tables:
        print("Keine Tabellen gefunden.")
        return None
    print("\nTabellen in der Datenbank:")
    for idx, table in enumerate(tables, start=1):
        print(f"{idx}: {table[0]}")
    table_name = input("Name der Tabelle wählen:\n->")
    return table_name

# Funktion: Zeigt Inhalte der ausgewählten Tabelle an
def show_table_content(cursor, table_name):
    try:
        cursor.execute(f"SELECT * FROM {table_name}")  # Alle Daten aus Tabelle holen
        rows = cursor.fetchall()
        if not rows:
            print("Keine Daten in der Tabelle.")
            return
        for row in rows:
            print(row)   # Ausgabe jeder Zeile
    except mysql.connector.Error as err:
        print(f"Fehler beim Abrufen: {err}")

# Funktion: Daten in Tabelle einfügen
def insert_into_table(cursor, db):
    print("\nDaten Einfügen - Werte eingeben.")
    table_name = input("In welche Tabelle willst du einfügen? (0 zum Zurück):\n-> ")
    if table_name == "0":
        return

    try:
        cursor.execute(f"SHOW COLUMNS FROM {table_name}")  # Spalteninformationen holen
        columns = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
        return

    # Spalten, die nicht auto_increment sind, werden ausgefüllt
    columns_to_fill = [col[0] for col in columns if "auto_increment" not in col[5]]

    values = []
    for col in columns_to_fill:
        val = input(f"Wert für '{col}': ")
        values.append(val)

    placeholders = ", ".join(["%s"] * len(values))  # Platzhalter für SQL
    columns_joined = ", ".join(columns_to_fill)

    sql = f"INSERT INTO {table_name} ({columns_joined}) VALUES ({placeholders})"

    try:
        cursor.execute(sql, values)  # Daten einfügen
        db.commit()                  # Änderungen speichern
        print("Eintrag erfolgreich eingefügt.")
    except mysql.connector.Error as err:
        print(f"Fehler beim Einfügen: {err}")

# Funktion: Daten aus Tabelle löschen
def delete_from_table(cursor, db):
    print("\nDaten Löschen - Bedingung eingeben.")
    table_name = input("Aus welcher Tabelle willst du löschen? (0 zum Zurück):\n-> ")
    if table_name == "0":
        return

    condition = input("Bedingung für DELETE (z.B. id=5) (0 zum Zurück):\n-> ")
    if condition == "0" or condition.strip() == "":
        return

    sql = f"DELETE FROM {table_name} WHERE {condition}"
    confirm = input(f"Bist du sicher? ({sql}) [j/n]: ")
    if confirm.lower() == "j":
        try:
            cursor.execute(sql)
            db.commit()
            print("Löschung erfolgreich.")
        except mysql.connector.Error as err:
            print(f"Fehler beim Löschen: {err}")
    else:
        print("Löschvorgang abgebrochen.")

# Hauptmenü und Steuerung
def main():
    while True:
        db_cursor = select_database()
        if db_cursor is None:
            print("Programm beendet.")
            break
        db, cursor = db_cursor

        while True:
            print("\nMenü:")
            print("1: Tabellen anzeigen und Daten ansehen")
            print("2: Daten einfügen")
            print("3: Daten löschen")
            print("0: Zurück zur Datenbank-Auswahl")
            auswahl = input("Wähle eine Option:\n-> ")

            if auswahl == "0":
                break
            elif auswahl == "1":
                table_name = show_tables(cursor)
                if table_name:
                    show_table_content(cursor, table_name)
            elif auswahl == "2":
                insert_into_table(cursor, db)
            elif auswahl == "3":
                delete_from_table(cursor, db)
            else:
                print("Ungültige Eingabe. Versuch es erneut.")

if __name__ == "__main__":
    main()
