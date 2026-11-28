from .connection import get_connection

def create_user_table():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            contact VARCHAR(15) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    """

    cursor.execute(query)
    conn.commit()

    cursor.close()
    conn.close()

    print('User table created successfully!')

if __name__ == "__main__":
    create_user_table()