from flask import Flask,render_template,request
from database import get_connection,create_tables

app= Flask(__name__)

create_tables()

@app.route('/')
def admin():
    return render_template("admin.html")

@app.route('/patient')
def patient():
    return render_template("add_pat.html")

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

    return render_template("add_pat.html")

@app.route('/viewpat')
def viewpat():
    return render_template("view_pat.html")

@app.route('/viewpatients')
def viewpatients():
    conn=get_connection()
    cursor=conn.cursor()
    
    cursor.execute("SELECT* FROM patients")
    patients=cursor.fetchall()
    conn.close()
    return render_template('view_pat.html',patients=patients)

if __name__== "__main__" :
    app.run(debug=True)
