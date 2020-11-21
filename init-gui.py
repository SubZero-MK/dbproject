from tkinter import *
import mysql.connector as sqlconn

conn = sqlconn.connect(host='192.168.10.7', user='root', passwd='Counter123', database='quest')
#conn.set_charset_collation('latin1', 'latin1_general_ci')
mycursor = conn.cursor()
#mycursor.execute("SELECT * FROM loginTable")
#result = mycursor.fetchall()

#For Every User
#--------------------------------------------------------------------------------------------------------------------------------------------
def displayInfo(ID): #User case to display the personal information of the person who logged in
	sqlcommand = None
	if ID//10000 == 1:
		sqlcommand = "SELECT id, name_, gpa, total_credit_hours, year_, major FROM student WHERE id = " + str(ID) + ";"
	elif ID//10000 ==2:
		sqlcommand = "SELECT id, name_, department_name, salary, post FROM teacher WHERE id = " + str(ID) + ";"
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
#Specifically for database managers:
def addCourse():
	return

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

#For workers
def workerFunction(topWIndow, ID, pw, root):
	ButtonDisplayInfo = Button(topWindow, text = 'Display Personal Information', command=lambda:displayInfo(ID))
	ButtonDisplayInfo.grid(row=0, column=0, padx=5, pady=5)

#For database manager
def managerFunction(topWindow, ID, pw, root):
	ButtonAddCourse = Button(topWindow, text = 'Add Course in the Course List', command = addCourse)
	ButtonAddCourse.grid(row=0, column=0, padx=5, pady=5)

#Helper functions
def deleteThreeWindows(win1, win2, win3):
	win1.destroy()
	win2.destroy()
	win3.destroy()
def destroy_all(root): #To destroy all toplevel windows
    for widget in root.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()

#For login
def getLogin(root, IDField, PasswordField):
	ID = IDField.get()
	ID = int(ID)
	pw = PasswordField.get()

	sqlcommand = "SELECT COUNT(%s) FROM loginTable WHERE id = %s AND pw = %s;"
	vals = (ID, ID, pw)
	mycursor.execute(sqlcommand, vals)

	loginBool = False

	loginResult = mycursor.fetchone()
	(loginResult, ) = loginResult
	if loginResult == 1:
		loginBool = True
		topWindow = Toplevel()

	
	if loginBool == True and ID//10000 == 1:
		print('Student: ID', ID, 'logged in.')
		studentFunction(topWindow, ID, pw, root)
	elif loginBool == True and ID//10000 == 2:
		print('Teacher: ID', ID, 'logged in.')
		teacherFunction(topWindow, ID, pw, root)
	else:
		print('Invalid Login')

def main():
	root = Tk()
	root.title('Login')

	#Creating username input field
	IDLabel = Label(root, text='ID: ')
	IDLabel.grid(row=0, column=0, padx=5, pady=5)
	IDField = Entry(root, width=25)
	IDField.grid(row=0, column=1, padx=5, pady=5)

	#Creating password input field
	PasswordLabel = Label(root, text='Password: ')
	PasswordLabel.grid(row=1, column=0, padx=5, pady=5)
	PasswordField = Entry(root, width=25)
	PasswordField.grid(row=1, column=1, padx=5, pady=5)

	#Creating a button to get the login
	LoginButton = Button(root, text='Login', command=lambda: getLogin(root, IDField, PasswordField))
	LoginButton.grid(row=2, column=1, padx=10, pady=10)

	root.mainloop()

main()

conn.close()