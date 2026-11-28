
from .connection import get_connection

def register_user(name, surname, email, contact, password):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT * FROM users
        WHERE email = %s OR contact = %s
    """
    cursor.execute(query, (email, contact))

    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        return ("Email or contact number already exists!")

    insert_query = """
        INSERT INTO users (name, surname, email, contact, password)
        VALUES (%s, %s, %s, %s, %s)
    """

    try:
        cursor.execute(insert_query, (name, surname, email, contact, password))
        conn.commit()

        

    except Exception as e:
        print("INSERT ERROR:", e)
        raise

    finally:
        cursor.close()
        conn.close() 
    return "Registration successful!"
