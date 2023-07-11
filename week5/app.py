from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.sqlite3'
db = SQLAlchemy(app)

class student(db.Model):
    student_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    roll_number=db.Column(db.String,unique=True,nullable=False)
    first_name=db.Column(db.String,nullable=False)
    last_name=db.Column(db.String)
    courses=db.relationship('enrollments',backref='student')

class course(db.Model):
    course_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    course_code=db.Column(db.String,unique=True,nullable=False)
    course_name=db.Column(db.String,nullable=False)
    course_description=db.Column(db.String)
    students=db.relationship('enrollments',backref='course')

class enrollments(db.Model):
    enrollment_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    estudent_id=db.Column(db.Integer,db.ForeignKey('student.student_id'),nullable=False)
    ecourse_id=db.Column(db.Integer,db.ForeignKey('course.course_id'),nullable=False)

@app.route("/")
def home():
    all=student.query.all()
    return render_template("index.html",all=all)


@app.route("/student/create",methods=["GET","POST"])
def add_student():
    if request.method=="POST":
        roll=request.form['roll']
        fname=request.form['f_name']
        lname=request.form['l_name']
        courses=request.form.getlist("courses")

        b=student.query.all()
        for elem in b:
            if elem.roll_number==roll:
                return render_template("already.html")


        m=student(roll_number=roll,first_name=fname,last_name=lname)
        db.session.add(m)
        db.session.commit()

        for elem in courses:
            if elem=="course_1":
                course_code='CSE01'

                n=course.query.filter_by(course_code=course_code).first()
                a=enrollments(estudent_id=m.student_id,ecourse_id=n.course_id)
                n.students.append(a)
                db.session.commit()

            elif elem=="course_2":
                course_code='CSE02'

                n=course.query.filter_by(course_code=course_code).first()
                a=enrollments(estudent_id=m.student_id,ecourse_id=n.course_id)
                n.students.append(a)
                db.session.commit()

            elif elem=="course_3":
                course_code='CSE03'

                n=course.query.filter_by(course_code=course_code).first()
                a=enrollments(estudent_id=m.student_id,ecourse_id=n.course_id)
                n.students.append(a)
                db.session.commit()

            elif elem=="course_4":
                course_code='BST13'

                n=course.query.filter_by(course_code=course_code).first()
                a=enrollments(estudent_id=m.student_id,ecourse_id=n.course_id)
                n.students.append(a)
                db.session.commit()
        

        return redirect("/")

    return render_template("addstudent.html")


@app.route("/student/<student_id>")
def show(student_id):
    a=student.query.filter_by(student_id=student_id).first()
    b=enrollments.query.filter_by(estudent_id=student_id).all()
    d=[]
    for elem in b:
        c=course.query.filter_by(course_id=elem.ecourse_id).first()
        d.append(c)
    return render_template("details.html",a=a,d=d)
    

@app.route('/student/<int:student_id>/update', methods=["GET"])
def show_update_form(student_id):
    students = student.query.filter_by(student_id=student_id).first()
    courses = enrollments.query.filter_by(estudent_id=student_id).all()
    checked = ["", "", "", ""]
    for course in courses:
        checked[course.ecourse_id-1] = "checked"
    return render_template("update.html",student_id=student_id, current_roll=students.roll_number, current_f_name=students.first_name, current_l_name=students.last_name,
                           checked_1=checked[0],checked_2=checked[1],checked_3=checked[2],checked_4=checked[3])


@app.route('/student/<int:student_id>/update', methods=["POST"])
def update_form(student_id):
    data = request.form
    first_name = data["f_name"]
    last_name = data["l_name"]

    courses_list = []

    for listkey, listval in data.lists():
        if listkey == 'courses':
            for val in listval:
                courses_list.append(val)
    
    current_courses = enrollments.query.filter_by(estudent_id=student_id).all()
    for course in current_courses:
        db.session.delete(course)
    db.session.commit()

    curr_stu = student.query.filter_by(student_id=student_id).first()
    curr_stu.first_name = first_name
    curr_stu.last_name = last_name
    db.session.commit()

    for course in courses_list:
        course_number = course.split("_")[1]
        courseObj = enrollments(
            estudent_id=curr_stu.student_id, ecourse_id=course_number)
        db.session.add(courseObj)
    db.session.commit()
    return redirect('/')

@app.route("/student/<student_id>/delete", methods=["GET","POST"])
def delete(student_id):
    if request.method=="GET":
        #email=request.form["email"]
        a=student.query.filter_by(student_id=student_id).first()
        b=enrollments.query.filter_by(estudent_id=student_id).all()
        db.session.delete(a)
        for elem in b:
            db.session.delete(elem)
        db.session.commit()
        return redirect("/")



if __name__=="__main__":
    app.run(debug=True)