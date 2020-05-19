"""
TODO: for the sake of clean code we need to do the following:
1. rename all variables into meaningful names
2. remove all unused variables
3. remove all print() functions
4. add comments for each function
5. rename all confirm and error msgs, and check its spelling & grammer
6. I notice the database connections are in every function, why not to have one? and close it at the end of the function?
7. combine all css files together as well as js files. same applied to HTML pages
8. why there is a logos folder? it is better to store them in database
"""
import os
import random
import sqlite3
import pdfkit
from flask import Flask, render_template, redirect, url_for, request, session
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename

app = Flask(__name__)
mail = Mail(app)
if __name__ == '__main__':
    app.run()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'static/logos/'
app.secret_key = 'workshop'
app.config['SESSION_TYPE'] = 'null'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = '@gmail.com'
app.config['MAIL_PASSWORD'] = '*******'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# TODO: why local?
WKHTMLTOPDF_PATH = 'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'


@app.route('/tem')
def tem():
    return render_template('Organizer/template.html')


# Organizer activity details page
@app.route('/cer/<id>', methods=["GET", "POST"])
def v_cert(id):
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    conn = sqlite3.connect("CCSITWorkshop.DB")
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM certificates where Activity='" + id + "'")
    return render_template('Organizer/generatedPdf.html', rows=result)


def generate_pdf(html, static_path, _path):
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    PDF = pdfkit.from_string(html, os.path.join(static_path, _path),
                             # TODO: why more than one css file?
                             css=['static/Organizer/assets/css/smoothproducts.css',
                                  'static/Organizer/assets/css/progress-bars.css',
                                  'static/Organizer/assets/bootstrap/css/bootstrap.min.css'],
                             configuration=config,
                             options={'encoding': "UTF-8", 'custom-header': [('Accept-Encoding', 'gzip')],
                                      'disable-smart-shrinking': '',
                                      'page-size': 'Letter', 'orientation': 'landscape', 'no-outline': None})
    return True


# Organizer activity details page
@app.route('/de/<id>', methods=["GET", "POST"])
def v_detail(id):
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    if request.method == "POST":
        if 'edit' in request.form:
            print(request.form['edit'])
            return redirect(url_for('update', id=request.form['edit']))
        elif 'attendence' in request.form:
            print(request.form['attendence'])
            return redirect(url_for('attendence', id=request.form['attendence']))
        else:
            conn = sqlite3.connect("CCSITWorkshop.DB")
            cursor4 = conn.cursor()
            cursor4.execute(" SELECT Title,ID,WDate FROM Workshops where ID ='" + id + "'")
            result4 = cursor4.fetchall()
            print(result4[0][0])
            cursor5 = conn.cursor()
            cursor5.execute("SELECT Name, ID FROM Student INNER JOIN registration ON registration.S_ID = Student.ID where W_ID='" + id + "' And attend= 1;")
            rows2 = cursor5.fetchall()
            if cursor5 != 0:
                for row in rows2:
                    cursor6 = conn.cursor()
                    # w_id,s_id,pdf
                    cursor6.execute('INSERT INTO certificates VALUES (?,?,?)', (result4[0][1], row[1], str(result4[0][1]) + str(row[1]) + ".pdf"))
                    conn.commit()
                    print(str(result4[0][1]) + str(row[1]) + ".pdf")
                    print((result4[0][2].split("T"))[0])
                    print((result4[0][2].split("T"))[1])
                    html = render_template('Organizer/template.html', name=row[0], workshop=result4[0][0], date=(result4[0][2].split("T"))[0], time=(result4[0][2].split("T"))[1])
                    static_path = "static/"
                    file_path = "PDF/" + str(result4[0][1]) + str(row[1]) + ".pdf"
                    generate_pdf(html, static_path, file_path)
                cursor7 = conn.cursor()
                cursor7.execute(" UPDATE Workshops SET flag= 1 WHERE ID = '" + id + "';")
                conn.commit()
                return redirect(url_for('v_cert', id=id))
            else:
                conn = sqlite3.connect("CCSITWorkshop.DB")
                # TODO: why so many cursors?
                cursor = conn.cursor()
                cursor1 = conn.cursor()
                cursor2 = conn.cursor()
                cursor3 = conn.cursor()
                # TODO: u can use the code like this, to avoid unused variables
                # result = cursor.execute("SELECT * FROM Workshops where ID='" + id + "'").fetchall()
                result = cursor.execute("SELECT * FROM Workshops where ID='" + id + "'")
                result = cursor.fetchall()
                seat = result[0][4]
                print(seat)
                result1 = cursor1.execute("SELECT W_ID, COUNT(*) FROM registration where  W_ID='" + id + "' GROUP BY W_ID  ;")
                result1 = cursor1.fetchall()
                print(result1)
                if result1:
                    reg = result1[0][1]
                    print(reg)
                    avaReal = (seat - reg)
                    avaround = (round((avaReal / seat), 1) * 100)
                    print(avaround)
                else:
                    ava = 0
                cursor2.execute("SELECT W_ID, COUNT(*) FROM registration where attend= 1 AND W_ID='" + id + "' GROUP BY W_ID  ;")
                result2 = cursor2.fetchall()
                if result2:
                    Attend = result2[0][1]
                    print(Attend)
                else:
                    Attend = 0
                    cursor3.execute("SELECT W_ID, COUNT(*) FROM registration where attend= 0 AND W_ID='" + id + "' GROUP BY W_ID  ;")
                if cursor3 != 0:
                    result0 = cursor3.fetchall()
                    if result0:
                        Absent = result0[0][1]
                        print(Absent)
                    else:
                        Absent = 0
                return render_template('Organizer/activity-details.html', rows=result, Attend=Attend, Absent=Absent, ava=avaReal, reg=reg, avaround=avaround)
    conn = sqlite3.connect("CCSITWorkshop.DB")
    cursor = conn.cursor()
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    result = cursor.execute(" SELECT * FROM Workshops where ID ='" + id + "'")
    result = cursor.fetchall()
    seat = result[0][4]
    print(seat)
    cursor1.execute("SELECT W_ID, COUNT(*) FROM  registration  where  W_ID ='" + id + "' GROUP BY W_ID  ;")
    result1 = cursor1.fetchone()
    print(result1)
    # TODO: repalce it '!=' with 'is not'
    if result1 != None:
        reg = result1[1]
        print(reg)
        avaReal = (seat - reg)
        avaround = (round((avaReal / seat), 1) * 100)
        print(avaround)
    else:
        reg = 1
        avaReal = seat
        avaround = 100
    cursor2.execute("SELECT W_ID, COUNT(*) FROM registration where attend = 1 AND W_ID='" + id + "' GROUP BY W_ID;")
    result2 = cursor2.fetchone()
    if result2 != None:
        Attend = result2[1]
        print(Attend)
    else:
        Attend = 0
    cursor3.execute("SELECT W_ID, COUNT(*) FROM registration where attend = 0 AND W_ID='" + id + "' GROUP BY W_ID;")
    result0 = cursor3.fetchone()
    print(result0)
    if result0 != None:
        Absent = result0[1]
        print(Absent)
    else:
        Absent = 0
    return render_template('Organizer/activity-details.html', rows=result, Attend=Attend, Absent=Absent, ava=avaReal, reg=reg, avaround=avaround)


# user cert
@app.route('/cert', methods=["GET", "POST"])
def u_cert():
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    id = session['username']
    conn = sqlite3.connect("CCSITWorkshop.DB")
    cursor3 = conn.cursor()
    result3 = cursor3.execute("SELECT * FROM Workshops INNER JOIN  certificates ON certificates.Activity= Workshops.ID where S_ID ='" + id + "';")
    return render_template('users/certificate.html', rows=result3)


# activity enroll user
@app.route('/activityenroll', methods=["GET", "POST"])
def activityenroll():
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    id = session['username']
    if request.method == "POST":
        if 'unenroll' in request.form:
            Wid = request.form['unenroll']
            conn = sqlite3.connect("CCSITWorkshop.DB")
            cursor = conn.cursor()
            cursor.execute('DELETE FROM registration WHERE W_ID=? AND S_ID=?', (Wid, id))
            conn.commit()
            return redirect(url_for('activityenroll'))
    conn = sqlite3.connect("CCSITWorkshop.DB")
    cursor3 = conn.cursor()
    result3 = cursor3.execute("SELECT * FROM Workshops INNER JOIN registration ON registration.W_ID = Workshops.ID where S_ID ='" + id + "';")
    return render_template('users/activity-enrolled.html', rows=result3)


# user activity details page
@app.route('/ded/<id>', methods=["GET", "POST"])
def uv_detail(id):
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    user = session['username']
    if request.method == "POST":
        idsession = session['username']
        if 'enroll' in request.form:
            conn = sqlite3.connect("CCSITWorkshop.DB")
            cursor = conn.cursor()
            cursor.execute('INSERT INTO registration VALUES (?,?,?,?)', (None, idsession, id, 0))
            conn.commit()
            print(request.form['enroll'])
            return redirect(url_for('activityenroll'))
    idsession = session['username']
    conn = sqlite3.connect("CCSITWorkshop.DB")
    cursor1 = conn.cursor()
    cursor2 = conn.cursor()
    cursor3 = conn.cursor()
    result = cursor1.execute(" SELECT * FROM Workshops where ID ='" + id + "'")
    cursor2.execute(" SELECT * FROM registration where W_ID ='" + id + "' AND S_ID='" + idsession + "'")
    result2 = cursor2.fetchall()
    cursor3.execute("SELECT W_ID, COUNT(*) FROM  registration  where  W_ID ='" + id + "' GROUP BY W_ID  ;")
    result3 = cursor3.fetchone()
    if result3 != None:
        reg = result3[1]
        print(reg)
    else:
        reg = 0
    conn.commit()
    print(len(result2))
    if len(result2) > 0:
        result2 = "enroll"
    else:
        result2 = "unenroll"
    return render_template('users/activity-details.html', rows=result, check=result2, reg=reg)


# user home
@app.route('/UHome', methods=["GET", "POST"])
def UHome():
    if session['logged_in'] == False:  return redirect(url_for('login'))
    user = session['username']
    con = sqlite3.connect('CCSITWorkshop.DB')
    cursor = con.cursor()
    cursor1 = con.cursor()
    cursor.execute(" SELECT * FROM Workshops ")
    result = cursor.fetchall()
    reg = [0]
    ava = [0]
    avaP = [0]
    for row in result:
        cursor1.execute("SELECT W_ID, COUNT(*) FROM  registration  where  W_ID ='" + str(row[0]) + "' GROUP BY W_ID  ;")
        result1 = cursor1.fetchall()
        if result1:
            reg.append(result1[0][1])
            ava.append(row[4] - result1[0][1])
            avaP.append(round(((row[4] - result1[0][1]) / row[4]), 1) * 100)
        else:
            reg.append(0)
            ava.append(row[4])
            avaP.append(100)
        print(row[4])
    print(reg)
    print(ava)
    print(avaP)
    return render_template('users/Home.html', rows=result, reg=reg, ava=ava, avaP=avaP)


# attendance
@app.route('/attendence/<id>', methods=["GET", "POST"])
def attendence(id):
    if session['logged_in'] == False:  return redirect(url_for('login'))
    conn = sqlite3.connect("CCSITWorkshop.DB")
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM Workshops where ID ='" + id + "'")
    cursor3 = conn.cursor()
    result3 = cursor3.execute("SELECT Name ,ID, attend FROM Student INNER JOIN registration ON registration.S_ID = Student.ID where W_ID ='" + id + "';")

    if request.method == "POST":
        if 'attend' in request.form:
            attend = request.form['attend']
            SID = request.form['studentid']
            cursor.execute("UPDATE registration SET attend='" + attend + "' WHERE W_ID='" + id + "' AND S_ID='" + SID + "' ;")
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(request.url)
        else:
            return redirect(url_for('home'))
    return render_template('Organizer/attendence.html', rows=result, names=result3)


# delete vendor info page
@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    # user = session['username']
    conn = sqlite3.connect("CCSITWorkshop.DB")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Workshops WHERE ID=?', (id,))
    conn.commit()
    return redirect(url_for('home'))


# Organizer home page
@app.route('/home', methods=['GET', 'POST'])
def home():
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    con = sqlite3.connect('CCSITWorkshop.DB')
    with con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Workshops")
        rows = cursor.fetchall()
    return render_template('Organizer/Home.html', rows=rows)


# vendor update PE page
@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    if session['logged_in'] == False:  return redirect(url_for('login'))
    if request.method == "GET":
        conn = sqlite3.connect("CCSITWorkshop.DB")
        cursor = conn.cursor()
        result = cursor.execute(" SELECT * FROM  Workshops where ID='" + id + "'")
        return render_template('Organizer/edit-activity.html', info=result)
    if request.method == "POST":
        error = " "
        if request.method == 'POST':
            file = request.files['files']
            if file.filename == '':
                title = request.form['title']
                org = request.form['org']
                date = request.form['date']
                location = request.form['loc']
                seats = request.form['seats']
                conn = sqlite3.connect("CCSITWorkshop.DB")
                cursor = conn.cursor()
                cursor.execute("UPDATE Workshops SET OrgName='" + org + "', Title='" + title + "', WDate='" + date + "', SeatsNo='" + seats + "', Location='" + location + "' WHERE  ID ='" + id + "';")
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('home'))

            if file and allowed_file(file.filename):
                # The image file seems valid!
                # Get the filenames and pass copy in logo dir and keep it in database
                title = request.form['title']
                org = request.form['org']
                date = request.form['date']
                location = request.form['loc']
                seats = request.form['seats']
                conn = sqlite3.connect("CCSITWorkshop.DB")
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE Workshops SET OrgName='" + org + "', Title='" + title + "', WDate='" + date + "', SeatsNo='" + seats + "', Location='" + location + "', Image='" + file.filename + "' WHERE  ID ='" + id + "';")
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('home'))
            error = "File is invalid type."
            return render_template('Organizer/edit-activity.html', error=error)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if session['logged_in'] == False:
        return redirect(url_for('login'))
    error = " "
    if request.method == 'POST':
        if 'files' in request.files:
            file = request.files['files']
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                # The image file seems valid!
                # Get the filenames and pass copy in logo dir and keep it in database
                title = request.form['title']
                org = request.form['org']
                date = request.form['date']
                location = request.form['loc']
                seats = request.form['seats']
                conn = sqlite3.connect("CCSITWorkshop.DB")
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Workshops VALUES (?,?,?,?,?,?,?,?)', (None, org, title, date, seats, location, file.filename, 0))
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                conn.commit()
                cursor.close()
                conn.close()
                return redirect(url_for('home'))
            error = "File is invalid type."
            return render_template('Organizer/add-activity.html', error=error)
        error = "Please upload image for activity."
        return render_template('Organizer/add-activity.html', error=error)
    return render_template('Organizer/add-activity.html', error=error)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# reset password page
@app.route('/resetpassword')
def resetpassword():
    return render_template('resetpassword.html')


# login page
@app.route('/', methods=['GET', 'POST'])
def login():
    session['logged_in'] = False
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = b_validate(username, password)
        if completion == False:
            completion = v_validate(username, password)
            if completion == False:
                error = 'Invalid Credentials. Please try again.'
            else:
                session['logged_in'] = True
                return redirect(url_for('home'))
        else:
            session['logged_in'] = True
            return redirect(url_for('UHome'))
    if 'forgetpass' in session:
        error2 = session['forgetpass']
    else:
        error2 = None
    #TODO: templates/login.html?
    return render_template('login.html', error=error, error2=error2)


# method for beneficiary login
def b_validate(username, password):
    con = sqlite3.connect('CCSITWorkshop.DB')
    completion = False
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Student")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[0]
            dbPass = row[2]
            if dbUser == username and dbPass == password:
                session['username'] = dbUser
                completion = True
    return completion


# method for vendor login
def v_validate(username, password):
    con = sqlite3.connect('CCSITWorkshop.DB')
    completion = False
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Organizer")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[0]
            dbPass = row[2]
            if dbUser == username and dbPass == password:
                session['username'] = dbUser
                completion = True
    return completion


# logout
@app.route('/logout')
def logout():
    return redirect(url_for('login'))


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    error = None
    if request.method == 'POST':
        token = request.form['Token']
        password = request.form['password']
        ConfirmPassword = request.form['ConfirmPassword']
        con = sqlite3.connect('CCSITWorkshop.DB')
        cur = con.cursor()
        with con:
            cur.execute("SELECT * FROM ResetPassword")
            rows = cur.fetchall()
            print(token)
            for row in rows:
                Token = row[1]
                username = row[0]
                print(Token)
                print(username)
                if token == Token and username == session['username']:
                    if password == ConfirmPassword:
                        if session['table'] == 'Organizer':
                            cur.execute("UPDATE Organizer SET Password ='" + password + "' Where ID ='" + session['username'] + "'")
                            cur.execute('DELETE FROM ResetPassword WHERE username=?', (session['username'],))
                            con.commit()
                            return redirect(url_for('login'))
                        elif session['table'] == 'Student':
                            cur.execute("UPDATE Student SET Password ='" + password + "' Where ID ='" + session['username'] + "'")
                            cur.execute('DELETE FROM ResetPassword WHERE username=?', (session['username'],))
                            con.commit()
                            return redirect(url_for('login'))
                        else:
                            con.commit()
                    else:
                        error = "Password and confirm password fileds are not matching"
                        return render_template('resetpassword.html', error=error)
                else:
                    error = "Please enter a vaild token"
                    return render_template('resetpassword.html', error=error)
    return render_template('resetpassword.html', error=error)


# method for vendor login
def E_validate(email):
    completion = False
    con = sqlite3.connect('CCSITWorkshop.DB')
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Organizer")
        rows = cur.fetchall()
        for row in rows:
            email = row[3]
            print(email)
            print(email)
            if email == email:
                completion = True
                con.commit()
                session['table'] = 'Organizer'
                return completion, row[0]
            else:
                with con:
                    cur.execute("SELECT * FROM Student")
                    rows = cur.fetchall()
                    for row in rows:
                        email = row[3]
                        print(email)
                        print(email)
                        if email == email:
                            completion = True
                            con.commit()
                            session['table'] = 'Student'
                            return completion, row[0]
    if completion == False:
        return completion, None


def sendmassage(token, email):
    msg = Message('Reset Password', sender='2020capes@gmail.com', recipients=[email])
    # TODO: it would be better to replace user with the real user name
    msg.body = "Hello \nDear user, use this token to reset your password:" + token
    mail.send(msg)
    return None


def get_random_string(length=5, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))


@app.route('/forgot', methods=['GET', 'POST'])
def forget():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        completion, username = E_validate(email)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
            return render_template('forgetpassword.html', error=error)
        elif completion == True and username is not None:
            token = get_random_string()
            con = sqlite3.connect('CCSITWorkshop.DB')
            cur = con.cursor()
            cur.execute('INSERT INTO ResetPassword VALUES (?,?)', (username, token))
            con.commit()
            cur.close()
            con.close()
            sendmassage(token, email)
            print(username)
            session['username'] = username
            return redirect(url_for('reset'))
    if request.method == 'GET':
        return render_template('forgetpassword.html', error=error)
