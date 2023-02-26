#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import sqlite3


def main():
    """Run administrative tasks."""
    if sys.argv[1] == "runserver":
        insert_defaults()
        run_django(sys.argv)
    elif sys.argv[1] == "dropdb":
        if os.path.isfile("db.sqlite3"):
            os.remove("db.sqlite3")
        # for migration in os.listdir(os.path.join('doctors', 'migrations')):
        #     if migration[:4].isdigit():
        # for migration in os.listdir(os.path.join('myuser', 'migrations')):
        #
        for f_name in os.listdir("."):
            if os.path.exists(os.path.join(".", f_name, "migrations")):
                for migration in os.listdir(os.path.join(f_name, "migrations")):
                    if migration[:4].isdigit():
                        os.remove(os.path.join(f_name, "migrations", migration))
        run_django([sys.argv[0], "makemigrations"])
        run_django([sys.argv[0], "migrate"])
        exit(0)
    else:
        run_django(sys.argv)


def run_django(args):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "med_service.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(args)


def get_database():
    return sqlite3.connect("db.sqlite3")


def create_query(table_name, fields, values):
    formated_values = [f'"{x}"' if isinstance(x, str) else str(x) for x in values]
    return f'INSERT OR IGNORE INTO {table_name} ({", ".join(fields)}) VALUES({", ".join(formated_values)})'


def insert_query(cursor, query):
    cursor.execute(query)
    return cursor.lastrowid


def insert_defaults():
    db = get_database()
    cursor = db.cursor()
    group_types = []
    rezus_types = []
    blood_type_id = 0
    for rezus_type in ("+", "-"):
        rezus_id = insert_query(
            cursor, create_query("myuser_bloodtyperezus", ["name"], [rezus_type])
        )
        if rezus_id != 0:
            rezus_types.append((rezus_id, rezus_type))
    for group_type in (1, 2, 3, 4):
        group_id = insert_query(
            cursor, create_query("myuser_bloodtypegroup", ["name"], [group_type])
        )
        if group_id != 0:
            group_types.append((group_id, group_type))

    for group_id, group_type in group_types:
        for rezus_id, resuz_type in rezus_types:
            blood_type_id += 1
            insert_query(
                cursor,
                create_query(
                    "myuser_bloodtype", ["group_id", "rezus_id"], [group_id, rezus_id]
                ),
            )

    for gender in ("Чоловік", "Жінка", "Не вказувати"):
        insert_query(cursor, create_query("myuser_gender", ["name"], [gender]))
    db.commit()
    db.close()


if __name__ == "__main__":
    main()
