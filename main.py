import subprocess
import mysql
import mysql.connector
from flask import *
from datetime import date
import matplotlib.pyplot as plt
import unittest

from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "it should be secret"


#######################################################################################################


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


#######################################################################################################


@app.route("/logout")
def logout():
    session.pop("moduleList", None)  # Instructor
    session.pop("AllStudentList", None)  # Instructor
    session.pop("questionList", None)  # Instructor
    session.pop("selectedCourse", None)  # Instructor
    session.pop("selectedModule", None)  # Instructor
    session.pop("selectedCourseID", None)  # Instructor
    session.pop("selectedModuleID", None)  # Instructor
    session.pop("isSolvedList", None)  # Instructor
    session.pop("attemptsList", None)  # Instructor
    session.pop("selectedQuestionID", None)  # Instructor
    session.pop("selectedQuestion", None)  # Instructor

    session.pop("selectedQuestionIDCreateReport", None)  # Interpreter
    session.pop("code", None)  # Interpreter
    session.pop("codeoutput", None)  # Interpreter

    session.pop("username", None)  # Student,Instructor
    session.pop("courseList", None)  # Student,Instructor

    session.pop("studentQuestionList", None)  # Student
    session.pop("studentSelectedModule", None)  # Student
    session.pop("studentSelectedCourse", None)  # Student
    session.pop("studentModuleList", None)  # Student
    session.pop("studentSelectedModuleID", None)  # Student
    session.pop("studentSelectedCourseID", None)  # Student
    session.pop("studentSelectedQuestionID", None)  # Student
    session.pop("studentSelectedQuestion", None)  # Student
    session.pop("studentIsSolvedList", None)  # Student

    return redirect(url_for("index"))


#######################################################################################################
# helper function to convert escape result to string
def applyescape(string):
    return str(escape(string))


#######################################################################################################

### Instructor / Student


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = applyescape(request.form["username"])
        password = applyescape(request.form["password"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        ###deneme
        if conn.is_connected():
            print("connection is successfull")
        ###deneme
        print(type(username))

        c.execute(
            "SELECT * FROM user WHERE username=%s AND password=%s",
            ((username), (password)),
        )
        row = c.fetchone()

        conn.close()
        if row != None:
            session["username"] = username
            if row[4] == 1:
                conn = mysql.connector.connect(
                    host="localhost", port="3306", user="root", database="lap"
                )
                c = conn.cursor()

                c.execute(
                    "SELECT courseID,courseCode FROM course WHERE instructorUsername=%s ORDER BY courseCode",
                    (str(session["username"]),),
                )
                courseList = c.fetchall()
                conn.close()

                session["courseList"] = courseList
                return render_template("courses.html", courseList=session["courseList"])

            else:
                conn = mysql.connector.connect(
                    host="localhost", port="3306", user="root", database="lap"
                )
                c = conn.cursor()

                c.execute(
                    "SELECT registration.courseID,course.courseCode FROM student,course,registration WHERE registration.courseID=course.courseID AND  student.username=registration.username AND registration.username=%s ORDER BY course.courseCode",
                    (session["username"],),
                )
                courseList = c.fetchall()

                conn.close()

                session["courseList"] = courseList
                return render_template(
                    "studentCourses.html",
                    courseList=session["courseList"],
                    username=(session["username"]),
                )
        else:
            flash("Invalid Username or Password!", "warning")
            return redirect(url_for("index"))

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor / Student


@app.route("/registerPage")
def registerPage():
    return render_template("register.html")


def insertUser(username, password, name, surname, userType):
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    ###deneme
    if conn.is_connected():
        print("connection is successfull")
    ###deneme

    c.execute("SELECT * FROM user WHERE username=%s", (username,))
    row = c.fetchone()

    if row != None:
        return False
    else:
        c.execute(
            "INSERT INTO user VALUES (%s, %s, %s, %s, %s)",
            (
                username,
                password,
                name,
                surname,
                userType,
            ),
        )
        if userType == "1":
            c.execute("INSERT INTO instructor VALUES (%s)", (username,))
        else:
            c.execute("INSERT INTO student VALUES (%s)", (username,))
        conn.commit()
        conn.close()
        return True


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = applyescape(request.form["username"])
        name = applyescape(request.form["name"])
        surname = applyescape(request.form["surname"])
        password = applyescape(request.form["password"])
        userType = applyescape(request.form["user_type"])

        insertUs = insertUser(
            username=username,
            password=password,
            name=name,
            surname=surname,
            userType=userType,
        )

        if insertUs == False:
            flash("This username is already used!", "warning")
            return render_template("register.html")
        elif insertUs == True:
            return render_template("index.html")

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/instructor")
def instructor():
    return render_template("instructor.html", username=session["username"])


#######################################################################################################

### Instructor


@app.route("/coursesPage")
def coursesPage():
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    c.execute(
        "SELECT courseID,courseCode FROM course WHERE instructorUsername=%s ORDER BY courseCode",
        (str(session["username"]),),
    )
    courseList = c.fetchall()
    conn.close()

    session["courseList"] = courseList
    return render_template("courses.html", courseList=session["courseList"])


#######################################################################################################

### Instructor


@app.route("/addCoursesPage")
def addCoursesPage():
    return render_template("addCourses.html")


def insertCourse(courseCode, instructorUsername):
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    ###deneme
    if conn.is_connected():
        print("connection is successfull")
    ###deneme

    c.execute(
        "SELECT courseCode FROM course,instructor WHERE instructor.username=course.instructorUsername AND courseCode=%s AND instructor.username=%s ",
        (courseCode, instructorUsername),
    )
    rowCourse = c.fetchone()

    if rowCourse == None:
        c.execute(
            "INSERT INTO course(courseCode,instructorUsername) VALUES (%s, %s)",
            (
                courseCode,
                instructorUsername,
            ),
        )
        conn.commit()
        conn.close()
        return True
    else:
        return False


@app.route("/addCourse", methods=["GET", "POST"])
def addCourse():
    if request.method == "POST":
        courseCode = applyescape(request.form["courseCode"])
        instructorUsername = session["username"]

        insertCo = insertCourse(courseCode, instructorUsername)

        if insertCo == True:
            return redirect(url_for("coursesPage"))

        else:
            return render_template("addCourses.html")

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/selectedCoursePage", methods=["GET", "POST"])
def selectedCoursePage():
    if request.method == "POST":
        selectedCourseID = applyescape(request.form["selectedCourseID"])

        ###deneme
        print(selectedCourseID)
        print(session["courseList"])
        print(session["username"])
        ###deneme

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT moduleID,moduleName FROM module WHERE courseID=%s ORDER BY moduleName",
            (selectedCourseID,),
        )
        moduleList = c.fetchall()

        c.execute(
            "SELECT courseCode FROM course WHERE courseID=%s", (selectedCourseID,)
        )
        selectedCourse = c.fetchone()

        conn.close()

        session["moduleList"] = moduleList
        session["selectedCourse"] = selectedCourse[0]
        session["selectedCourseID"] = selectedCourseID

        return render_template(
            "selectedCourse.html",
            moduleList=session["moduleList"],
            selectedCourse=session["selectedCourse"],
        )

    elif request.method == "GET":
        ### herhangi bir işlem olmadığında tekrar module listeyi döndürcek...

        selectedCourseID = session["selectedCourseID"]

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT * FROM module WHERE courseID=%s ORDER BY moduleName",
            (selectedCourseID,),
        )
        moduleList = c.fetchall()

        c.execute(
            "SELECT courseCode FROM course WHERE courseID=%s", (selectedCourseID,)
        )
        selectedCourse = c.fetchone()

        conn.close()

        session["selectedCourse"] = selectedCourse[0]
        session["moduleList"] = moduleList

        return render_template(
            "selectedCourse.html",
            moduleList=session["moduleList"],
            selectedCourse=session["selectedCourse"],
        )


#######################################################################################################

### Instructor


@app.route("/addModulesPage")
def addModulesPage():
    return render_template("addModules.html", selectedCourse=session["selectedCourse"])


def insertModule(moduleName, selectedCourseID, deadline):
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    ###deneme
    if conn.is_connected():
        print("connection is successfull")
    ###deneme

    c.execute(
        "SELECT * FROM module,course WHERE moduleName=%s AND course.courseID=module.courseID AND course.courseID=%s ",
        (
            moduleName,
            selectedCourseID,
        ),
    )
    rowModule = c.fetchone()

    ###deneme
    print(rowModule)
    ###deneme

    if rowModule == None:
        c.execute(
            "INSERT INTO module(moduleName,deadline,courseID) VALUES (%s, %s, %s)",
            (
                moduleName,
                deadline,
                selectedCourseID,
            ),
        )
        conn.commit()
        conn.close()
        return True
    else:
        return False


@app.route("/addModule", methods=["GET", "POST"])
def addModule():
    if request.method == "POST":
        moduleName = applyescape(request.form["moduleName"])
        deadline = applyescape(request.form["deadline"])
        selectedCourseID = session["selectedCourseID"]

        inserMod = insertModule(
            moduleName=moduleName, selectedCourseID=selectedCourseID, deadline=deadline
        )

        if inserMod == True:
            return redirect(url_for("selectedCoursePage"))
        else:
            return render_template("addModules.html")

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/selectedModulePage", methods=["GET", "POST"])
def selectedModulePage():
    if request.method == "POST":
        selectedModuleID = applyescape(request.form["selectedModuleID"])

        ###deneme
        print(selectedModuleID)
        print(session["selectedCourse"])
        print(session["username"])
        ###deneme

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT questionID,questionNo,questionStatus FROM question WHERE moduleID=%s ORDER BY questionNo",
            (selectedModuleID,),
        )
        questionList = c.fetchall()

        c.execute(
            "SELECT moduleName FROM module WHERE moduleID=%s", (selectedModuleID,)
        )
        selectedModule = c.fetchone()

        c.execute(
            "SELECT * FROM registration WHERE courseID=%s",
            (session["selectedCourseID"],),
        )
        registeredStudent = c.fetchall()

        isSolvedList = []
        attemptsList = []
        for i in questionList:
            sumOfisSolved = 0
            sumOfAttempts = 0
            c.execute("SELECT * FROM solution WHERE questionID=%s", (i[0],))
            isSolved = c.fetchall()
            for j in isSolved:
                sumOfisSolved += j[2]
                sumOfAttempts += j[3]
            listIsSolved = []
            listIsSolved.append(i[0])

            if len(registeredStudent) == 0:
                listIsSolved.append(0.0)
            else:
                listIsSolved.append(100 * sumOfisSolved / len(registeredStudent))

            isSolvedList.append(listIsSolved)

            listAttempts = []
            listAttempts.append(i[0])

            if len(isSolved) == 0:
                listAttempts.append(0.0)
            else:
                listAttempts.append(sumOfAttempts / len(isSolved))

            attemptsList.append(listAttempts)

        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        print(isSolvedList)
        print("yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
        print(attemptsList)
        print("zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz")
        for i in range(len(isSolvedList)):
            isSolvedList[i][1] = float("{:.2f}".format(isSolvedList[i][1]))
        print(isSolvedList)

        for i in range(len(attemptsList)):
            attemptsList[i][1] = float("{:.2f}".format(attemptsList[i][1]))
        print(attemptsList)

        conn.close()

        session["isSolvedList"] = isSolvedList
        session["attemptsList"] = attemptsList

        session["questionList"] = questionList
        session["selectedModuleID"] = selectedModuleID
        session["selectedModule"] = selectedModule[0]

        ###deneme
        print(questionList)
        ###deneme

        return render_template(
            "selectedModule.html",
            questionList=session["questionList"],
            selectedModule=session["selectedModule"],
            selectedCourse=session["selectedCourse"],
            isSolvedList=session["isSolvedList"],
            attemptsList=session["attemptsList"],
        )

    elif request.method == "GET":
        session.pop(
            "code", None
        )  # Code poplanır her seferinde question content gelsin diye!!!

        selectedModuleID = session["selectedModuleID"]

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT questionID,questionNo,questionStatus FROM question WHERE moduleID=%s ORDER BY questionNo",
            (selectedModuleID,),
        )
        questionList = c.fetchall()

        c.execute(
            "SELECT moduleName FROM module WHERE moduleID=%s", (selectedModuleID,)
        )
        selectedModule = c.fetchone()

        c.execute(
            "SELECT * FROM registration WHERE courseID=%s",
            (session["selectedCourseID"],),
        )
        registeredStudent = c.fetchall()

        isSolvedList = []
        attemptsList = []
        for i in questionList:
            sumOfisSolved = 0
            sumOfAttempts = 0
            c.execute("SELECT * FROM solution WHERE questionID=%s", (i[0],))
            isSolved = c.fetchall()
            for j in isSolved:
                sumOfisSolved += j[2]
                sumOfAttempts += j[3]
            listIsSolved = []
            listIsSolved.append(i[0])

            if len(registeredStudent) == 0:
                listIsSolved.append(0.0)
            else:
                listIsSolved.append(100 * sumOfisSolved / len(registeredStudent))

            isSolvedList.append(listIsSolved)

            listAttempts = []
            listAttempts.append(i[0])

            if len(isSolved) == 0:
                listAttempts.append(0.0)
            else:
                listAttempts.append(sumOfAttempts / len(isSolved))

            attemptsList.append(listAttempts)

        print(isSolvedList)
        for i in range(len(isSolvedList)):
            isSolvedList[i][1] = float("{:.2f}".format(isSolvedList[i][1]))
        print(isSolvedList)
        print(attemptsList)
        for i in range(len(attemptsList)):
            attemptsList[i][1] = float("{:.2f}".format(attemptsList[i][1]))
        print(attemptsList)

        conn.close()

        session["isSolvedList"] = isSolvedList
        session["attemptsList"] = attemptsList

        session["questionList"] = questionList
        session["selectedModule"] = selectedModule[0]

        ###deneme
        print(questionList)
        ###deneme

        return render_template(
            "selectedModule.html",
            questionList=session["questionList"],
            selectedModule=session["selectedModule"],
            selectedCourse=session["selectedCourse"],
            isSolvedList=session["isSolvedList"],
            attemptsList=session["attemptsList"],
        )


#######################################################################################################

### Instructor


@app.route("/addQuestionPage")
def addQuestionPage():
    return render_template(
        "addQuestions.html",
        selectedModule=session["selectedModule"],
        selectedCourse=session["selectedCourse"],
    )


def insertQuestion(
    questionNo, question, selectedModuleID, questionContent, selectedCourseID, testCase
):
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    ###deneme
    if conn.is_connected():
        print("connection is successfull")
    ###deneme

    c.execute(
        "SELECT * FROM module,course,question WHERE questionNo=%s AND module.moduleID=question.moduleID AND course.courseID=module.courseID AND module.moduleID=%s AND course.courseID=%s",
        (
            questionNo,
            selectedModuleID,
            selectedCourseID,
        ),
    )
    rowQuestion = c.fetchone()

    if rowQuestion == None:
        c.execute(
            "INSERT INTO question(questionNo,question,moduleID,questionContent) VALUES (%s, %s, %s,%s)",
            (questionNo, question, selectedModuleID, questionContent),
        )

        conn.commit()

        c.execute(
            "SELECT questionID FROM module,course,question WHERE questionNo=%s AND module.moduleID=question.moduleID AND course.courseID=module.courseID AND module.moduleID=%s AND course.courseID=%s",
            (
                questionNo,
                selectedModuleID,
                selectedCourseID,
            ),
        )
        rowQuestionID = c.fetchone()

        c.execute(
            "INSERT INTO testcases VALUES (%s, %s)",
            (
                rowQuestionID[0],
                testCase,
            ),
        )

        conn.commit()
        conn.close()
        return True

    else:
        return False


@app.route("/addQuestion", methods=["GET", "POST"])
def addQuestion():
    if request.method == "POST":
        questionNo = int(applyescape(request.form["questionNo"]))
        question = applyescape(request.form["question"])
        testCase = request.form["testCase"]
        questionContent = applyescape(request.form["questionContent"])

        selectedModuleID = session["selectedModuleID"]
        selectedCourseID = session["selectedCourseID"]

        insertQu = insertQuestion(
            questionNo=questionNo,
            question=question,
            selectedModuleID=selectedModuleID,
            questionContent=questionContent,
            selectedCourseID=selectedCourseID,
            testCase=testCase,
        )

        if insertQu == True:
            return redirect(url_for("selectedModulePage"))

        else:
            return render_template("addQuestions.html")
    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/selectedQuestionPage", methods=["GET", "POST"])
def selectedQuestionPage():
    if request.method == "POST":
        selectedQuestionID = applyescape(request.form["selectedQuestionID"])

        ###deneme
        print(selectedQuestionID)
        print(session["selectedCourse"])
        print(session["selectedModule"])
        print(session["username"])
        ###deneme

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT questionNo,question,questionContent,testCase FROM question,testcases WHERE question.questionID=testcases.questionID AND question.questionID=%s",
            (selectedQuestionID,),
        )
        selectedQuestion = c.fetchone()

        conn.close()

        session["selectedQuestionID"] = selectedQuestionID
        session["selectedQuestion"] = selectedQuestion

        ###deneme
        print(selectedQuestion)
        ###deneme

        return render_template(
            "selectedQuestion.html",
            selectedQuestion=session["selectedQuestion"],
            selectedModule=session["selectedModule"],
            selectedCourse=session["selectedCourse"],
        )

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/addStudentPage")
def addStudentPage():
    return render_template("addStudents.html", selectedCourse=session["selectedCourse"])


def insertStudent(studentList, selectedCourseID):
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()
    ###deneme
    if conn.is_connected():
        print("connection is successfull")
    ###deneme

    print(studentList)

    for student in studentList:
        c.execute(
            "SELECT * FROM registration WHERE registration.username=%s AND registration.courseID=%s  ",
            (
                student,
                selectedCourseID,
            ),
        )
        rowStudent = c.fetchone()

        if student == "":
            break

        if rowStudent == None:
            c.execute("SELECT * FROM student WHERE username=%s ", (student,))
            rowStudent = c.fetchone()
            if rowStudent != None:
                c.execute(
                    "INSERT INTO registration VALUES (%s, %s, %s,%s)",
                    (student, selectedCourseID, 0, "null"),
                )
                conn.commit()

            else:
                print("Student with %s username does not exist!" % (student))
                flash("Student with %s username does not exist!" % (student), "warning")
                return False
        else:
            print(
                "Student with %s username already registered to this course!"
                % (student)
            )
            flash(
                "Student with %s username already registered to this course!"
                % (student),
                "warning",
            )
            return False
    conn.close()
    return True


@app.route("/addStudent", methods=["GET", "POST"])
def addStudent():
    if request.method == "POST":
        studentUsernameList = applyescape(request.form["studentUsernameList"])
        selectedCourseID = session["selectedCourseID"]

        studentList = studentUsernameList.split(";")
        insertStu = insertStudent(
            studentList=studentList, selectedCourseID=selectedCourseID
        )

        if insertStu == True:
            return redirect(url_for("selectedCoursePage"))

        else:
            return render_template(
                "addStudents.html", selectedCourse=session["selectedCourse"]
            )

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/getStudentList")
def getStudentList():
    selectedCourseID = session["selectedCourseID"]

    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    ###deneme
    if conn.is_connected():
        print("connection is successfull")
    ###deneme

    c.execute(
        "SELECT user.username,name,surname FROM registration,student,user WHERE student.username=user.username AND student.username=registration.username AND registration.courseID=%s ",
        (selectedCourseID,),
    )
    AllStudentList = c.fetchall()

    ###deneme
    print(AllStudentList)
    ###deneme

    conn.close()
    session["AllStudentList"] = AllStudentList

    return render_template(
        "getStudentList.html",
        AllStudentList=session["AllStudentList"],
        selectedCourse=session["selectedCourse"],
    )


#######################################################################################################

### Instructor


@app.route("/takeAttendanceInStudentList")
def takeAttendanceInStudentList():
    selectedCourseID = session["selectedCourseID"]
    selectedModuleID = session["selectedModuleID"]

    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    ###deneme
    if conn.is_connected():
        print("connection is successfull")
    ###deneme

    c.execute(
        "SELECT user.username,name,surname FROM registration,student,user WHERE student.username=user.username AND student.username=registration.username AND registration.courseID=%s ",
        (selectedCourseID,),
    )
    AllStudentList = c.fetchall()

    session["AllStudentList"] = AllStudentList

    ###deneme
    print(AllStudentList)
    ###deneme

    c.execute("SELECT * FROM attendance WHERE moduleID=%s", (selectedModuleID,))
    AllModuleAttendanceList = c.fetchall()

    conn.close()

    if AllModuleAttendanceList == None:
        AllModuleAttendanceList = []
        return render_template(
            "getStudentListInModule.html",
            selectedModule=session["selectedModule"],
            AllStudentList=session["AllStudentList"],
            selectedCourse=session["selectedCourse"],
            AllModuleAttendanceList=AllModuleAttendanceList,
        )
    else:
        return render_template(
            "getStudentListInModule.html",
            selectedModule=session["selectedModule"],
            AllStudentList=session["AllStudentList"],
            selectedCourse=session["selectedCourse"],
            AllModuleAttendanceList=AllModuleAttendanceList,
        )


@app.route("/takeAttendancePage")
def takeAttendancePage():
    return render_template(
        "takeAttendance.html",
        selectedModule=session["selectedModule"],
        selectedCourse=session["selectedCourse"],
    )


@app.route("/takeAttendance", methods=["GET", "POST"])
def takeAttendance():
    if request.method == "POST":
        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        ###deneme
        if conn.is_connected():
            print("connection is successfull")
        ###deneme

        f = request.files["myfile"]
        f.save(secure_filename(f.filename))

        fileName = f.filename

        ###deneme
        print(f)
        print(fileName)
        ###deneme

        attendanceList = open(fileName, "r")
        selectedModuleID = session["selectedModuleID"]

        for line in attendanceList:
            splittedLine = line.split("-")
            splittedLine[1] = splittedLine[1][:-1]
            print(splittedLine)

            c.execute(
                "SELECT * FROM attendance WHERE username=%s AND moduleID=%s",
                (
                    splittedLine[0],
                    selectedModuleID,
                ),
            )
            AllModuleAttendanceList = c.fetchone()

            if AllModuleAttendanceList == None:
                c.execute(
                    "INSERT INTO attendance VALUES (%s, %s, %s)",
                    (
                        selectedModuleID,
                        splittedLine[0],
                        splittedLine[1],
                    ),
                )
                conn.commit()
            else:
                c.execute(
                    "UPDATE attendance SET attended=%s WHERE username=%s AND moduleID=%s",
                    (
                        splittedLine[1],
                        splittedLine[0],
                        selectedModuleID,
                    ),
                )
                conn.commit()
        conn.close()
        attendanceList.close()
        return redirect(url_for("takeAttendanceInStudentList"))


#######################################################################################################

### Student


@app.route("/student")
def student():
    return render_template("student.html", username=session["username"])


#######################################################################################################

### Student


@app.route("/studentCoursesPage")
def studentCoursesPage():
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    c.execute(
        "SELECT registration.courseID,course.courseCode FROM student,course,registration WHERE registration.courseID=course.courseID AND  student.username=registration.username AND registration.username=%s ORDER BY course.courseCode",
        (session["username"],),
    )
    courseList = c.fetchall()

    conn.close()

    session["courseList"] = courseList
    return render_template(
        "studentCourses.html",
        courseList=session["courseList"],
        username=(session["username"]),
    )


#######################################################################################################

### Student


@app.route("/studentSelectedCoursePage", methods=["GET", "POST"])
def studentSelectedCoursePage():
    if request.method == "POST":
        studentSelectedCourseID = applyescape(request.form["studentSelectedCourseID"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT module.moduleID,module.moduleName,module.deadline FROM course,module WHERE module.courseID=course.courseID AND course.courseID=%s ORDER BY module.moduleName",
            (studentSelectedCourseID,),
        )
        studentModuleList = c.fetchall()

        c.execute(
            "SELECT courseCode FROM course WHERE courseID=%s",
            (studentSelectedCourseID,),
        )
        studentSelectedCourse = c.fetchone()

        conn.close()

        session["studentSelectedCourse"] = studentSelectedCourse[0]
        session["studentModuleList"] = studentModuleList
        session["studentSelectedCourseID"] = studentSelectedCourseID

        today = date.today()

        ###deneme
        print(today)
        print(studentSelectedCourseID)
        print(studentModuleList)
        ###deneme

        return render_template(
            "studentSelectedCourse.html",
            studentModuleList=session["studentModuleList"],
            studentSelectedCourse=session["studentSelectedCourse"],
            today=today,
        )

    elif request.method == "GET":
        studentSelectedCourseID = session["studentSelectedCourseID"]

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT module.moduleID,module.moduleName,module.deadline FROM course,module WHERE module.courseID=course.courseID AND course.courseID=%s ORDER BY module.moduleName",
            (studentSelectedCourseID,),
        )
        studentModuleList = c.fetchall()

        c.execute(
            "SELECT courseCode FROM course WHERE courseID=%s",
            (studentSelectedCourseID,),
        )
        studentSelectedCourse = c.fetchone()

        conn.close()

        session["studentSelectedCourse"] = studentSelectedCourse[0]
        session["studentModuleList"] = studentModuleList
        today = date.today()

        ###deneme
        print(today)
        print(studentSelectedCourse)
        print(studentModuleList)
        ###deneme

        return render_template(
            "studentSelectedCourse.html",
            studentModuleList=session["studentModuleList"],
            studentSelectedCourse=session["studentSelectedCourse"],
            today=today,
        )


#######################################################################################################

### Student


@app.route("/studentSelectedModulePage", methods=["GET", "POST"])
def studentSelectedModulePage():
    if request.method == "POST":
        studentSelectedModuleID = applyescape(request.form["studentSelectedModuleID"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT questionID,questionNo,questionStatus FROM question WHERE moduleID=%s ORDER BY questionNo",
            (studentSelectedModuleID,),
        )
        studentQuestionList = c.fetchall()

        c.execute(
            "SELECT moduleName FROM module WHERE moduleID=%s",
            (studentSelectedModuleID,),
        )
        studentSelectedModule = c.fetchone()

        isSolvedList = []
        for i in studentQuestionList:
            c.execute(
                "SELECT isSolved FROM solution WHERE username=%s AND questionID=%s",
                (session["username"], i[0]),
            )
            isSolved = c.fetchone()
            isSolvedInner = []
            isSolvedInner.append(i[0])
            if isSolved == None:
                isSolvedInner.append(0)
            else:
                isSolved = isSolved[0]
                isSolvedInner.append(isSolved)

            isSolvedList.append(isSolvedInner)

        conn.close()

        session["studentIsSolvedList"] = isSolvedList
        session["studentQuestionList"] = studentQuestionList
        session["studentSelectedModule"] = studentSelectedModule[0]
        session["studentSelectedModuleID"] = studentSelectedModuleID

        ###deneme
        print(studentQuestionList)
        print(studentSelectedModule)
        ###deneme

        return render_template(
            "studentSelectedModule.html",
            studentQuestionList=session["studentQuestionList"],
            studentSelectedCourse=session["studentSelectedCourse"],
            studentSelectedModule=session["studentSelectedModule"],
            studentIsSolvedList=session["studentIsSolvedList"],
        )
    elif request.method == "GET":
        session.pop(
            "code", None
        )  # Code poplanır her seferinde question content gelsin diye!!!

        studentSelectedModuleID = session["studentSelectedModuleID"]

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT questionID,questionNo,questionStatus FROM question WHERE moduleID=%s ORDER BY questionNo",
            (studentSelectedModuleID,),
        )
        studentQuestionList = c.fetchall()

        c.execute(
            "SELECT moduleName FROM module WHERE moduleID=%s",
            (studentSelectedModuleID,),
        )
        studentSelectedModule = c.fetchone()

        isSolvedList = []
        for i in studentQuestionList:
            c.execute(
                "SELECT isSolved FROM solution WHERE username=%s AND questionID=%s",
                (session["username"], i[0]),
            )
            isSolved = c.fetchone()
            isSolvedInner = []
            isSolvedInner.append(i[0])
            if isSolved == None:
                isSolvedInner.append(0)
            else:
                isSolved = isSolved[0]
                isSolvedInner.append(isSolved)

            isSolvedList.append(isSolvedInner)

        conn.close()

        session["studentIsSolvedList"] = isSolvedList
        session["studentQuestionList"] = studentQuestionList
        session["studentSelectedModule"] = studentSelectedModule[0]

        ###deneme
        print(studentQuestionList)
        print(studentSelectedModule)
        ###deneme

        return render_template(
            "studentSelectedModule.html",
            studentQuestionList=session["studentQuestionList"],
            studentSelectedCourse=session["studentSelectedCourse"],
            studentSelectedModule=session["studentSelectedModule"],
            studentIsSolvedList=session["studentIsSolvedList"],
        )


#######################################################################################################

### Student


@app.route("/studentSelectedQuestionPage", methods=["GET", "POST"])
def studentSelectedQuestionPage():
    if request.method == "POST":
        studentSelectedQuestionID = applyescape(
            request.form["studentSelectedQuestionID"]
        )

        ###deneme
        print(studentSelectedQuestionID)
        print(session["username"])
        ###deneme

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT questionNo,question,questionContent FROM question WHERE questionID=%s",
            (studentSelectedQuestionID,),
        )
        studentSelectedQuestion = c.fetchone()

        conn.close()

        session["studentSelectedQuestionID"] = studentSelectedQuestionID
        session["studentSelectedQuestion"] = studentSelectedQuestion

        ###deneme
        print(studentSelectedQuestion)
        ###deneme

        return render_template(
            "studentSelectedQuestion.html",
            studentSelectedQuestion=session["studentSelectedQuestion"],
            studentSelectedModule=session["studentSelectedModule"],
            studentSelectedCourse=session["studentSelectedCourse"],
        )

    elif request.method == "GET":
        pass


#######################################################################################################

### Student


@app.route("/studentSelectedCourseEvaluationPage", methods=["GET", "POST"])
def studentSelectedCourseEvaluationPage():
    if request.method == "POST":
        studentSelectedCourseEvaluate = applyescape(
            request.form["studentSelectedCourseEvaluate"]
        )

        ###deneme
        print(studentSelectedCourseEvaluate)
        ###deneme


#######################################################################################################

### Instructor


@app.route("/updateCoursePage", methods=["GET", "POST"])
def updateCoursePage():
    if request.method == "POST":
        selectedCourseID = applyescape(request.form["selectedCourseID"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT courseCode FROM course WHERE courseID=%s", (selectedCourseID,)
        )
        selectedCourse = c.fetchone()

        conn.close()

        return render_template(
            "updateCourse.html",
            selectedCourse=selectedCourse,
            selectedCourseID=selectedCourseID,
        )
    elif request.method == "GET":
        pass


@app.route("/updateCourse/<selectedCourseID>", methods=["GET", "POST"])
def updateCourse(selectedCourseID):
    if request.method == "POST":
        newCourseCode = applyescape(request.form["courseCode"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "UPDATE course SET courseCode=%s WHERE courseID=%s",
            (
                newCourseCode,
                selectedCourseID,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("coursesPage"))

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/updateModulePage", methods=["GET", "POST"])
def updateModulePage():
    if request.method == "POST":
        selectedModuleID = applyescape(request.form["selectedModuleID"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT moduleName,deadline FROM module WHERE moduleID=%s",
            (selectedModuleID,),
        )
        selectedModule = c.fetchone()

        conn.close()

        return render_template(
            "updateModule.html",
            selectedCourse=session["selectedCourse"],
            selectedModule=selectedModule,
            selectedModuleID=selectedModuleID,
        )
    elif request.method == "GET":
        pass


@app.route("/updateModule/<selectedModuleID>", methods=["GET", "POST"])
def updateModule(selectedModuleID):
    if request.method == "POST":
        newModuleName = applyescape(request.form["moduleName"])

        newDeadline = applyescape(request.form["deadline"])

        print(newDeadline)

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "UPDATE module SET moduleName=%s,deadline=%s WHERE moduleID=%s",
            (
                newModuleName,
                newDeadline,
                selectedModuleID,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("selectedCoursePage"))

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/updateQuestionPage", methods=["GET", "POST"])
def updateQuestionPage():
    if request.method == "POST":
        selectedQuestionID = applyescape(request.form["selectedQuestionID"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT questionNo,question,questionContent FROM question WHERE questionID=%s",
            (selectedQuestionID,),
        )
        selectedQuestion = c.fetchone()

        conn.close()

        return render_template(
            "updateQuestion.html",
            selectedCourse=session["selectedCourse"],
            selectedModule=session["selectedModule"],
            selectedQuestion=selectedQuestion,
            selectedQuestionID=selectedQuestionID,
        )
    elif request.method == "GET":
        pass


@app.route("/updateQuestion/<selectedQuestionID>", methods=["GET", "POST"])
def updateQuestion(selectedQuestionID):
    if request.method == "POST":
        newQuestionNo = applyescape(request.form["questionNo"])
        newQuestion = applyescape(request.form["question"])
        newQuestionContent = applyescape(request.form["questionContent"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "UPDATE question SET questionNo=%s, question=%s, questionContent=%s WHERE questionID=%s",
            (
                newQuestionNo,
                newQuestion,
                newQuestionContent,
                selectedQuestionID,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("selectedModulePage"))

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/updateTestCaseSelectedQuestionPage", methods=["GET", "POST"])
def updateTestCaseSelectedQuestionPage():
    if request.method == "POST":
        selectedQuestionID = applyescape(request.form["selectedQuestionID"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "SELECT questionNo,question,testCase FROM question,testcases WHERE question.questionID=testcases.questionID AND question.questionID=%s",
            (selectedQuestionID,),
        )
        questionDetails = c.fetchone()

        conn.close()
        ###deneme
        print(questionDetails)
        print(session["courseList"])
        ###deneme

        return render_template(
            "updateTestCase.html",
            questionDetails=questionDetails,
            selectedCourse=session["selectedCourse"],
            selectedModule=session["selectedModule"],
            selectedQuestionID=selectedQuestionID,
        )

    elif request.method == "GET":
        pass


@app.route(
    "/updateTestCaseSelectedQuestion/<selectedQuestionID>", methods=["GET", "POST"]
)
def updateTestCaseSelectedQuestion(selectedQuestionID):
    if request.method == "POST":
        newTestCase = request.form["updateTestCase"]

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "UPDATE testcases SET testCase=%s WHERE questionID=%s",
            (
                newTestCase,
                selectedQuestionID,
            ),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("selectedModulePage"))

    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/deleteCourse", methods=["GET", "POST"])
def deleteCourse():
    if request.method == "POST":
        selectedCourseID = applyescape(request.form["selectedCourseID"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute("DELETE FROM course WHERE courseID=%s", (selectedCourseID,))
        conn.commit()
        conn.close()

        return redirect(url_for("coursesPage"))
    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/deleteModule", methods=["GET", "POST"])
def deleteModule():
    if request.method == "POST":
        selectedModuleID = applyescape(request.form["selectedModuleID"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute("DELETE FROM module WHERE moduleID=%s", (selectedModuleID,))
        conn.commit()
        conn.close()

        return redirect(url_for("selectedCoursePage"))
    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/changeQuestionStatus/<questionStatus>", methods=["GET", "POST"])
def changeQuestionStatus(questionStatus):
    if request.method == "POST":
        selectedQuestionID = applyescape(request.form["selectedQuestionID"])

        print(selectedQuestionID)

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        if questionStatus == "1":
            c.execute(
                "UPDATE question SET questionStatus=%s WHERE questionID=%s",
                (
                    0,
                    selectedQuestionID,
                ),
            )
        else:
            c.execute(
                "UPDATE question SET questionStatus=%s WHERE questionID=%s",
                (
                    1,
                    selectedQuestionID,
                ),
            )
        conn.commit()
        conn.close()

        return redirect(url_for("selectedModulePage"))
    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/deleteQuestion", methods=["GET", "POST"])
def deleteQuestion():
    if request.method == "POST":
        selectedQuestionID = applyescape(request.form["selectedQuestionID"])

        print(selectedQuestionID)

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "UPDATE question SET questionStatus=%s WHERE questionID=%s",
            (
                2,
                selectedQuestionID,
            ),
        )
        conn.commit()
        conn.close()

        return redirect(url_for("selectedModulePage"))
    elif request.method == "GET":
        pass


#######################################################################################################

### Instructor


@app.route("/deleteStudent", methods=["GET", "POST"])
def deleteStudent():
    if request.method == "POST":
        selectedStudentUsername = applyescape(request.form["selectedStudentUsername"])

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        c.execute(
            "DELETE FROM registration WHERE username=%s", (selectedStudentUsername,)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("getStudentList"))
    elif request.method == "GET":
        pass


#######################################################################################################


### Interpreter


@app.route("/pythoncode", methods=["GET", "POST"])
def pythoncode():
    if request.method == "POST":
        txt = "self.assertEqual("
        a = showTestCase()
        fnc_name = a[0][0]
        textcases = ""
        for i in a:
            counter = len(i)
            textcases += "\t\t" + txt + fnc_name + "("
            for j in range(1, len(i) - 1):
                textcases += i[j] + ","
            textcases = textcases[:-1]
            textcases += ")," + i[counter - 1] + ")\n"

        questionID = int(session["studentSelectedQuestionID"])
        username = session["username"]

        code = request.form["code"]
        f = open(("%s.py" % (username)), "w")
        f.write(
            "import unittest\n"
            "%s"
            "\nclass Test(unittest.TestCase):\n"
            "\tdef test(self):\n"
            "%s"
            "if __name__ == '__main__':\n"
            "\tunittest.main()\n" % (code, textcases)
        )
        f.close()

        session["code"] = code
        filePath = "%s.py" % (username)
        command = f"python {filePath}"
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        output, error = process.communicate()
        code_output = ""
        output = str(output)[2:]
        code_output += output
        error = str(error)[2:]
        code_output += str(error)
        code_output = code_output.split("\\r\\n")
        code_output = code_output[:-1]
        session["codeoutput"] = code_output

        conn = mysql.connector.connect(
            host="localhost", port="3306", user="root", database="lap"
        )
        c = conn.cursor()

        errorText = str(error)

        if "OK" in errorText:
            c.execute(
                "SELECT * FROM solution WHERE questionID = %s AND username = %s",
                (
                    questionID,
                    username,
                ),
            )
            flag = c.fetchone()
            if flag == None:
                c.execute(
                    "INSERT INTO solution VALUES (%s, %s, %s, %s)",
                    (
                        questionID,
                        username,
                        1,
                        1,
                    ),
                )
                conn.commit()
            else:
                c.execute(
                    "UPDATE solution SET isSolved = 1 , attempts = attempts + 1 WHERE questionID = %s AND username = %s",
                    (
                        questionID,
                        username,
                    ),
                )
                conn.commit()
        elif "!=" in errorText:
            c.execute(
                "SELECT * FROM solution WHERE questionID = %s AND username = %s",
                (
                    questionID,
                    username,
                ),
            )
            flag = c.fetchone()
            if flag == None:
                c.execute(
                    "INSERT INTO solution VALUES (%s, %s, %s, %s)",
                    (
                        questionID,
                        username,
                        0,
                        1,
                    ),
                )
                conn.commit()
            else:
                c.execute(
                    "UPDATE solution SET isSolved = 0 , attempts = attempts + 1 WHERE questionID = %s AND username = %s",
                    (
                        questionID,
                        username,
                    ),
                )
                conn.commit()

        else:
            c.execute(
                "SELECT * FROM solution WHERE questionID = %s AND username = %s",
                (
                    questionID,
                    username,
                ),
            )
            flag = c.fetchone()
            if flag == None:
                c.execute(
                    "INSERT INTO solution VALUES (%s, %s, %s, %s)",
                    (
                        questionID,
                        username,
                        0,
                        1,
                    ),
                )
                conn.commit()
            else:
                c.execute(
                    "UPDATE solution SET isSolved = 0 , attempts = attempts + 1 WHERE questionID = %s AND username = %s",
                    (
                        questionID,
                        username,
                    ),
                )
                conn.commit()

            if "AssertionError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 1),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            1,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 1),
                    )

            elif "AttributeError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 2),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            2,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 2),
                    )

            elif "FloatingPointError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 3),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            3,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 3),
                    )

            elif "GeneratorExit" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 4),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            4,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 4),
                    )

            elif "ImportError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 5),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            5,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 5),
                    )
            elif "IndexError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 6),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            6,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 6),
                    )

            elif "KeyError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 7),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            7,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 7),
                    )

            elif "KeyboardInterrupt" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 8),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            8,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 8),
                    )

            elif "MemoryError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 9),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            9,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 9),
                    )
            elif "NameError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 10),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            10,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 10),
                    )

            elif "NotImplementedError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 11),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            11,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 11),
                    )
            elif "OSError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 12),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            12,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 12),
                    )

            elif "OverflowError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 13),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            13,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 13),
                    )
            elif "ReferenceError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 14),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            14,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 14),
                    )
            elif "RuntimeError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 15),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            15,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 15),
                    )

            elif "StopIteration" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 16),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            16,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 16),
                    )
            elif "SyntaxError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 17),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            17,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 17),
                    )
            elif "IndentationError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 18),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            18,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 18),
                    )

            elif "TabError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 19),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            19,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 19),
                    )

            elif "SystemError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 20),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            20,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 20),
                    )

            elif "SystemExit" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 21),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            21,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 21),
                    )

            elif "TypeError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 22),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            22,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 22),
                    )

            elif "UnboundLocalError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 23),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            23,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 23),
                    )

            elif "UnicodeError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 24),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            24,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 24),
                    )

            elif "UnicodeEncodeError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 25),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            25,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 25),
                    )

            elif "UnicodeDecodeError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 26),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            26,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 26),
                    )

            elif "UnicodeTranslateError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 27),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            27,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 27),
                    )

            elif "ValueError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 19),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            19,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 28),
                    )

            elif "ZeroDivisionError" in errorText:
                c.execute(
                    "SELECT * FROM solutionexception WHERE questionID = %s AND username = %s AND exceptionID = %s",
                    (questionID, username, 29),
                )
                flag = c.fetchone()
                if flag == None:
                    c.execute(
                        "INSERT INTO solutionexception VALUES (%s, %s, %s, %s)",
                        (
                            questionID,
                            username,
                            29,
                            1,
                        ),
                    )
                else:
                    c.execute(
                        "UPDATE solutionexception SET count = count + 1 WHERE questionID = %s AND username = %s AND exceptionID = %s",
                        (questionID, username, 29),
                    )

        conn.commit()
        conn.close()

        return render_template(
            "studentSelectedQuestion.html",
            codeoutput=session["codeoutput"],
            code=session["code"],
            studentSelectedQuestion=session["studentSelectedQuestion"],
            studentSelectedModule=session["studentSelectedModule"],
            studentSelectedCourse=session["studentSelectedCourse"],
        )

    elif request.method == "GET":
        pass


#######################################################################################################

### Interpreter


@app.route("/showTestCase")
def showTestCase():
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    ###deneme
    if conn.is_connected():
        print("connection is successfull")
    ###deneme

    c.execute(
        "SELECT testCase FROM testcases WHERE questionID=%s",
        (session["studentSelectedQuestionID"],),
    )
    rowtestcase = c.fetchone()

    testCaseList = []

    for i in range(0, len(rowtestcase[0])):
        if rowtestcase[0][i] == "(":
            j = i
            tempList = []
            str = ""
            for j in range(j, len(rowtestcase[0])):
                if rowtestcase[0][j] == "(":
                    pass
                elif rowtestcase[0][j] == ",":
                    tempList.append(str)
                    str = ""

                elif rowtestcase[0][j] == ")":
                    tempList.append(str)
                    testCaseList.append(tuple(tempList))
                    break
                else:
                    str += rowtestcase[0][j]

        elif rowtestcase[0][i] == ",":
            pass
    ###deneme
    print(testCaseList)
    ###deneme
    return testCaseList


#######################################################################################################


### Interpreter


@app.route("/createQuestionReportBarChart/<questionNo>", methods=["GET", "POST"])
def createQuestionReportBarChart(questionNo):
    if request.method == "POST":
        selectedQuestionID = int(escape(request.form["selectedQuestionID"]))

        session["selectedQuestionIDCreateReport"] = selectedQuestionID

        return render_template(
            "questionReportBarChart.html",
            questionNo=questionNo,
            selectedCourse=session["selectedCourse"],
            selectedModule=session["selectedModule"],
        )

    elif request.method == "GET":
        pass


@app.route("/createQuestionReportPieChart/<questionNo>", methods=["GET", "POST"])
def createQuestionReportPieChart(questionNo):
    if request.method == "POST":
        selectedQuestionID = int(escape(request.form["selectedQuestionID"]))

        session["selectedQuestionIDCreateReport"] = selectedQuestionID

        return render_template(
            "questionReportPieChart.html",
            questionNo=questionNo,
            selectedCourse=session["selectedCourse"],
            selectedModule=session["selectedModule"],
        )

    elif request.method == "GET":
        pass


def getException(selectedQuestionIDCreateReport, selectedCharType):
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    exceptions = None

    if selectedCharType == "1":
        c.execute(
            "SELECT * FROM solutionexception WHERE questionID=%s",
            (selectedQuestionIDCreateReport,),
        )
        exceptions = c.fetchall()
    elif selectedCharType == "2":
        c.execute(
            "SELECT solutionexception.* FROM solutionexception INNER JOIN solution ON solutionexception.questionID = solution.questionID AND solutionexception.username = solution.username WHERE solutionexception.questionID = %s AND solution.isSolved = 1 AND solution.attempts BETWEEN 1 AND 5",
            (selectedQuestionIDCreateReport,),
        )
        exceptions = c.fetchall()
    elif selectedCharType == "3":
        c.execute(
            "SELECT solutionexception.* FROM solutionexception INNER JOIN solution ON solutionexception.questionID = solution.questionID AND solutionexception.username = solution.username WHERE solutionexception.questionID = %s AND solution.isSolved = 1 AND solution.attempts BETWEEN 6 AND 10",
            (selectedQuestionIDCreateReport,),
        )

        exceptions = c.fetchall()
    elif selectedCharType == "4":
        c.execute(
            "SELECT solutionexception.* FROM solutionexception INNER JOIN solution ON solutionexception.questionID = solution.questionID AND solutionexception.username = solution.username WHERE solutionexception.questionID = %s AND solution.isSolved = 1 AND solution.attempts > 10",
            (selectedQuestionIDCreateReport,),
        )
        exceptions = c.fetchall()
    elif selectedCharType == "5":
        c.execute(
            "SELECT solutionexception.* FROM solutionexception INNER JOIN solution ON solutionexception.questionID = solution.questionID AND solutionexception.username = solution.username WHERE solutionexception.questionID = %s AND solution.isSolved = 0",
            (selectedQuestionIDCreateReport,),
        )
        exceptions = c.fetchall()
    elif selectedCharType == "6":
        c.execute(
            "SELECT se.* FROM solutionexception se JOIN solution s ON se.username = s.username JOIN question q ON s.questionID = q.questionID JOIN attendance a ON s.username = a.username AND q.moduleID = a.moduleID WHERE se.questionID = %s AND a.attended = 1",
            (selectedQuestionIDCreateReport,),
        )
        exceptions = c.fetchall()
    elif selectedCharType == "7":
        c.execute(
            "SELECT se.* FROM solutionexception se JOIN solution s ON se.username = s.username JOIN question q ON s.questionID = q.questionID JOIN attendance a ON s.username = a.username AND q.moduleID = a.moduleID WHERE se.questionID = %s AND a.attended = 0",
            (selectedQuestionIDCreateReport,),
        )
        exceptions = c.fetchall()

    exceptionsTepmList = []
    exceptionsTempCount = []
    for exception in exceptions:
        c.execute("SELECT * FROM exception WHERE exceptionID = %s", (exception[2],))
        exceptionName = c.fetchone()
        exceptionsTepmList.append(exceptionName[1])
        exceptionsTempCount.append(exception[3])

    exceptionsList = []
    exceptionsCount = []
    i = 0
    for exception in exceptionsTepmList:
        if exception in exceptionsList:
            j = 0
            for subException in exceptionsList:
                if subException == exception:
                    exceptionsCount[j] = exceptionsCount[j] + exceptionsTempCount[i]
                j = j + 1

        else:
            exceptionsList.append(exception)
            exceptionsCount.append(exceptionsTempCount[i])
        i = i + 1

    exceptionsList.append(exceptionsCount)
    return exceptionsList


@app.route("/gethint", methods=["GET"])
def gethint():
    selectedCharType = request.args.get("q")

    selectedQuestionIDCreateReport = session["selectedQuestionIDCreateReport"]
    exceptionList = getException(
        selectedQuestionIDCreateReport=selectedQuestionIDCreateReport,
        selectedCharType=selectedCharType,
    )
    return exceptionList


#######################################################################################################


### Interpreter


@app.route("/createModuleBarReport/<selectedModule>", methods=["GET", "POST"])
def createModuleBarReport(selectedModule):
    if request.method == "POST":
        selectedModuleID = applyescape(request.form["selectedModuleID"])
        session["selectedModuleID"] = selectedModuleID

        return render_template(
            "createModuleBarReport.html",
            selectedCourse=session["selectedCourse"],
            selectedModule=selectedModule,
        )

    elif request.method == "GET":
        pass


@app.route("/createModulePieReport/<selectedModule>", methods=["GET", "POST"])
def createModulePieReport(selectedModule):
    if request.method == "POST":
        selectedModuleID = applyescape(request.form["selectedModuleID"])
        session["selectedModuleID"] = selectedModuleID

        return render_template(
            "createModulePieReport.html",
            selectedCourse=session["selectedCourse"],
            selectedModule=selectedModule,
        )

    elif request.method == "GET":
        pass


@app.route("/gethintTwo", methods=["GET"])
def gethintTwo():
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    selectedModuleIDCreateReport = session["selectedModuleID"]

    c.execute(
        "SELECT solutionexception.questionID,solutionexception.username,solutionexception.exceptionID,solutionexception.count FROM solutionexception,question WHERE question.questionID=solutionexception.questionID AND question.moduleID=%s",
        (selectedModuleIDCreateReport,),
    )
    exceptions = c.fetchall()

    exceptionsTepmList = []
    exceptionsTempCount = []
    for exception in exceptions:
        c.execute("SELECT * FROM exception WHERE exceptionID = %s", (exception[2],))
        exceptionName = c.fetchone()
        exceptionsTepmList.append(exceptionName[1])
        exceptionsTempCount.append(exception[3])

    exceptionsList = []
    exceptionsCount = []
    i = 0
    for exception in exceptionsTepmList:
        if exception in exceptionsList:
            j = 0
            for subException in exceptionsList:
                if subException == exception:
                    exceptionsCount[j] = exceptionsCount[j] + exceptionsTempCount[i]
                j = j + 1

        else:
            exceptionsList.append(exception)
            exceptionsCount.append(exceptionsTempCount[i])
        i = i + 1

    exceptionsList.append(exceptionsCount)

    return exceptionsList


###################################################################

### Interpreter


@app.route("/createCourseBarReport/<selectedCourse>", methods=["GET", "POST"])
def createCourseBarReport(selectedCourse):
    if request.method == "POST":
        selectedCourseID = applyescape(request.form["selectedCourseID"])
        session["selectedCourseID"] = selectedCourseID

        return render_template(
            "createCourseBarReport.html", selectedCourse=selectedCourse
        )

    elif request.method == "GET":
        pass


@app.route("/createCoursePieReport/<selectedCourse>", methods=["GET", "POST"])
def createCoursePieReport(selectedCourse):
    if request.method == "POST":
        selectedCourseID = applyescape(request.form["selectedCourseID"])
        session["selectedCourseID"] = selectedCourseID

        return render_template(
            "createCoursePieReport.html", selectedCourse=selectedCourse
        )

    elif request.method == "GET":
        pass


@app.route("/gethintThree", methods=["GET"])
def gethintThree():
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    selectedCourseIDCreateReport = session["selectedCourseID"]

    c.execute(
        "SELECT solutionexception.questionID,solutionexception.username,solutionexception.exceptionID,solutionexception.count FROM solutionexception,question,module WHERE question.questionID=solutionexception.questionID AND question.moduleID=module.moduleID AND module.courseID=%s",
        (selectedCourseIDCreateReport,),
    )
    exceptions = c.fetchall()

    exceptionsTepmList = []
    exceptionsTempCount = []
    for exception in exceptions:
        c.execute("SELECT * FROM exception WHERE exceptionID = %s", (exception[2],))
        exceptionName = c.fetchone()
        exceptionsTepmList.append(exceptionName[1])
        exceptionsTempCount.append(exception[3])

    exceptionsList = []
    exceptionsCount = []
    i = 0
    for exception in exceptionsTepmList:
        if exception in exceptionsList:
            j = 0
            for subException in exceptionsList:
                if subException == exception:
                    exceptionsCount[j] = exceptionsCount[j] + exceptionsTempCount[i]
                j = j + 1

        else:
            exceptionsList.append(exception)
            exceptionsCount.append(exceptionsTempCount[i])
        i = i + 1

    exceptionsList.append(exceptionsCount)

    return exceptionsList


###################################################################

### Interpreter


@app.route(
    "/createStudentBarChart/<studentName>,<studentSurname>", methods=["GET", "POST"]
)
def createStudentBarChart(studentName, studentSurname):
    if request.method == "POST":
        selectedStudentUsername = applyescape(request.form["selectedStudentUsername"])
        session["selectedStudentUsername"] = selectedStudentUsername

        return render_template(
            "createStudentBarReport.html",
            selectedCourse=session["selectedCourse"],
            studentName=studentName,
            studentSurname=studentSurname,
        )

    elif request.method == "GET":
        pass


@app.route(
    "/createStudentPieChart/<studentName>,<studentSurname>", methods=["GET", "POST"]
)
def createStudentPieChart(studentName, studentSurname):
    if request.method == "POST":
        selectedStudentUsername = applyescape(request.form["selectedStudentUsername"])
        session["selectedStudentUsername"] = selectedStudentUsername

        return render_template(
            "createStudentPieReport.html",
            selectedCourse=session["selectedCourse"],
            studentName=studentName,
            studentSurname=studentSurname,
        )

    elif request.method == "GET":
        pass


@app.route("/gethintFour", methods=["GET"])
def gethintFour():
    conn = mysql.connector.connect(
        host="localhost", port="3306", user="root", database="lap"
    )
    c = conn.cursor()

    selectedCourseID = session["selectedCourseID"]

    selectedStudentUsername = session["selectedStudentUsername"]

    c.execute(
        "SELECT solutionexception.questionID,solutionexception.username,solutionexception.exceptionID,solutionexception.count FROM solutionexception,question,registration WHERE registration.username=solutionexception.username AND question.questionID=solutionexception.questionID AND registration.courseID=%s AND solutionexception.username=%s",
        (
            selectedCourseID,
            selectedStudentUsername,
        ),
    )
    exceptions = c.fetchall()

    print("*******************************************************")
    print(exceptions)

    exceptionsTepmList = []
    exceptionsTempCount = []
    for exception in exceptions:
        c.execute("SELECT * FROM exception WHERE exceptionID = %s", (exception[2],))
        exceptionName = c.fetchone()
        exceptionsTepmList.append(exceptionName[1])
        exceptionsTempCount.append(exception[3])

    exceptionsList = []
    exceptionsCount = []
    i = 0
    for exception in exceptionsTepmList:
        if exception in exceptionsList:
            j = 0
            for subException in exceptionsList:
                if subException == exception:
                    exceptionsCount[j] = exceptionsCount[j] + exceptionsTempCount[i]
                j = j + 1

        else:
            exceptionsList.append(exception)
            exceptionsCount.append(exceptionsTempCount[i])
        i = i + 1

    exceptionsList.append(exceptionsCount)

    return exceptionsList


#######################################################################################

if __name__ == "__main__":
    app.run(debug=True)
