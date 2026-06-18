import sqlite3

def get_connection():
    conn=sqlite3.connect("hospital.db")
    conn.row_factory=sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS patients(p_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, email TEXT, gender TEXT, blood_group TEXT, allergies TEXT, medical_conditions TEXT, emergency_name TEXT, emergency_number TEXT)")

    cursor.execute("CREATE TABLE IF NOT EXISTS doctors(d_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, email TEXT, gender TEXT, qualification TEXT, experience TEXT, specialization TEXT, department TEXT, consultation_fee TEXT)")

    cursor.execute("CREATE TABLE IF NOT EXISTS billing(b_id INTEGER PRIMARY KEY AUTOINCREMENT, p_id INTEGER, amount REAL)")

    cursor.execute("CREATE TABLE IF NOT EXISTS appointment(a_id INTEGER PRIMARY KEY AUTOINCREMENT, p_id INTEGER, p_name TEXT, d_id INTEGER, doa DATE, mode TEXT, status TEXT, phone INTEGER)")

    conn.commit()
    conn.close()
