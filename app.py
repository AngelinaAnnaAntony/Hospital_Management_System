import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from database import get_connection,create_tables
app = Flask(__name__)
create_tables()
@app.route('/')
def home():
    return render_template("homepage.html")
#admin
@app.route('/admin')
def admin():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM doctor")
    total_doctors = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]
    
    cursor.execute("""SELECT SUM(cons_fee) + SUM(room) + SUM(medicine) +
    SUM(other) FROM billings """)

    total_revenue = cursor.fetchone()[0] or 0
    
    cursor.execute("""
    SELECT app_id, patient_name, department, doctor, date, mode
    FROM appointments LIMIT 5 """)

    recent_appointments = cursor.fetchall()
    
    
    
    conn.close()
    return render_template("admin_dashboard.html",total_patients=total_patients,
                           doctors=total_doctors,
                           appointments=total_appointments,
                            total_revenue=round(total_revenue,2),
                           recent_appointments=recent_appointments)
                        
@app.route('/add_bill')
def add_bill_page():
    return render_template('admin.bills.html')

@app.route('/add_bill', methods=['POST'])
def add_bill():

    p_id = request.form['p_id']
    app_id = request.form['app_id']
    bill_date = request.form['bill_date']
    cons_fee = request.form['cons_fee']
    room = request.form['room']
    medicine = request.form['medicine']
    other = request.form['other']

    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO billings
        (p_id, app_id, bill_date, cons_fee, room, medicine, other)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (p_id, app_id, bill_date, cons_fee, room, medicine, other))

    conn.commit()
    conn.close()

    return render_template('admin.bills.html', message="Bill added successfully!")

@app.route('/view_bill')
def view_bill():

    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM billings")
    bills = cursor.fetchall()

    conn.close()

    return render_template('admin.view_bills.html', bills=bills)

@app.route('/patient')
def patient():
    return render_template("admin.add_patients.html")

@app.route('/add_patient',methods=['GET','POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form["name"]
        age = request.form["age"]
        email = request.form["email"]
        gender = request.form["gender"]
        blood = request.form["blood_group"]
        allergy = request.form["allergies"]
        medical_conditions = request.form["medical_conditions"]
        emergency_name = request.form["emergency_name"]
        emergency_number = request.form["emergency_number"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO patients
            (
                name,age,email,gender,blood_group,allergies,medical_conditions,
                emergency_name,emergency_number
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            age,
            email,
            gender,
            blood,
            allergy,
            medical_conditions,
            emergency_name,
            emergency_number
        ))

        conn.commit()
        conn.close()

    return render_template("admin.add_patients.html")

@app.route('/viewpat')
def viewpat():
    return render_template("admin.view_patients.html")

@app.route('/viewpatients')
def viewpatients():
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("SELECT* FROM patients")
    patients=cursor.fetchall()
    conn.close()
    return render_template('admin.view_patients.html',patients=patients)

@app.route("/appointments")
def appointments():
    return render_template("admin.add_appointments.html")

@app.route("/add_appointments",methods=['GET','POST'])
def add_appointments():
    if request.method=='POST':
        name=request.form['name']
        phone=request.form['phone']
        department=request.form['department']
        doctor=request.form['doctor']
        date=request.form['date']
        time=request.form['time']
        symptoms=request.form['symptoms']
        mode=request.form['mode']
        
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''INSERT INTO appointments(patient_name,phone,department,doctor,date,time,symptoms,mode)VALUES(?,?,?,?,?,?,?,?)''',
                        (name,phone,department,doctor,date,time,symptoms,mode))

        conn.commit()
        conn.close()
        
    return render_template("admin.add_appointments.html")

@app.route('/viewappoints')
def viewappoints():
    return render_template("admin.view_appointments.html")

@app.route('/viewappointments')
def viewappointments():
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("SELECT* FROM appointments")
    appointments=cursor.fetchall()
    conn.close()
    return render_template('admin.view_appointments.html',appointments=appointments)
#doctor
@app.route('/doctor')
def doctor():
    return render_template('doctor/doctor_dashboard.html')

@app.route('/doc-view_appointments')
def drview_appointments():
    return render_template('doctor/doc-view_appointments.html')

@app.route('/doc-view_patients')
def drview_patients():
    return render_template('doctor/doc-view_patients.html')

@app.route('/doc-med_rec', methods=['GET', 'POST'])
def med_rec():
    if request.method == 'POST':
        patient = request.form['patient']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        conn = sqlite3.connect('hospital.db')
        cursor = conn.cursor()

        cursor.execute("""insert into diagnosis (patient, diagnosis, treatment) values (?, ?, ?)""", (patient, diagnosis, treatment))
        conn.commit()
        conn.close()
        return render_template('doctor/doc-med_rec.html')
    return render_template('doctor/doc-med_rec.html')

@app.route('/add_pres', methods=['GET','POST'])
def add_pres():
    if request.method == 'POST':
        patient = request.form['patient']
        medicine = request.form['medicine']
        dosage = request.form['dosage']
             
        conn= sqlite3.connect('hospital.db')
        cursor = conn.cursor()
        cursor.execute("""insert into prescriptions(name, medicine, dosage) values(?, ?, ?)""", (patient, medicine, dosage))
        conn.commit()
        conn.close()
        return render_template('doctor/add_pres.html',)
    return render_template('doctor/add_pres.html')

@app.route('/doc-view_profile')
def view_profile():
    return render_template('doctor/doc-view_profile.html')

@app.route('/drlogout')
def drlogout():
    return render_template('doctor/drlogout.html')

@app.route('/doctor_login')
def login():
    return render_template('doctor/doctor_login.html')

@app.route('/doctor_login', methods=['POST'])
def doctor_login():
    username = request.form['username']
    password = request.form['password']
    return render_template('doctor/doctor_dashboard.html')

@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('doctor/doctor_dashboard.html')

@app.route('/admin.add_doctor', methods=['GET','POST'])
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
        return render_template('admin.add_doctor.html',message="Doctor Registered Successfully")
    return render_template('admin.add_doctor.html')

@app.route('/view_doc')
def view_doc():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row   # allows column names
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctor")
    doctors= cursor.fetchall()
    conn.close()
    return render_template('admin.view_doctor.html', doctors=doctors)
#patient
@app.route('/patient_dashboard')
def patient_dashboard():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM prescriptions")
    total_prescriptions=cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM diagnosis")
    total_reports=cursor.fetchone()[0]
    conn.close()
    return render_template("patient_dashboard.html",
                           total_appointments=total_appointments,
                           total_prescriptions=total_prescriptions,
                           total_reports=total_reports)

@app.route('/patient_profile')
def patient_profile():
    return render_template("patient_profile.html")

@app.route('/patient_bookAppointment', methods=['GET','POST'])
def patient_bookAppointment():
    success=False
    if request.method=='POST':
        conn=get_connection()
        cursor=conn.cursor()
        
        cursor.execute("""
            INSERT INTO appointments
            (patient_name, phone, department, doctor, date, time, symptoms, mode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (request.form['patient_name'],
              request.form['phone'],
              request.form['department'],
              request.form['doctor'],
              request.form['date'],
              request.form['time'],
              request.form['symptoms'],
              request.form['mode']))
        conn.commit()
        conn.close()
        success=True
    return render_template("patient_bookAppointment.html",success=success)

@app.route('/patient_myAppointment')
def patient_myAppointment():
    conn=get_connection()
    cursor=conn.cursor()


    cursor.execute("SELECT * FROM appointments")
    appointments=cursor.fetchall()
    conn.close()
    return render_template("patient_myAppointment.html" , appointments=appointments)

@app.route('/delete_appointment/<int:id>')
def delete_appointment(id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE app_id=?",(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('patient_myAppointment'))

@app.route('/patient_prescription')
def patient_prescription():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
            SELECT 
                   pr_id,name,medicine,dosage FROM prescriptions
                   """)
    prescriptions=cursor.fetchall()
    conn.close()
    return render_template("patient_prescription.html",prescriptions=prescriptions)

@app.route('/patient_medicalReport')
def patient_medicalReport():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("""
            SELECT * FROM diagnosis
                   """)
    reports=cursor.fetchall()
    conn.close()
    return render_template("patient_medicalReport.html",reports=reports)

if __name__== '__main__':
    app.run(debug=True)
