from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERS = {
    "admin": ("adminpass", "admin"),
    "staff": ("staffpass", "staff"),
    "guest": ("guestpass", "guest")
}

ROLE_PERMISSIONS = {
    "admin": [
        "Can add/remove users",
        "Can view/edit/delete all records",
        "Can change system settings"
    ],
    "staff": [
        "Can view/edit/delete all records"
    ],
    "guest": [
        "Can view all records"
    ]
}

@app.route('/', methods=['GET', 'POST'])
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
            message = "Access denied! Contact Admin."
    return render_template('login.html', message=message)

@app.route('/admin')
def admin_page():
    if session.get('role') == 'admin':
        return render_template('admin.html', permissions=ROLE_PERMISSIONS['admin'])
    return redirect(url_for('login'))

@app.route('/staff')
def staff_page():
    if session.get('role') == 'staff':
        return render_template('staff.html', permissions=ROLE_PERMISSIONS['staff'])
    return redirect(url_for('login'))

@app.route('/guest')
def guest_page():
    if session.get('role') == 'guest':
        return render_template('guest.html', permissions=ROLE_PERMISSIONS['guest'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 