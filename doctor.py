from flask import Flask, render_template,request,url_for
app = Flask(__name__)
@app.route('/')
def home():
    return render_template('doctor/doctor_dashboard.html')

@app.route('/view_appointments')
def view_appointments():
    return render_template('doctor/view_appointments.html')

@app.route('/view_patients')
def view_patients():
    return render_template('doctor/view_patients.html')

@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    if request.method == 'POST':
        patient = request.form['patient']
        diagnosis = request.form['diagnosis']
        treatment = request.form['treatment']
        return render_template('diagnosis.html',patient=patient, diagnosis=diagnosis, treatment=treatment)
    return render_template('doctor/diagnosis.html')

@app.route('/add_pres', methods=['GET','POST'])
def add_pres():
    if request.method == 'POST':
        patient = request.form['patient']
        medicine = request.form['medicine']
        dosage = request.form['dosage']
        return render_template( 'doctor/add_pres.html',patient=patient,medicine=medicine,dosage=dosage)
    return render_template('doctor/add_pres.html')

@app.route('/view_profile')
def view_profile():
    return render_template('doctor/view_profile.html')

@app.route('/logout')
def logout():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)