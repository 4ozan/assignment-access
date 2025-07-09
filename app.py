from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Hospital Management System Users
USERS = {
    "admin": ("adminpass", "admin"),
    "doctor": ("doctorpass", "doctor"),
    "nurse": ("nursepass", "nurse"),
    "receptionist": ("receptionistpass", "receptionist"),
    "guest": ("guestpass", "guest")
}

# Hospital Role-Based Permissions
ROLE_PERMISSIONS = {
    "admin": [
        "Can add/remove hospital staff",
        "Can view all patient records",
        "Can manage system settings",
        "Can generate hospital reports",
        "Can access financial data"
    ],
    "doctor": [
        "Can view/edit patient medical records",
        "Can create treatment plans",
        "Can access medical history",
        "Can prescribe medications",
        "Can schedule surgeries"
    ],
    "nurse": [
        "Can view patient care records",
        "Can update medication logs",
        "Can access basic patient info",
        "Can manage care schedules",
        "Can monitor vital signs"
    ],
    "receptionist": [
        "Can register new patients",
        "Can manage appointments",
        "Can access basic patient info",
        "Can update contact details",
        "Can process insurance forms"
    ],
    "guest": [
        "Can view public hospital information",
        "Can access hospital directory",
        "Can view visiting hours",
        "Can access emergency contact info"
    ]
}

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        selected_role = request.form.get('role')
        user = USERS.get(username)
        if user and user[0] == password and user[1] == selected_role:
            session['role'] = user[1]
            return redirect(url_for(f"{user[1]}_page"))
        else:
            message = "Access denied! Please check your credentials."
    return render_template('login.html', message=message)

@app.route('/admin')
def admin_page():
    if session.get('role') == 'admin':
        return render_template('admin.html', permissions=ROLE_PERMISSIONS['admin'])
    return redirect(url_for('login'))

@app.route('/doctor')
def doctor_page():
    if session.get('role') == 'doctor':
        return render_template('doctor.html', permissions=ROLE_PERMISSIONS['doctor'])
    return redirect(url_for('login'))

@app.route('/nurse')
def nurse_page():
    if session.get('role') == 'nurse':
        return render_template('nurse.html', permissions=ROLE_PERMISSIONS['nurse'])
    return redirect(url_for('login'))

@app.route('/receptionist')
def receptionist_page():
    if session.get('role') == 'receptionist':
        return render_template('receptionist.html', permissions=ROLE_PERMISSIONS['receptionist'])
    return redirect(url_for('login'))

@app.route('/guest')
def guest_page():
    if session.get('role') == 'guest':
        return render_template('guest.html', permissions=ROLE_PERMISSIONS['guest'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True) 