from flask import Flask, render_template, request
app = Flask(__name__)
#home page
@app.route('/')
def home():
    return render_template('home.html')

#Patient login page
@app.route('/patient')
def patient():
    return render_template('patient_login.html')

#Patient login
@app.route('/patient_login')
def patient_login():
    email = request.args.get('email')
    password = request.args.get('password')
    return render_template('patient_dashboard.html')

#Doctor Login Page
@app.route('/doctor')
def doctor():
    return render_template('doctor_login.html')

#Doctor Login
@app.route('/doctor_login')
def doctor_login():
    email = request.args.get('email')
    password = request.args.get('password')

    return render_template('doctor_dashboard.html')

#Receptionist Login Page
@app.route('/receptionist')
def receptionist():
    return render_template('receptionist_login.html')

#Receptionist Login
@app.route('/receptionist_login')
def receptionist_login():
    email = request.args.get('email')
    password = request.args.get('password')
    return render_template('receptionist_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)