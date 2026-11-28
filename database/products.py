from .connection import get_connection



def get_products():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        query = "SELECT id, name, category, image FROM products"
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]

        products = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

        return products

    finally:
        cursor.close()
        conn.close()

