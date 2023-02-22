#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'med_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


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
    for rezus_type in ('+', '-'):
        rezus_id = insert_query(cursor, create_query("doctors_bloodtyperezus", ['name'], [rezus_type]))
        rezus_types.append((rezus_id, rezus_type))
    for group_type in (1, 2, 3, 4):
        group_id = insert_query(cursor, create_query("doctors_bloodtypegroup", ['name'], [group_type]))
        rezus_types.append((group_id, group_type))

    for group_id, group_type in group_types:
        for rezus_id, resuz_type in rezus_types:
            blood_type_id += 1
            insert_query(
                cursor, create_query("doctors_bloodtype", ['id'], [blood_type_id])
            )
            insert_query(
                cursor,
                create_query("doctors_bloodtype_group", ['bloodtype_id', 'group_id'], [blood_type_id, group_id])
            )
            insert_query(
                cursor,
                create_query("doctors_bloodtype_group", ['bloodtype_id', 'rezus_id'], [blood_type_id, rezus_id])
            )

    for gender in ('Чоловік', 'Жінка', 'Не вказувати'):
        insert_query(cursor, create_query("myuser_gender", ['name'], [gender]))
    db.commit()
    db.close()


if __name__ == '__main__':
    main()
