
from .connection import get_connection
from .otp import generate_otp

def verify_user(login_type, identity, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if login_type == "email":

            query = """
                SELECT * FROM users
                WHERE email = %s AND password = %s
            """

        elif login_type == "contact":

            query = """
                SELECT * FROM users
                WHERE contact = %s AND password = %s
            """

        else:
            return None

        cursor.execute(query, (identity, password))

        user = cursor.fetchone()

        return user

    finally:
        cursor.close()
        conn.close()



def check_user_for_otp(login_type, identity):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        if login_type == 'email':
            query = "SELECT * FROM users WHERE email = %s"

        elif login_type == 'contact':
            query = "SELECT * FROM users WHERE contact = %s"

        else:
            return None

        cursor.execute(query, (identity,))
        user = cursor.fetchone()

        if user:
            otp = generate_otp()
            return otp

        return None

    finally:
        cursor.close()
        conn.close()