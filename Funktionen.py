import mysql.connector
import tkinter as tk
from tkinter import messagebox


def verbindung_aufbauen():
    return mysql.connector.connect(
        user='root',
        password='',
        host='localhost'
        # keine Datenbank angeben, um frei wählen zu können
    )


conn = verbindung_aufbauen()


def show_databases():
    cursor1 = conn.cursor()
    cursor1.execute("SHOW DATABASES")

    print("\n📚 Verfügbare Datenbanken:")
    for (db,) in cursor1:
        print(f"– {db}")

    cursor1.close()


def show_tables():
    db_name = input("\nWelche Datenbank willst du nutzen?\n-> ")
    cursor2 = conn.cursor()

    try:
        cursor2.execute(f"USE `{db_name}`")
        cursor2.execute("SHOW TABLES")

        print(f"\n📂 Tabellen in {db_name}:")
        for (table,) in cursor2:
            print(f"– {table}")
    except mysql.connector.Error as err:
        print(f"Fehler: {err}")
    finally:
        cursor2.close()


# Ablauf:
show_databases()
show_tables()

# Verbindung erst ganz am Ende schließen
conn.close()
