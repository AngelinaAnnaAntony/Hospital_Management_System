import sqlite3
conn=sqlite3.connect("hospital.db")
cursor=conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS patient(p_id INTEGER PRIMARY KEY AUTOINCREMENT,
               p_name TEXT,age INTEGER,mail TEXT,gender TEXT,bgroup TEXT,allergy TEXT,
               med_condition TEXT,emg_name TEXT,emg_nmbr TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS doctor(d_id INTEGER PRIMARY KEY AUTOINCREMENT,
               d_name TEXT,age INTEGER,mail TEXT,gender TEXT,qualification TEXT,
               specialisation TEXT,dept TEXT,yoe INTEGER,fee INTEGER) ''')

cursor.execute('''CREATE TABLE IF NOT EXISTS appointment(a_id INTEGER PRIMARY KEY,p_id INTEGER,
               p_name TEXT,d_id INTEGER,doa DATE,mode TEXT,status TEXT,FOREIGN KEY(p_id)REFERENCES patient(p_id),
               FOREIGN KEY(d_id)REFERENCES doctor(d_id))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS prescription(pr_id INTEGER PRIMARY KEY,p_id INTEGER,
              ,d_id INTEGER,doa DATE,mode TEXT,status TEXT,FOREIGN KEY(p_id)REFERENCES patient(p_id),
               FOREIGN KEY(d_id)REFERENCES doctor(d_id))''')

conn.commit()
conn.close()