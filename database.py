import sqlite3
def get_connection():
    con= sqlite3.connect("hospital.db")
    con.row_factory = sqlite3.Row
    return con

def create_tables():
    con= get_connection()
    cursor = con.cursor()
    cursor.execute("""create table if not exists doctor(d_id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,
               age INTEGER,email TEXT,gender TEXT,qualification TEXT,experience INTEGER,specialization TEXT,
    department TEXT,cons_fee REAL)""")
    cursor.execute('''CREATE TABLE IF NOT EXISTS prescriptions(pr_id INTEGER PRIMARY KEY,p_id INTEGER
              ,d_id INTEGER,name TEXT,medicine TEXT,dosage INTEGER,FOREIGN KEY(p_id)REFERENCES patient(p_id),
               FOREIGN KEY(d_id)REFERENCES doctor(d_id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS diagnosis(p_id INTEGER PRIMARY KEY,
                patient TEXT,diagnosis TEXT, treatment TEXT,FOREIGN KEY(p_id)REFERENCES patient(p_id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients(p_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT,age INTEGER,email TEXT,gender TEXT,blood_group TEXT,allergies TEXT,
                medical_conditions TEXT,emergency_name TEXT,emergency_number TEXT)''')

    con.commit()
    con.close()