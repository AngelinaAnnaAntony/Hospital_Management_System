import sqlite3
from flask import Flask, render_template,request,url_for
from database import get_connection,create_tables
app = Flask(__name__)
create_tables()
@app.route('/')
def home():
    return render_template('doctor/doctor_dashboard.html')

@app.route('/doc-view_appointments')
def view_appointments():
    return render_template('doctor/doc-view_appointments.html')

@app.route('/doc-view_patients')
def view_patients():
    return render_template('doctor/doc-view_patients.html')

@app.route('/doc-med_rec', methods=['GET', 'POST'])
def med_rec():
    if request.method == 'POST':
        patient = request.form['patient']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        con = sqlite3.connect('hospital.db')
        cursor = con.cursor()

        cursor.execute("""insert into diagnosis (patient, diagnosis, treatment) values (?, ?, ?)""", (patient, diagnosis, treatment))
        con.commit()
        con.close()
        return render_template('doctor/doc-med_rec.html')
    return render_template('doctor/doc-med_rec.html')

@app.route('/add_pres', methods=['GET','POST'])
def add_pres():
    if request.method == 'POST':
        patient = request.form['patient']
        medicine = request.form['medicine']
        dosage = request.form['dosage']
        
        con= sqlite3.connect('hospital.db')
        cursor = con.cursor()
        cursor.execute("""insert into prescriptions(patient, medicine, dosage) values(?, ?, ?)""", (patient, medicine, dosage))
        con.commit()
        con.close()
        return render_template('doctor/add_pres.html',)
    return render_template('doctor/add_pres.html')

@app.route('/doc-view_profile')
def view_profile():
    return render_template('doctor/doc-view_profile.html')

@app.route('/logout')
def logout():
    return render_template('doctor/logout.html')
@app.route('/doctor')
def doctor():
    return render_template('doctor_login.html')

#Doctor Login
@app.route('/doctor_login',methods=['POST'])
def doctor_login():
    username = request.args('username')
    password = request.args('password')
    return render_template('doctor/doctor_dashboard.html')

@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('doctor/doctor_dashboard.html')

@app.route('/add_doc', methods=['GET','POST'])
def add_doc():
    if request.method=='POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        gender = request.form['gender']
        qualification = request.form['qualification']
        experience = request.form['experience']
        specialization = request.form['specialization']
        department = request.form['department']
        cons_fee = request.form['cons_fee']
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("""insert into doctor(name,age,email,gender,qualification,experience,specialization,department,cons_fee)
        values(?,?,?,?,?,?,?,?,?)""", (name,age,email,gender,qualification,experience,specialization,department, cons_fee))
        conn.commit()
        conn.close()
        return render_template('add_doc.html',message="Doctor Registered Successfully")
    return render_template('add_doc.html')
@app.route('/view_doc')
def view_doc():
    con = sqlite3.connect('hospital.db')
    con.row_factory = sqlite3.Row   
    cursor = con.cursor()
    cursor.execute("SELECT * FROM doctor")
    doctors= cursor.fetchall()
    con.close()
    return render_template('view_doc.html', doctors=doctors)

if __name__== '__main__':
    app.run(debug=True)
