from flask import Flask, render_template, request, redirect
from database import get_connection,create_tables

app= Flask(__name__)

create_tables()
    
@app.route('/')
def admin():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM patients")
    total_patients = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM doctors")
    total_doctors = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointment")
    total_appointments = cursor.fetchone()[0]
    
    cursor.execute("SELECT COALESCE(SUM(amount),0) FROM billing")
    total_revenue = cursor.fetchone()[0]
    
    cursor.execute("SELECT * FROM appointment ORDER BY a_id DESC LIMIT 5")
    recent_appointments = cursor.fetchall()
    
    conn.close()
    
    return render_template("admin_dashboard.html",
                           total_patients=total_patients,
                           doctors=total_doctors,
                           appointments=total_appointments,
                           total_revenue=total_revenue,
                           recent_appointments=recent_appointments)

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

@app.route('/viewpatients')
def viewpatients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()
    conn.close()
    return render_template("admin.view_patients.html", patients=patients)

@app.route('/viewdoctors')
def viewdoctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    conn.close()
    return render_template("view_doc.html", doctors=doctors)

@app.route('/doctor', methods=['GET', 'POST'])
def doctor():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        gender = request.form['gender']
        qualification = request.form['qualification']
        experience = request.form['experience']
        specialization = request.form['specialization']
        department = request.form['department']
        consultation_fee = request.form['consultation_fee']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctors(name,age,email,gender,qualification,experience,specialization,department,consultation_fee) VALUES(?,?,?,?,?,?,?,?,?)",
                      (name,age,email,gender,qualification,experience,specialization,department,consultation_fee))
        conn.commit()
        conn.close()
        return render_template("add_doc.html")
    return render_template("add_doc.html")

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        p_id     = request.form['p_id']
        p_name   = request.form['p_name']
        d_id     = request.form['d_id']
        doa      = request.form['doa']
        mode     = request.form['mode']
        status   = request.form['status']
        phone    = request.form['phone']

        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO appointment (p_id, p_name, d_id, doa, mode, status, phone) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (p_id, p_name, d_id, doa, mode, status, phone)
                       )
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('admin.add_appointments.html')


@app.route('/viewappointments')
def viewappointments():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointment")
    appointments = cursor.fetchall()
    conn.close()
    return render_template('admin.view_appointments.html', appointments=appointments)

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        p_id   = request.form['p_id']
        amount = request.form['amount']

        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO billing (p_id, amount) VALUES (?, ?)",
            (p_id, amount)
        )
        conn.commit()
        conn.close()
        return redirect('/')

    return render_template('admin.bills.html')

@app.route('/viewbilling')
def viewbilling():
    conn   = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM billing")
    bills = cursor.fetchall()
    conn.close()
    return render_template('admin.view_bills.html', bills=bills)

if __name__== "__main__" :
    app.run(debug=True)
