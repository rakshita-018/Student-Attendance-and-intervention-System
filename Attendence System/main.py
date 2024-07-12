from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector as msql
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

app = Flask(_name_)

# Database connection
con = msql.connect(
    host='localhost',
    user='root',
    passwd='beebase',
    database='attendance_db',
    charset='utf8'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        grade_level = request.form['grade_level']
        school_id = int(request.form['school_id'])

        qry = 'INSERT INTO students (first_name, last_name, date_of_birth, grade_level, school_id) VALUES (%s, %s, %s, %s, %s)'
        val = (first_name, last_name, date_of_birth, grade_level, school_id)
        mcursor = con.cursor()
        mcursor.execute(qry, val)
        con.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/add_teacher', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        subject = request.form['subject']
        school_id = int(request.form['school_id'])

        qry = 'INSERT INTO teachers (first_name, last_name, subject, school_id) VALUES (%s, %s, %s, %s)'
        val = (first_name, last_name, subject, school_id)
        mcursor = con.cursor()
        mcursor.execute(qry, val)
        con.commit()
        return redirect(url_for('index'))
    return render_template('add_teacher.html')

@app.route('/add_counselor', methods=['GET', 'POST'])
def add_counselor():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        contact_info = request.form['contact_info']
        school_id = int(request.form['school_id'])

        qry = 'INSERT INTO counselors (first_name, last_name, contact_info, school_id) VALUES (%s, %s, %s, %s)'
        val = (first_name, last_name, contact_info, school_id)
        mcursor = con.cursor()
        mcursor.execute(qry, val)
        con.commit()
        return redirect(url_for('index'))
    return render_template('add_counselor.html')

@app.route('/add_school', methods=['GET', 'POST'])
def add_school():
    if request.method == 'POST':
        school_name = request.form['school_name']
        school_address = request.form['school_address']

        qry = 'INSERT INTO schools (school_name, address) VALUES (%s, %s)'
        val = (school_name, school_address)
        mcursor = con.cursor()
        mcursor.execute(qry, val)
        con.commit()
        return redirect(url_for('index'))
    return render_template('add_school.html')

@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    if request.method == 'POST':
        class_name = request.form['class_name']
        teacher_id = int(request.form['teacher_id'])
        school_id = int(request.form['school_id'])

        qry = 'INSERT INTO classes (class_name, teacher_id, school_id) VALUES (%s, %s, %s)'
        val = (class_name, teacher_id, school_id)
        mcursor = con.cursor()
        mcursor.execute(qry, val)
        con.commit()
        return redirect(url_for('index'))
    return render_template('add_class.html')

@app.route('/add_attendance', methods=['GET', 'POST'])
def add_attendance():
    if request.method == 'POST':
        student_id = int(request.form['student_id'])
        class_id = int(request.form['class_id'])
        attendance_date = request.form['attendance_date']
        status = request.form['status']

        qry = 'INSERT INTO attendance (student_id, class_id, attendance_date, status) VALUES (%s, %s, %s, %s)'
        val = (student_id, class_id, attendance_date, status)
        mcursor = con.cursor()
        mcursor.execute(qry, val)
        con.commit()

        if status.lower() == 'absent':
            send_absence_alert(student_id)
        
        return redirect(url_for('index'))
    return render_template('add_attendance.html')

def send_absence_alert(student_id):
    qry = '''
        SELECT guardians.guardian_email, guardians.parent_type, students.first_name, students.last_name
        FROM guardians 
        JOIN students ON guardians.student_id = students.student_id 
        WHERE students.student_id = %s
    '''
    mcursor = con.cursor()
    mcursor.execute(qry, (student_id,))
    results = mcursor.fetchall()

    for result in results:
        guardian_email, parent_type, first_name, last_name = result
        send_email(
            guardian_email,
            'Absence Alert Notification',
            f'Dear {parent_type},\n\nYour child, {first_name} {last_name}, was marked absent today.\n\nRegards,\nSchool Administration'
        )
        print(f'Absence alert email sent to {guardian_email}')

def send_email(to_email, subject, body):
    from_email = 'xyzxyza6969@gmail.com'
    from_password = 'kekh xfij ktye zhpb'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

if _name_ == '_main_':
    app.run(debug=True)