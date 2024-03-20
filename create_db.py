import sqlite3

def create_tables() -> sqlite3.Connection:
    """
    Create necessary database tables for the application.
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            slug TEXT NOT NULL
        )
        '''
    )
    
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        '''
    )

    conn.commit()
    return conn

if __name__ == '__main__':
    create_tables()
