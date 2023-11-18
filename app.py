import psycopg2

db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'wakweli',  
    'user': 'cem',
    'password': 'mega'  
}

try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

except Exception as e:
    print(f"Error: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()