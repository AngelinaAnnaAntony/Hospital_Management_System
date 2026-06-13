from flask import Flask,render_template,request,redirect,url_for
app=Flask(__name__)

@app.route('/')
def login():
    return render_template("patient_login.html")

@app.route('/check_login',methods=['POST'])
def check_login():
    email=request.form['email']
    password=request.form['password']

    if email and password:
        return redirect(url_for('dashboard'))
    return "Invalid Login"

@app.route('/dashboard')
def dashboard():
    return render_template("patient_dashboard.html")

@app.route('/profile')
def profile():
    return render_template("patient_profile.html")

@app.route('/bookappointment')
def bookappointment():
    return render_template("patient_bookAppointment.html")

@app.route('/myappointment')
def myappointment():
    return render_template("patient_myAppointment.html")

@app.route('/prescription')
def prescription():
    return render_template("patient_prescription.html")

@app.route('/medicalrecord')
def medicalrecord():
    return render_template("patient_medicalReport.html")

if __name__ == '__main__':
    app.run(debug=True)