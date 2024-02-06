from flask import Flask, request, render_template, redirect, url_for, flash
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

students = {}
hostels = {
    'male': {
        '100': 'Mark',
        '200': 'John',
        '300': random.choice(['Matthew', 'Luke']),
        '400': random.choice(['Nh', 'Extension']),
        '500': random.choice(['Extension', 'Nh'])
    },
    'female': {
        '100': random.choice(['Saddler', 'Upe', 'Block', '288']),
        '200': random.choice(['Saddler', 'Upe', 'Block', '288']),
        '300': random.choice(['Saddler', 'Upe', 'Block', '288']),
        '400': 'Nh',
        '500': 'Nh'
    }
}
rooms = {}


@app.route('/register', methods=['POST'])
def register_student():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm = request.form['confirm']

    if password != confirm:
        return 'Password and confirm password do not match'

    hashed_password = hash_password(password)

    student_id = len(students) + 1
    students[student_id] = {'name': name, 'email': email, 'password': hashed_password}

    return redirect(url_for('show_login_form'))


def hash_password(password):
    return password[::-1]


@app.route('/apply', methods=['POST'])
def apply_for_hostel():
    matric_number = request.form['matric_number']
    gender = request.form['gender']
    level = request.form['level']

    if gender in hostels and level in hostels[gender]:
        hostel = hostels[gender][level]
        room_number = random.randint(1, 60)
    else:
        return 'Invalid gender or level'

    rooms[matric_number] = {'hostel': hostel, 'room_number': room_number, 'level': level}

    return redirect(url_for('show_result', matric_number=matric_number))


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    for student_id, student in students.items():
        if student['name'] == username and student['password'] == hash_password(password):
            return redirect(url_for('show_apply_form'))

    flash('Invalid username or password', 'error')
    return redirect(url_for('show_login_form'))


@app.route('/rooms/<int:student_id>', methods=['GET'])
def view_rooms(student_id):
    student = students.get(student_id)
    if student:
        pass
    else:
        return 'Student not found'


@app.route('/register_form')
def show_registration_form():
    return render_template('register_form.html')


@app.route('/apply_form')
def show_apply_form():
    return render_template('apply_form.html')


@app.route('/login_form')
def show_login_form():
    return render_template('login_form.html')


@app.route('/result/<matric_number>')
def show_result(matric_number):
    room_info = rooms.get(matric_number)
    if room_info:
        return render_template('result.html', matric_number=matric_number, hostel=room_info['hostel'],
                               room_number=room_info['room_number'], level=room_info['level'])
    else:
        return 'Room information not found'


if __name__ == '__main__':
    app.run(debug=True)
