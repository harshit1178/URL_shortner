import sqlite3

DB_NAME="urls.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    #connection to database

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            click_count INTEGER DEFAULT 0
        )
        ''')
    #creation of urls table

    conn.commit()
    conn.close()

def save_url(short_code,original_url):
    conn=sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Insertion code and long URL into the table
    cursor.execute('''
    INSERT INTO urls (short_code, original_url) 
    VALUES (?, ?)
    ''', (short_code, original_url))

    conn.commit()
    conn.close()

def get_original_url(short_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Searching for the long URL using the short code
    cursor.execute('SELECT original_url FROM urls WHERE short_code = ?', (short_code,))
    row = cursor.fetchone()

    conn.close()

    # Returning the URL string, otherwise return None
    if row:
        return row[0]
    return None

def increment_click(short_code):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Add +1 to click_count for this specific short code
    cursor.execute('''
        UPDATE urls 
        SET click_count = click_count + 1 
        WHERE short_code = ?
    ''', (short_code,))
    
    conn.commit()
    conn.close()

def check_duplicate_url(original_url):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT short_code FROM urls WHERE original_url = ?', (original_url,))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else None

def get_all_urls():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # B. Ask for all rows ordered by the most clicks first
    cursor.execute('SELECT short_code, original_url, click_count FROM urls ORDER BY click_count DESC')
    rows = cursor.fetchall()

    conn.close()

    return rows

        
