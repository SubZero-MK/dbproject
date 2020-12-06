from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import mysql.connector as sqlconn

conn = sqlconn.connect(host='localhost', user='root', passwd='Counter123', database='quest')
#conn = sqlconn.connect(host='sql212.epizy.com', user='epiz_27348819	', passwd='X8hSATETooX9R', database='epiz_27348819_quest')

#H(0mL7z*|{Y~P&7y
#conn.set_charset_collation('latin1', 'latin1_general_ci')
mycursor = conn.cursor()
#mycursor.execute("SELECT * FROM loginTable")
#result = mycursor.fetchall()

#COMPILICATIONS TO HANDLE NEXT
#The introduction of sections as course IDs-- need to cater the unique ID as well when new course is being added

#IDEAS:
#Promotion by department heads
#Teacher assigning grade components of their students
#After assigning the grades and on the approval of database manager, the semester will end and the grades will be counted towards GPA and total credit hours of teachers

#For Every User
#--------------------------------------------------------------------------------------------------------------------------------------------
def displayInfo(ID): #User case to display the personal information of the person who logged in
	sqlcommand = None
	if ID//10000 == 1:
		sqlcommand = "SELECT id, name_, gpa, total_credit_hours, year_, major FROM student WHERE id = " + str(ID) + ";"
	elif ID//10000 == 2:
		sqlcommand = "SELECT id, name_, department_name, salary, post FROM teacher WHERE id = " + str(ID) + ";"
	elif ID//10000 == 3:
		sqlcommand = "SELECT id, name_, office_under, salary, post FROM worker WHERE id = " + str(ID) + ";"

	mycursor.execute(sqlcommand)
	displayWindow = Toplevel()
	ButtonCloseDisplay = Button(displayWindow, text='Ok', command=displayWindow.destroy)
	display = None

	displayInfoResult = mycursor.fetchone()
	if ID//10000 == 1:
		(sID, name_, gpa, total_credit_hours, year_, major) = displayInfoResult
		display = 'ID: ' + str(sID) + '\nName: ' + name_ + '\nGPA: ' + str(gpa) + '\nTotal Credit Hours: ' + str(total_credit_hours) + '\nYear: ' + year_ + '\nMajor: ' + major
	elif ID//10000 == 2:
		(tID, name_, department_name, salary, post) = displayInfoResult
		display = 'ID: ' + str(tID) + '\nName: ' + name_ + '\nDepartment Name: ' + department_name + '\nSalary: ' + str(salary) + '\nPost: ' + post
	elif ID//10000 == 3:
		(wID, name_, office, salary, post) = displayInfoResult
		display = 'ID: ' + str(wID) + '\nName: ' + name_ + '\nOffice: ' + office + '\nSalary: ' + str(salary) + '\nPost: ' + post 

	displayLabel = Label(displayWindow, text=display)	
	displayLabel.grid(row=0, column=0, padx=5, pady=5)
	ButtonCloseDisplay.grid(row=1, column=1, columnspan=5, rowspan=5, padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------------------------------------------

#User case for the password change
def passwordChange(ID, pw, topWindow, root): #Opens the window for input fields
	passwordWindow = Toplevel()

	currentPasswordLabel = Label(passwordWindow, text='Enter Current Password: ')
	currentPasswordLabel.grid(row=0, column=0, padx=5, pady=5)
	currentPasswordField = Entry(passwordWindow, width=30)
	currentPasswordField.grid(row=0, column=1, padx=5, pady=5)

	newPasswordLabel = Label(passwordWindow, text='Enter New Password: ')
	newPasswordLabel.grid(row=1, column=0, padx=5, pady=5)
	newPasswordField = Entry(passwordWindow, width=30)
	newPasswordField.grid(row=1, column=1, padx=5, pady=5)

	ButtonNewPassword = Button(passwordWindow, text='Change Password', command=lambda:changePassword(ID, passwordWindow, currentPasswordField, newPasswordField, pw, root))
	ButtonNewPassword.grid(row=2, column=0, padx=5, pady=5)

def changePassword(ID, passwordWindow, currentPasswordField, newPasswordField, pw, root): #Takes the input of the fields and changes the password accordingly
	currentpw = currentPasswordField.get()
	newpw = newPasswordField.get()
	display = None
	canChange = False
	if currentpw != pw:
		display = 'The entered current password is not right.'
	else:
		canChange = True
		display = 'Your password is changed. You have to login again with your new password'

	if canChange == True:
		sqlcommand = "UPDATE loginTable SET pw = (%s) WHERE id = (%s)"
		vals = (newpw, ID)
		mycursor.execute(sqlcommand, vals)
		conn.commit()
		pw = newpw
		ButtonClosePasswordWindow = Button(passwordWindow, text=display, command=lambda:destroy_all(root))
	else:
		ButtonClosePasswordWindow = Button(passwordWindow, text=display, command=passwordWindow.destroy)
	ButtonClosePasswordWindow.grid(row=3, column=0, padx=5, pady=5)

#Specifically for teachers
#--------------------------------------------------------------------------------------------------------------------------------------------
def ChangeCourseComponent(ID, root): #To change the grading components of a course
	sqlcommand = "SELECT course_title FROM course_teacher_map WHERE teacher_id = " + str(ID) + ";"
	mycursor.execute(sqlcommand)
	sqlexecutionResult = mycursor.fetchall()
	taughtCoursesList = []
	for i in  range(len(sqlexecutionResult)):
		(course, ) = sqlexecutionResult[i]
		taughtCoursesList.append(course)

	courseWindow = Toplevel()
	for i in range(len(taughtCoursesList)):
		cur_Button = Button(courseWindow, text=taughtCoursesList[i], command=lambda course=taughtCoursesList[i]:OpenCourseEntryBoxes(ID, course, courseWindow))
		cur_Button.grid(row=i, column=0, padx=5, pady=5)

def OpenCourseEntryBoxes(ID, taughtCourse, courseWindow): #Opening the course entry boxes that will take the input
	print('Selected course: ' + taughtCourse)
	EntryBoxWindow = Toplevel()
	ComponentList = ['CP:', 'Assignment:', 'Quiz:', 'MidTerm:', 'Final:']
	EntryBoxList = []
	for i in range(5):
		curLabel = Label(EntryBoxWindow, text=ComponentList[i])
		curLabel.grid(row=i, column=0, padx=5, pady=5)
		cur_EntryBox = Entry(EntryBoxWindow, width=10)
		EntryBoxList.append(cur_EntryBox)
		cur_EntryBox.grid(row=i, column=1, padx=5,pady=5)

	ButtonSubmit = Button(EntryBoxWindow, text='Submit', command=lambda:getDataFromEntryBoxes(EntryBoxList, taughtCourse, courseWindow, EntryBoxWindow))
	ButtonSubmit.grid(row=6, column=1, padx=5, pady=5)

def getDataFromEntryBoxes(entryBoxList, taughtCourse, courseWindow, EntryBoxWindow): #Evaluate data from the inputs in the entry boxes
	vals = []
	CountCheck = 0
	for i in range(len(entryBoxList)):
		x = entryBoxList[i].get()
		val = int(x)
		CountCheck += val
		vals.append(val)

	for i in vals:
		if i < 0 or i > 100:
			ErrorWindow = Toplevel()
			ButtonErrorShow = Button(ErrorWindow, text='Graded component cannot be negative or more than 100.\nClick the button to proceed.', command=ErrorWindow.destroy)
			ButtonErrorShow.grid(row=0, column=0, padx=5, pady=5)
			break

	if CountCheck != 100:
		ErrorWindow = Toplevel()
		ButtonErrorShow = Button(ErrorWindow, text='Sum of course components should be 100.\nClick the button to proceed', command=ErrorWindow.destroy)
		ButtonErrorShow.grid(row=0, column=0, padx=5, pady=5)
	else:
		sqlcommand = '''UPDATE course
						SET cp_component = %s, assignment_component = %s, quiz_component = %s, midterm_component = %s, final_component = %s
						WHERE title = %s;'''
		values = (vals[0], vals[1], vals[2], vals[3], vals[4], taughtCourse)
		mycursor.execute(sqlcommand, values)
		conn.commit()
		NotificationWindow = Toplevel()
		ButtonNotification = Button(NotificationWindow, text='Changes have been made.\nPress the button to move the main menu.', command=lambda:deleteThreeWindows(NotificationWindow,EntryBoxWindow, courseWindow))
		ButtonNotification.grid(row=0, column=0, padx=0, pady=0)
#--------------------------------------------------------------------------------------------------------------------------------------------

def assigningGrades(ID): #Assigning grade to students
	sqlcommand = '''SELECT pop.student_id, pop.course_title, student.name_, pop.c_id
					FROM (	SELECT student_id, course_teacher_map.course_title, teacher_id, course_teacher_map.c_id
						  	FROM course_teacher_map, student_course_map
					     	WHERE course_teacher_map.course_title = student_course_map.course_title
							AND course_teacher_map.c_id = student_course_map.c_id) AS pop, student
					WHERE pop.teacher_id = %s AND pop.student_id = student.id;'''	#sql query to fetch the students that a specific teacher teaches

	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	taughtStudents = mycursor.fetchall()
	numOfStudents = len(taughtStudents)

	buttonWindow = Toplevel() #A window that will include the buttons of individual students of the teacher

	for i in range(numOfStudents):
		(studentID, course, sname, cID) = taughtStudents[i]
		scTuple = (studentID, course, cID) #Student-Course tuple - mainly for binding with the function argument
		cur_Button = Button(buttonWindow, text=str(studentID) + ":" + sname + ':' + course, command=lambda scTup=scTuple:OpenGradeBox(ID, scTup, buttonWindow))
		cur_Button.grid(row=i, column=0, padx=5, pady=5)

def OpenGradeBox(ID, scTuple, buttonWindow): #scTuple = Student-Course tuple
	GradeWindow = Toplevel()
	GradeLabel = Label(GradeWindow, text='Enter grade of the student: ')
	GradeLabel.grid(row=0, column=0, padx=5, pady=5)
	GradeBox = Entry(GradeWindow, width=5)
	GradeBox.grid(row=0, column=1, padx=5, pady=5)

	ButtonSubmit = Button(GradeWindow, text='Enter', command=lambda:assignTheGrade(GradeBox, GradeWindow, scTuple, buttonWindow))
	ButtonSubmit.grid(row=1, column=1, padx=5, pady=5)

def assignTheGrade(GradeBox, GradeWindow, scTuple, buttonWindow): #Insert the grade of the student now
	grade = GradeBox.get()
	(sID, c, cID) = scTuple #Breaking down the tuple back
	sqlcommand = '''UPDATE student_course_map
					SET grade = %s
					WHERE student_id = %s AND course_title = %s AND c_id = %s;'''
	vals = (grade, sID, c, cID)
	mycursor.execute(sqlcommand, vals)
	conn.commit()
	NotificationWindow = Toplevel()
	exitButton = Button(NotificationWindow, text='Changes have been made.\nPress the button to proceed',command=lambda:deleteThreeWindows(NotificationWindow, GradeWindow, buttonWindow))
	exitButton.grid(row=0, column=0,padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------------------------------------------

def displayDepartmentTeachers(ID):	#Only heads of departments (HODs) have access to the function
	sqlcommand = "SELECT post FROM teacher WHERE id = %s;" #Query to check the post of the teacher
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	tPost = mycursor.fetchone()
	(tPost, ) = tPost

	tDispWindow = Toplevel()

	if tPost != 'HOD':
		notificationButton = Button(tDispWindow, text='You do not have access to the command.\nPress the button to proceed.', command=tDispWindow.destroy)
		notificationButton.grid(row=0, column=0, padx=5, pady=5)
	else:
		getListofDeptTeacher = "SELECT * FROM teacher WHERE department_name = (SELECT department_name FROM teacher WHERE id = %s);" #SQL query to get all the instructors of the department
		mycursor.execute(getListofDeptTeacher, vals)
		tTable = mycursor.fetchall()
		numOfTeachers = len(tTable)

		tTuple = None
		for i in range(numOfTeachers):
			(tid, tname, tdept, tsalary, tpost) = tTable[i]
			tid = str(tid)
			tsalary = str(tsalary)

			tTuple = tid + '\t' + tname + '\t' + tdept + '\t' + tsalary + '\t' + tpost
			curLabel = Label(tDispWindow, text='#' + str(i) + '\t' + tTuple)
			curLabel.grid(row=i, column=0, padx=5, pady=5)

		exitButton = Button(tDispWindow, text='Exit', command=tDispWindow.destroy)
		exitButton.grid(row=numOfTeachers+1, column=numOfTeachers//2, padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------------------------------------------

#Specifically for database managers:
def addCourse():
	courseNewWindow = Toplevel()

	courseInfoLabel = Label(courseNewWindow, text='Insert info of the new course: ')
	courseInfoLabel.grid(row=0, column=0, padx=5, pady=5)

	courseTitleLabel = Label(courseNewWindow, text='Title: ')
	courseTitleLabel.grid(row=1, column=0, padx=5, pady=5)
	courseTitleField = Entry(courseNewWindow, width=25)
	courseTitleField.grid(row=1, column=1, padx=5, pady=5)
	courseIDLabel = Label(courseNewWindow, text='ID: ')
	courseIDLabel.grid(row=2, column=0, padx=5, pady=5)
	courseIDField = Entry(courseNewWindow, width=25)
	courseIDField.grid(row=2, column=1, padx=5, pady=5)
	courseDeptLabel = Label(courseNewWindow, text= 'Department: ')
	courseDeptLabel.grid(row=3, column=0, padx=5, pady=5)
	courseDeptField = Entry(courseNewWindow, width=25)
	courseDeptField.grid(row=3, column=1, padx=5, pady=5)
	courseCHLabel = Label(courseNewWindow, text= 'Credit Hours: ') #CH = Credit Hour
	courseCHLabel.grid(row=4, column=0, padx=5, pady=5)
	courseCHField = Entry(courseNewWindow, width=25)
	courseCHField.grid(row=4, column=1, padx=5, pady=5)

	courseDataInputButton = Button(courseNewWindow, text='Enter', command=lambda:getDataFromCourseBoxes(courseTitleField, courseIDField, courseDeptField, courseCHField, courseNewWindow))
	courseDataInputButton.grid(row=5, column=1, padx=5, pady=5)

def getDataFromCourseBoxes(cT, cI, cD, cC, window): #cT=courseTitleBox, cI=courseIDBox, cD=courseDeptBox, cC=courseCHBox
	cTitle = cT.get()
	cTitle = (cTitle, )
	sqlcommandcTcheck = "SELECT COUNT(title) FROM course WHERE title = %s LIMIT 0,1;"
	mycursor.execute(sqlcommandcTcheck, cTitle)
	courseUniqueCheck = mycursor.fetchone()
	(courseUniqueCheck, ) = courseUniqueCheck

	courseUniqueCheck = int(courseUniqueCheck)

	UniqueCheck = False
	if courseUniqueCheck == 1:
		ErrorWindow = Toplevel()
		ButtonErrorShow = Button(ErrorWindow, text='There is already a course of same title.\nClick the button to proceed', command=ErrorWindow.destroy)
		ButtonErrorShow.grid(row=0, column=0, padx=5, pady=5)
		UniqueCheck = False
	else:
		UniqueCheck = True

	cDept = cD.get()
	cDept = (cDept, )
	sqlcommandcDcheck = "SELECT COUNT(department_in) FROM course WHERE department_in = %s LIMIT 0, 1;"
	mycursor.execute(sqlcommandcDcheck, cDept)
	courseDeptCheck = mycursor.fetchone()
	(courseDeptCheck, ) = courseDeptCheck

	courseDeptCheck = int(courseDeptCheck)

	DeptCheck = False
	if courseDeptCheck == 0:
		ErrorWindow = Toplevel()
		ButtonErrorShow = Button(ErrorWindow, text='Department not found.\nClick the button to proceed', command=ErrorWindow.destroy)
		ButtonErrorShow.grid(row=0, column=0, padx=5, pady=5)
		DeptCheck = False
	else:
		DeptCheck = True

	if DeptCheck == True and UniqueCheck == True:
		cIDee = cI.get()
		cCHours = cC.get()

		dGC = '20' #Default Grade Component
		sqlcommand = "INSERT INTO course VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
		(cDept, ) = cDept
		(cTitle, ) = cTitle
		vals = (cTitle, cIDee, cDept, cCHours, dGC, dGC, dGC, dGC, dGC)
		mycursor.execute(sqlcommand, vals)
		conn.commit()

		NotificationWindow = Toplevel()
		ButtonNotification = Button(NotificationWindow, text='Course has been added.\nClick the button to proceed', command=lambda:deleteTwoWindows(NotificationWindow, window))
		ButtonNotification.grid(row=0, column=0, padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------------------------------------------
def displayAllCourses():
	courseDisplayWindow = Toplevel()
	sqlcommand = '''SELECT * FROM course;'''	#To fetch all courses in form of tuples
	sqlcommandNumofCourses = "SELECT COUNT(*) FROM course;"	#To get the total number of courses in the course table
	mycursor.execute(sqlcommand)	
	cTable = mycursor.fetchall()	#Has all the tuples from the table
	mycursor.execute(sqlcommandNumofCourses) 
	numOfCourses = mycursor.fetchone()	#Fetching the total number of courses
	(numOfCourses, ) = numOfCourses
	numOfCourses = int(numOfCourses)	#Converting the fetched data to int
	cTuple = None #For display in label; cTuple = courseTuple
	for i in range(numOfCourses):
		(ctitle, cid, cdept, cch, g1, g2, g3, g4, g5) = cTable[i]
		cid = str(cid)
		cch = str(cch)
		g1 = str(g1)
		g2 = str(g2)
		g3 = str(g3)
		g4 = str(g4)
		g5 = str(g5)

		cTuple = ctitle + '\t' + cid + '\t' + cdept + '\t' + cch + '\t' + g1 + '\t' + g2 + '\t' + g3 + '\t' + g4 + '\t' + g5
		curLabel = Label(courseDisplayWindow, text='#' + str(i) + '\t' + cTuple)
		curLabel.grid(row=i, column=0, padx=5, pady=5)

	windowCloseButton = Button(courseDisplayWindow, text='Exit', command=courseDisplayWindow.destroy)
	windowCloseButton.grid(row=numOfCourses+1, column=numOfCourses//2, padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------------------------------------------
def displayAllStudents():
	studentDisplayWindow = Toplevel()
	sqlcommand = '''SELECT * FROM student;'''

	mycursor.execute(sqlcommand)
	sTable = mycursor.fetchall()
	numOfStudents = len(sTable)

	sTuple = None 
	for i in range(numOfStudents):
		(sid, sname, sgpa, stch, syear, smajor) = sTable[i]
		sid = str(sid)
		sgpa = str(sgpa)
		stch = str(stch)

		sTuple = sid + '\t' + sname + '\t\t' + sgpa + '\t\t' + stch + '\t\t' + syear + '\t\t' + smajor
		curLabel = Label(studentDisplayWindow, text='#' + str(i) + '\t' + sTuple)
		curLabel.grid(row=i, column=0, padx=5, pady=5)

	windowCloseButton = Button(studentDisplayWindow, text='Exit', command=studentDisplayWindow.destroy)
	windowCloseButton.grid(row=numOfStudents+1, column=numOfStudents//2, padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------------------------------------------
def displayAllTeachers():
	teacherDisplayWindow = Toplevel()
	sqlcommand = "SELECT * FROM teacher;"

	mycursor.execute(sqlcommand)
	tTable = mycursor.fetchall()
	numOfTeachers = len(tTable)

	tTuple = None
	for i in range(numOfTeachers):
		(tid, tname, tdept, tsalary, tpost) = tTable[i]
		tid = str(tid)
		tsalary = str(tsalary)

		tTuple = tid + '\t' + tname + '\t' + tdept + '\t' + tsalary + '\t' + tpost
		curLabel = Label(teacherDisplayWindow, text='#' + str(i) + '\t' + tTuple)
		curLabel.grid(row=i, column=0, padx=5, pady=5)

	windowCloseButton = Button(teacherDisplayWindow, text='Exit', command=teacherDisplayWindow.destroy)
	windowCloseButton.grid(row=numOfTeachers+1, column=numOfTeachers//2, padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------------------------------------------
def setEnrollmentTimer(): #When students are allowed to enroll for new courses
	activationWindow = Toplevel()
	sqlcommand = 'SELECT timer FROM enrollment_timer;'
	mycursor.execute(sqlcommand)
	currentTimer = mycursor.fetchone()
	(currentTimer, ) = currentTimer

	activationButton = Button(activationWindow, text='Activate Enrollment', command=lambda:ActivateEnroll(currentTimer, activationWindow))
	activationButton.grid(row=0, column=0, padx=5, pady=5)
	deactivationButton = Button(activationWindow, text='Deactivate Enrollment', command=lambda:DeactivateEnroll(currentTimer, activationWindow))
	deactivationButton.grid(row=1, column=0, padx=5, pady=5)

def ActivateEnroll(cT, acW):
	NotificationWindow = Toplevel()
	if cT == 1:
		actButton = Button(NotificationWindow, text='The Enrollment timer is already active.\nClick the button to proceed. ', command=NotificationWindow.destroy)
		actButton.grid(row=0, column=0, padx=5, pady=5)
	if cT == 0:
		sqlcommand = 'UPDATE enrollment_timer SET timer = 1;'
		mycursor.execute(sqlcommand)
		conn.commit()
		actButton = Button(NotificationWindow, text='The Enrollment timer is now active.\nClick the button to proceed. ', command=lambda:deleteTwoWindows(NotificationWindow, acW))
		actButton.grid(row=0, column=0, padx=5, pady=5)

def DeactivateEnroll(cT, acW):
	NotificationWindow = Toplevel()
	if cT == 0:
		actButton = Button(NotificationWindow, text='The Enrollment timer is already not active.\nClick the button to proceed. ', command=NotificationWindow.destroy)
		actButton.grid(row=0, column=0, padx=5, pady=5)
	if cT == 1:
		sqlcommand = 'UPDATE enrollment_timer SET timer = 0;'
		mycursor.execute(sqlcommand)
		conn.commit()
		actButton = Button(NotificationWindow, text='The Enrollment timer is now deactivated.\nClick the button to proceed. ', command=lambda:deleteTwoWindows(NotificationWindow, acW))
		actButton.grid(row=0, column=0, padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------------------------------------------


#For students
def studentFunction(topWindow, ID, pw, root):
	ButtonDisplayInfo = Button(topWindow, text='Display Personal Information', command=lambda:displayInfo(ID))
	ButtonDisplayInfo.grid(row=0, column=0, padx=5, pady=5)
	ButtonPasswordChange = Button(topWindow, text='Change Password', command=lambda:passwordChange(ID, pw, topWindow, root))
	ButtonPasswordChange.grid(row=1, column=0, padx=5, pady=5)

#For teachers
def teacherFunction(topWindow, ID, pw, root):
	ButtonDisplayInfo = Button(topWindow, text='Display Personal Information', command=lambda:displayInfo(ID))
	ButtonDisplayInfo.grid(row=0,column=0, padx=5, pady=5)
	ButtonPasswordChange = Button(topWindow, text='Change Password', command=lambda:passwordChange(ID, pw, topWindow, root))
	ButtonPasswordChange.grid(row=1, column=0, padx=5, pady=5)
	ButtonCourseComponent = Button(topWindow, text='Change Course Grading Components', command=lambda:ChangeCourseComponent(ID, root))
	ButtonCourseComponent.grid(row=2, column=0, padx=5, pady=5)
	ButtonDisplayDepartmentTeachers = Button(topWindow, text='Display Teachers of your Department', command=lambda:displayDepartmentTeachers(ID))
	ButtonDisplayDepartmentTeachers.grid(row=3, column=0, padx=5, pady=5)
	ButtonGradeAssignment = Button(topWindow, text='Assign Grades to your Students', command=lambda:assigningGrades(ID))
	ButtonGradeAssignment.grid(row=4, column=0, padx=5, pady=5)

#For workers
def workerFunction(topWindow, ID, pw, root):
	ButtonDisplayInfo = Button(topWindow, text = 'Display Personal Information', command=lambda:displayInfo(ID))
	ButtonDisplayInfo.grid(row=0, column=0, padx=5, pady=5)

#For database manager
def managerFunction(topWindow, ID, pw, root):
	ButtonAddCourse = Button(topWindow, text = 'Add Course in the Course List', command=addCourse)
	ButtonAddCourse.grid(row=0, column=0, padx=5, pady=5)
	ButtonDisplayCourses = Button(topWindow, text = 'Display details of all the Courses', command=displayAllCourses)
	ButtonDisplayCourses.grid(row=1, column=0, padx=5, pady=5)
	ButtonDisplayStudents = Button(topWindow, text = 'Display details of all students', command=displayAllStudents)
	ButtonDisplayStudents.grid(row=2, column=0, padx=5, pady=5)
	ButtonDisplayTeachers = Button(topWindow, text = 'Display details of all teachers', command=displayAllTeachers)
	ButtonDisplayTeachers.grid(row=3, column=0, padx=5, pady=5)
	ButtonActivateEnrollment = Button(topWindow, text = 'Activate/Deactivate Enrollment for Students', command=setEnrollmentTimer)
	ButtonActivateEnrollment.grid(row=4, column=0, padx=5, pady=5)

#--------------------------------------------------------------------------------------------------------------------------------------------

#Helper functions
def deleteThreeWindows(win1, win2, win3):
	win1.destroy()
	win2.destroy()
	win3.destroy()
def destroy_all(root): #To destroy all toplevel windows
    for widget in root.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()
def deleteTwoWindows(w1, w2):
	w1.destroy();
	w2.destroy();

#--------------------------------------------------------------------------------------------------------------------------------------------

#For login
def getLogin(root, IDField, PasswordField):
	ID = IDField.get()
	ID = int(ID)
	pw = PasswordField.get()

	sqlcommand = "SELECT COUNT(%s) FROM loginTable WHERE id = %s AND pw = %s;"
	vals = (ID, ID, pw)
	mycursor.execute(sqlcommand, vals)

	loginBool = False
	loginNotification = 'Invalid Login'

	loginResult = mycursor.fetchone()
	(loginResult, ) = loginResult
	if loginResult == 1:
		loginBool = True
		topWindow = Toplevel()
		loginNotification = 'User Logged in'

	if loginBool == True and ID//10000 == 1:
		print('Student: ID', ID, 'logged in.')
		studentFunction(topWindow, ID, pw, root)
	elif loginBool == True and ID//10000 == 2:
		print('Teacher: ID', ID, 'logged in.')
		teacherFunction(topWindow, ID, pw, root)
	elif loginBool == True and ID//10000 == 3:
		print('Worker: ID', ID, 'logged in.')
		workerFunction(topWindow, ID, pw, root)
	elif loginBool == True and ID//10000 == 4:
		print('Manager: ID', ID, 'logged in.')
		managerFunction(topWindow, ID, pw, root)
	else:
		print('Invalid Login')

	loginLabel = Label(root, text = loginNotification, style = 'BW.TLabel')
	loginLabel.grid(row=3, column=1, padx=5, pady=5)

def main():

	root = Tk()
	root.title('Login')

	#Styling for Labels and Buttons on login table
	styleLabel = ttk.Style()
	styleLabel.configure('BW.TLabel', font = ('times new roman', 13, 'bold', 'underline'), foreground = 'dark green')

	styleButton = ttk.Style()
	styleButton.configure('BW.TButton', font = ('times new roman', 14, 'bold'), foreground = 'blue')

	#Creating username input field
	IDLabel = Label(root, text='ID: ', style = 'BW.TLabel')
	IDLabel.grid(row=0, column=0, padx=5, pady=5)
	IDField = Entry(root, width=25)
	IDField.grid(row=0, column=1, padx=5, pady=5)

	#Creating password input field
	PasswordLabel = Label(root, text='Password: ', style = 'BW.TLabel')
	PasswordLabel.grid(row=1, column=0, padx=5, pady=5)
	PasswordField = Entry(root, width=25)
	PasswordField.grid(row=1, column=1, padx=5, pady=5)

	#Creating a button to get the login
	LoginButton = Button(root, text='Login', style = 'BW.TButton', command=lambda: getLogin(root, IDField, PasswordField))
	LoginButton.grid(row=2, column=1, padx=10, pady=10)

	root.mainloop()

main()

conn.close()