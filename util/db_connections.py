import psycopg2
from psycopg2._psycopg import OperationalError


def create_connection():
    try:
        conn = psycopg2.connect(
            database='postgres',
            user='brian',
            password='',
            host='database-1.c44ijoqnzj79.us-east-2.rds.amazonaws.com',
            port='5432'
        )
        return conn
    except OperationalError as e:
        print(f"{e}")
        return conn


get_connected_for_free = create_connection()

