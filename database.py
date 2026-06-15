import sqlite3

def get_connection():
    conn=sqlite3.connect("hospital.db")
    conn.row_factory=sqlite3.Row
    return conn

def create_tables():
    
    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS patients(p_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,age INTEGER,email TEXT
                ,gender TEXT,blood_group TEXT,allergies TEXT,
                medical_conditions TEXT,emergency_name TEXT,emergency_number TEXT)''')

    # cursor.execute('''CREATE TABLE IF NOT EXISTS appointment(a_id INTEGER PRIMARY KEY,p_id INTEGER,
    #                p_name TEXT,d_id INTEGER,doa DATE,mode TEXT,status TEXT,FOREIGN KEY(p_id)REFERENCES patient(p_id),
    #                FOREIGN KEY(d_id)REFERENCES doctor(d_id))''')


    conn.commit()
    conn.close()
