import mysql.connector as mysql

from config import DATABASE, HOST, PASSWORD, USER
from src.tables import TABLES


def create_tables():
    my_connection = mysql.connect(
        host=HOST, user=USER,
        password=PASSWORD, database=DATABASE)
    cursor = my_connection.cursor()
    for table_name in TABLES:
        cursor.execute(TABLES[table_name])
    my_connection.close()


def existing_tables():
    my_connection = mysql.connect(
        host=HOST, user=USER,
        password=PASSWORD, database=DATABASE)
    cursor = my_connection.cursor()
    cursor.execute("SHOW TABLES;")
    existing = list(map(lambda x: x[0], cursor.fetchall()))
    my_connection.close()
    return existing


def drop_tables():
    DROPING_queue = ["Finance", "Equipment", "Brooms", "Handwear", "Headwear",
                     "Footwear", "Pants", "PersonalInfo", "Salaries", "Managment",
                     "Sponsors", "Ends", "Matches", "Players", "Coaches", "Teams", "Leagues"]
    my_connection = mysql.connect(
        host=HOST, user=USER,
        password=PASSWORD, database=DATABASE)
    cursor = my_connection.cursor()
    existing = existing_tables()
    DROPING_queue = [table_name for table_name in DROPING_queue if table_name in existing]
    for table_name in DROPING_queue:
        cursor.execute(f"DROP TABLE {table_name};")
    my_connection.close()
