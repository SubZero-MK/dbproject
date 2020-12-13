from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import mysql.connector as sqlconn

#connecting to the database
conn = sqlconn.connect(host='localhost', user='root', passwd='Counter123', database='quest') #Local database
#conn = sqlconn.connect(host='remotemysql.com', user='KenwezuDiC', passwd='N0hZGnthfY', database='KenwezuDiC') #Remote database (slow)

#cursor to the database
mycursor = conn.cursor()

#-- = little things to do

def displayInfo(ID):
	#Setting up the sqlcommand according to the ID
	sqlcommand = None
	if ID//10000 == 1:
		sqlcommand = "SELECT id, name_, gpa, total_credit_hours, year_, major FROM student WHERE id = " + str(ID) + ";"
	elif ID//10000 == 2:
		sqlcommand = "SELECT id, name_, department_name, salary, post FROM teacher WHERE id = " + str(ID) + ";"
	elif ID//10000 == 3:
		sqlcommand = "SELECT id, name_, office_under, salary, post FROM worker WHERE id = " + str(ID) + ";"
	#Executing the sqlcommand
	mycursor.execute(sqlcommand)
	#Opening a new window to display the personal information
	displayWindow = Toplevel()
	displayWindow.geometry('560x396')
	displayWindow.resizable(False, False)

	display = None

	#Fetching the result
	displayInfoResult = mycursor.fetchone()
	#Breaking the tuple and storing the text in 'display'
	if ID//10000 == 1:
		(sID, name_, gpa, total_credit_hours, year_, major) = displayInfoResult
		display = 'ID: ' + str(sID) + '\nName: ' + name_ + '\nGPA: ' + str(gpa) + '\nTotal Credit Hours: ' + str(total_credit_hours) + '\nYear: ' + year_ + '\nMajor: ' + major
	elif ID//10000 == 2:
		(tID, name_, department_name, salary, post) = displayInfoResult
		display = 'ID: ' + str(tID) + '\nName: ' + name_ + '\nDepartment Name: ' + department_name + '\nSalary: ' + str(salary) + '\nPost: ' + post
	elif ID//10000 == 3:
		(wID, name_, office, salary, post) = displayInfoResult
		display = 'ID: ' + str(wID) + '\nName: ' + name_ + '\nOffice: ' + office + '\nSalary: ' + str(salary) + '\nPost: ' + post 

	#Displaying label text on an image using compound
	displayImage = PhotoImage(file='design/displayInfoFunction.png')
	displayLabel = Label(displayWindow, text=display, font=('oswald', 24, 'bold'), foreground='white', image=displayImage, compound='center')
	displayLabel.image=displayImage	
	displayLabel.grid(row=0, column=0, padx=5, pady=5)

	#Exit Button as an image
	exitImg = PhotoImage(file='design/exitButton.png')
	ButtonCloseDisplay = Button(displayWindow, image=exitImg, command=displayWindow.destroy)
	ButtonCloseDisplay.image = exitImg
	ButtonCloseDisplay.place(x=405, y=313)
#--------------------------------------------------------------------------------------------------------------------------------------
#Change password when logged in
def passwordChange(ID, pw, root):
	#Opening a new window for password change portal
	passwordWindow = Toplevel()
	passwordWindow.title('Password Change')
	passwordWindow.geometry('850x430')
	passwordWindow.resizable(False, False)
	#Opening the image
	pwChangeImg = PhotoImage(file='design/pwchangePortal.png')
	pwChangeImgLabel = Label(passwordWindow, image=pwChangeImg)
	pwChangeImgLabel.image=pwChangeImg
	pwChangeImgLabel.place(x=0, y=0)
	#Opening the entry boxes for inputs
	curPasswordEntry = Text(passwordWindow, width=15, height=1, font=('oswald', 20, 'bold'))
	curPasswordEntry.place(x=377, y=153)
	newPasswordEntry = Text(passwordWindow, width=15, height=1, font=('oswald', 20, 'bold'))
	newPasswordEntry.place(x=377, y=240)
	#Button to take the input from the entry boxes
	pwChangeButtonImg = PhotoImage(file='design/pwchange.png')
	pwChangeButton = Button(passwordWindow, image=pwChangeButtonImg, command=lambda:passwordChangeExecute(passwordWindow, curPasswordEntry, newPasswordEntry, ID, pw, root))
	pwChangeButton.image = pwChangeButtonImg
	pwChangeButton.place(x=330, y=300)

def passwordChangeExecute(window, curPWfield, newPWfield, ID, curpw, root):
	curPWinput = curPWfield.get('1.0', 'end')
	curPWinput = curPWinput[:-1]
	#If the enetered current password does not match the user's password:
	if curPWinput != curpw: 
		NotificationShow(1)
	else: #Update the password in the table
		newPWinput = newPWfield.get('1.0', 'end')
		newPWinput = newPWinput[:-1]

		sqlcommand = "UPDATE loginTable SET pw = (%s) WHERE id = (%s)"
		vals = (newPWinput, ID)
		mycursor.execute(sqlcommand, vals)
		conn.commit()
		#Button to end the process and ask for re-login
		notificationDisplay = Toplevel()
		buttonStyle = ttk.Style()
		buttonStyle.configure('W.TButton', font=('oswald', 20, 'bold'), foreground='black', background='black')
		ButtonEndProcess = Button(notificationDisplay, text='Your password has been updated.\nLogin again with your new password.\nClick the button to proceed', style='W.TButton', command=lambda:destroy_all(root))
		ButtonEndProcess.grid(row=0, column=0)
#--------------------------------------------------------------------------------------------------------------------------------------
def enrollForCourses(ID):
	currentCreditHoursTaken = getCurrentCreditHoursTaken(ID)
	print(currentCreditHoursTaken)
	if currentCreditHoursTaken >= 22:
		NotificationShow(20)
	else:
		#Opening window for enrollment
		enrollWindow = Toplevel()
		enrollWindow.title('Enrollment')
		enrollWindow.geometry('1014x618')
		enrollWindow.resizable(False, False)
		#Setting up the canvas with scrolls
		enrollWindowFrame = Frame(enrollWindow)
		enrollWindowFrame.pack()
		enrollWindowCanvas = Canvas(enrollWindowFrame, width=994, height=618, bg='white')
		enrollWindowCanvas.pack(side=LEFT, fill=BOTH, expand=1)
		enrollWindowScrollBar = Scrollbar(enrollWindowFrame, orient=VERTICAL, command=enrollWindowCanvas.yview)
		enrollWindowScrollBar.pack(side=RIGHT, fill=Y)
		enrollWindowCanvas.configure(yscrollcommand=enrollWindowScrollBar.set)
		enrollWindowCanvas.bind('<Configure>', lambda e:enrollWindowCanvas.configure(scrollregion=enrollWindowCanvas.bbox('all')))
		#Styling for button
		buttonStyle = ttk.Style()
		labelStyle = ttk.Style()
		#Getting the image of the 'fancy' button
		buttonImg = PhotoImage(file='design/stripeButton.png')
		#Getting the timer --if enrollmet is active or not
		timer = getGetEnrollmentTimer()
		if timer == 0:
			buttonStyle.configure('BW.TButton', font=('oswald', 20, 'bold'), foreground='black', background='black')
			noEnrollmentForNowButton = Button(enrollWindowCanvas, text='Enrollment is not allowed for now.\nClick the button to proceed.', style='BW.TButton', command=enrollWindow.destroy)
			noEnrollmentForNowButtonWindow = enrollWindowCanvas.create_window(84, 73, anchor='nw', window=noEnrollmentForNowButton)
		else:
			buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='white', background='black')
			labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='white', background='white')
			#Executing the sqlcommand
			major = getStudentMajor(ID)
			sqlcommand = '''SELECT DISTINCT schedule_id, title, course.id, room_number, room_capacity, current_filled, starting_time, finishing_time, day_
							FROM ((course_enroll_map
							INNER JOIN room_timeslot ON course_enroll_map.schedule_id = room_timeslot.id)
							INNER JOIN course ON course_ref = course.id AND course_title_ref = course.title)
							WHERE course.department_in = %s AND course.title NOT IN (SELECT course_title_ref 
	                                                            					FROM student_passed_courses
	                                                            					WHERE student_id = %s);'''
			vals = (major, ID)
			mycursor.execute(sqlcommand, vals)
			enrollmentTable = mycursor.fetchall()

			numOfSlots = len(enrollmentTable)

			#--Will make enrollment tab icon here
			#textDisp = 'Starting\tEnding\tDay\tCourse ID\t      Course\tRoom Number'
			#tableHeadingLabel = Label(enrollWindowCanvas, image=buttonImg, text=textDisp, style='BW.TLabel', compound='center')
			#tableHeadingLabel.image=buttonImg
			#tableHeadingLabel.place(x=35, y=15, relwidth=1, relheight=0.2)

			for i in range(numOfSlots): #Schedule_id = mapID
				(mapID, courseTitle, courseID, roomNumber, roomCapacity, roomCurrentFilled, startingTime, finishingTime, day_) = enrollmentTable[i]
				dispText = startingTime + '\t' + finishingTime + '\t' + day_ + '\t' + str(courseID) + '\t' + courseTitle  #Text on buttons

				enrollmentTuple = (ID, mapID, courseTitle, courseID, roomNumber, roomCapacity, roomCurrentFilled, startingTime, finishingTime, day_)
				curButton = Button(enrollWindowCanvas, text=dispText, image=buttonImg, style='BW.TButton', compound='center', command=lambda enrollmentTuple=enrollmentTuple:addInEnrollmentList(enrollWindow, enrollmentTuple))
				curButton.image = buttonImg
				curButtonWindow = enrollWindowCanvas.create_window(35, 100 + i*50, anchor='nw', window=curButton)


def addInEnrollmentList(window, enrollmentTuple):
	#Exracting the tuple
	(ID, mapID, courseTitle, courseID, roomNumber, roomCapacity, roomCurrentFilled, startingTime, finishingTime, day_) = enrollmentTuple 
	#Checking if the request has already been made by the student
	alreadyRequestedCommand = '''SELECT count(student_id)
								 FROM enrollment
								 INNER JOIN course_enroll_map ON enrollment.req_id = course_enroll_map.schedule_id
								 WHERE student_id = %s AND course_title_ref = %s
								 LIMIT 1;'''
	vals = (ID, courseTitle)
	mycursor.execute(alreadyRequestedCommand, vals)
	aRCCheck = mycursor.fetchone() #aRCCheck = already Requested Command Check
	(aRCCheck, ) = aRCCheck
	print('arc', aRCCheck)
	currentCreditHoursTaken = getCurrentCreditHoursTaken(ID)
	if currentCreditHoursTaken >= 18:
		NotificationShow(20)
		window.destroy()
	else:
		if aRCCheck == 1:
			NotificationShow(2)
		else:
			roomCapacityCommand = '''SELECT room_capacity, current_filled
									 FROM room_timeslot, course_enroll_map
									 WHERE schedule_id = %s AND id = %s
									 LIMIT 1;'''
			vals = (mapID, mapID)
			mycursor.execute(roomCapacityCommand, vals)
			curAndCap = mycursor.fetchall() #currently filled And Capacity = curAndCap
			(cap, curr) = curAndCap[0]
			if curr >= cap:
				NotificationShow(3)
			else:
				timeslotClashCommand = '''SELECT starting_time, finishing_time, day_
										 FROM ((enrollment
										 INNER JOIN course_enroll_map ON enrollment.req_id = course_enroll_map.schedule_id)
										 INNER JOIN room_timeslot ON course_enroll_map.schedule_id = room_timeslot.id)
										 WHERE student_id = %s;'''
				vals = (ID, )
				mycursor.execute(timeslotClashCommand, vals)
				fetchTimeslots = mycursor.fetchall() #Already enrolled timeslots
				numOfTimeSlots = len(fetchTimeslots)

				clashFound = False #If there is a timing clash or not

				startingTimehours = startingTime[:2]
				startingTimemin = startingTime[-2:]
				startingTimehours = int(startingTimehours)
				startingTimemin = int(startingTimemin)

				finishingTimehours = finishingTime[:2]
				finishingTimemin = finishingTime[-2:]
				finishingTimehours = int(finishingTimehours)
				finishingTimemin = int(finishingTimemin)

				enrolledRange = (finishingTimehours*60 + finishingTimemin) - (startingTimehours*60 + startingTimemin)

				for i in range(numOfTimeSlots):
					(st, ft, dy) = fetchTimeslots[i]

					sthours = st[:2]
					stmin = st[-2:]

					sthours = int(sthours)
					stmin = int(stmin)

					fthours = ft[:2]
					ftmin = ft[-2:]

					fthours = int(sthours)
					ftmin = int(ftmin)

					newRange = (fthours*60 + ftmin) - (sthours*60 + stmin)

					if enrolledRange == newRange and day_ == dy:
						clashFound = True
						break

				if clashFound == True:
					NotificationShow(6)
				else:
					enrollCommand = '''	INSERT INTO enrollment(student_id, req_id) VALUES (%s, %s);'''
					vals = (ID, mapID)
					mycursor.execute(enrollCommand, vals)
					conn.commit()

					enrollCommand = ''' UPDATE room_timeslot
										SET current_filled = current_filled + 1
										WHERE id = %s;'''
					vals = (mapID, )
					mycursor.execute(enrollCommand, vals)
					conn.commit()

					NotificationShow(4)

#--------------------------------------------------------------------------------------------------------------------------------------
def showCurrentEnrolledCourses(ID): #Show currently enrolled classes
	#Creating new window
	currentEnrollWindow = Toplevel()
	currentEnrollWindow.title('Enrolled Courses')
	currentEnrollWindow.geometry('1014x618')
	currentEnrollWindow.resizable(False, False)
	#Setting up the canvas with scrolls
	currentEnrollWindowFrame = Frame(currentEnrollWindow)
	currentEnrollWindowFrame.pack()
	currentEnrollWindowCanvas = Canvas(currentEnrollWindowFrame, width=994, height=618, bg='white')
	currentEnrollWindowCanvas.pack(side=LEFT, fill=BOTH, expand=1)
	currentEnrollWindowScrollBar = Scrollbar(currentEnrollWindowFrame, orient=VERTICAL, command=currentEnrollWindowCanvas.yview)
	currentEnrollWindowScrollBar.pack(side=RIGHT, fill=Y)
	currentEnrollWindowCanvas.configure(yscrollcommand=currentEnrollWindowScrollBar.set)
	currentEnrollWindowCanvas.bind('<Configure>', lambda e:currentEnrollWindowCanvas.configure(scrollregion=currentEnrollWindowCanvas.bbox('all')))
	#Styling for button
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='white', background='white')
	#Getting the image of the 'fancy' label
	LabelImg = PhotoImage(file='design/stripeButton.png')
	#Executing the sqlcommand to fetch the courses
	sqlcommand = '''SELECT course_ref, course_title_ref 
					FROM enrollment
					INNER JOIN course_enroll_map ON enrollment.req_id = course_enroll_map.schedule_id
					WHERE student_id = %s;'''
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	allEnrolledCourses = mycursor.fetchall()
	numOfEnrolledCourses = len(allEnrolledCourses)

	for i in range(numOfEnrolledCourses):
		(courseID, courseTitle) = allEnrolledCourses[i]
		dispText = courseTitle + '\t' + str(courseID)
		curLabel = Label(currentEnrollWindowCanvas, text=dispText, style='BW.TLabel', image=LabelImg, compound='center')
		curLabel.image = LabelImg
		curLabelWindow = currentEnrollWindowCanvas.create_window(35, 15+50*i, anchor='nw', window=curLabel)
#--------------------------------------------------------------------------------------------------------------------------------------
def dropCourse(ID):
	#Creating new window
	timer = getGetEnrollmentTimer()
	if timer == 0:
		NotificationShow(5)
	else:
		dropCourseWindow = Toplevel()
		dropCourseWindow.title('Enrolled Courses')
		dropCourseWindow.geometry('1014x618')
		dropCourseWindow.resizable(False, False)
		#Setting up the canvas with scrolls
		dropCourseWindowFrame = Frame(dropCourseWindow, width=994, height=618)
		dropCourseWindowFrame.pack()

		dropCourseWindowCanvas = Canvas(dropCourseWindowFrame, width=994, height=618, bg='white')
		dropCourseWindowCanvas.pack(side=LEFT, fill=BOTH, expand=1)

		dropCourseWindowScrollBar = Scrollbar(dropCourseWindowFrame, orient=VERTICAL, command=dropCourseWindowCanvas.yview)
		dropCourseWindowScrollBar.pack(side=RIGHT, fill=Y)

		dropCourseWindowCanvas.configure(yscrollcommand=dropCourseWindowScrollBar.set)
		dropCourseWindowCanvas.bind('<Configure>', lambda e:dropCourseWindowCanvas.configure(scrollregion=dropCourseWindowCanvas.bbox('all')))

		#Executing the SQL command now
		sqlcommand = '''SELECT id, req_id,course_ref, course_title_ref 
						FROM enrollment
						INNER JOIN course_enroll_map ON enrollment.req_id = course_enroll_map.schedule_id
						WHERE student_id = %s;'''
		vals = (ID, )
		mycursor.execute(sqlcommand, vals)
		fetchCourses = mycursor.fetchall()
		numOfCourses = len(fetchCourses)

		buttonImg = PhotoImage(file='design/stripeButton.png')
		buttonStyle = ttk.Style()
		buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='white', background='black')

		for i in range(numOfCourses):
			(mapID, requestID, courseID, courseTitle) = fetchCourses[i]
			dispText = courseTitle + '\t' + str(courseID)
			fetchCourse = (mapID, requestID, courseID, courseTitle)	
			curButton = Button(dropCourseWindowCanvas, text=dispText, image=buttonImg, style='BW.TButton', compound='center',command=lambda fetchCourse=fetchCourse:showCourseButton(ID, fetchCourse, dropCourseWindow))
			curButton.image = buttonImg
			curButtonWindow = dropCourseWindowCanvas.create_window(35, 100 + i*50, anchor='nw', window=curButton)

def showCourseButton(ID, fetchCourse, window): #To execute the button
	(mapID, requestID, courseID, courseTitle) = fetchCourse
	sqlcommand = '''DELETE FROM enrollment WHERE id = %s;'''
	vals = (mapID, )

	mycursor.execute(sqlcommand, vals)

	sqlcommand = '''UPDATE room_timeslot
					SET current_filled = current_filled - 1
					WHERE id = %s;'''

	vals = (requestID, )
	mycursor.execute(sqlcommand, vals)

	conn.commit()
	dropNotification(window)

def dropNotification(window): #To show the notification
	buttonStyle = ttk.Style()
	buttonStyle.configure('W.TButton', font=('oswald', 20, 'bold'), foreground='black', background='black')
	NotificationWindow = Toplevel()
	NotificationWindow.resizable(False, False)
	ButtonNotification = Button(NotificationWindow, style='W.TButton', text='The course has been dropped.\nSelect the button to proceed.', command=lambda:deleteTwoWindows(NotificationWindow, window))
	ButtonNotification.grid(row=0, column=0, padx=5, pady=5)
#--------------------------------------------------------------------------------------------------------------------------------------
def showSchedule(ID):
	#Creating new window
	scheduleWindow = Toplevel()
	scheduleWindow.title('Enrolled Courses')
	scheduleWindow.geometry('1014x618')
	scheduleWindow.resizable(False, False)
	#Setting up the canvas with scrolls
	scheduleWindowFrame = Frame(scheduleWindow, width=994, height=618)
	scheduleWindowFrame.pack()

	scheduleWindowCanvas = Canvas(scheduleWindowFrame, width=994, height=618, bg='white')
	scheduleWindowCanvas.pack(side=LEFT, fill=BOTH, expand=1)

	scheduleWindowScrollBar = Scrollbar(scheduleWindowFrame, orient=VERTICAL, command=scheduleWindowCanvas.yview)
	scheduleWindowScrollBar.pack(side=RIGHT, fill=Y)

	scheduleWindowCanvas.configure(yscrollcommand=scheduleWindowScrollBar.set)
	scheduleWindowCanvas.bind("<Configure>", lambda e:scheduleWindowCanvas.configure(scrollregion=scheduleWindowCanvas.bbox('all')))

	#Styling for button
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='white', background='white')
	#Getting the image of the 'fancy' label
	LabelImg = PhotoImage(file='design/stripeButton.png')
	#SQL command to fetch schedule
	sqlcommand = '''SELECT course_idsch, course_titlesch, starting_t, finishing_t, day_t 
					FROM student_schedule
					WHERE studentid = %s;'''
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	studentSchedule = mycursor.fetchall()
	numOfSlots = len(studentSchedule)
	for i in range(numOfSlots):
		(courseID, courseTitle, startingTime, finishingTime, day_) = studentSchedule[i]
		dispText = courseTitle + '\t' + str(courseID) + '\t' + startingTime + '\t' + finishingTime + '\t' + day_
		curLabel = Label(scheduleWindowCanvas, text=dispText, style='BW.TLabel', image=LabelImg, compound='center')
		curLabel.image = LabelImg
		curLabelWindow = scheduleWindowCanvas.create_window(35, 100 + i*50, anchor='nw', window=curLabel)
#--------------------------------------------------------------------------------------------------------------------------------------
def majorChangeRequest(ID):
	majorVar = getMajorChangeVar(ID)
	if majorVar != 0:
		NotificationShow(7)
	else:
		#Creating new window
		majorWindow = Toplevel()
		majorWindow.title('Major Change Request')
		majorWindow.geometry('600x450')
		majorWindow.resizable(False, False)
		#Setting up the canvas with scrolls
		majorWindowFrame = Frame(majorWindow, width=580, height=450)
		majorWindowFrame.pack()

		majorWindowCanvas = Canvas(majorWindowFrame, width=580, height=450, bg='white')
		majorWindowCanvas.pack(side=LEFT, fill=BOTH, expand=1)

		majorWindowScrollBar = Scrollbar(majorWindowFrame, orient=VERTICAL, command=majorWindowCanvas.yview)
		majorWindowScrollBar.pack(side=RIGHT, fill=Y)

		majorWindowCanvas.configure(yscrollcommand=majorWindowScrollBar.set)
		majorWindowCanvas.bind("<Configure>", lambda e:majorWindowCanvas.configure(scrollregion=majorWindowCanvas.bbox('all')))

		buttonStyle = ttk.Style()
		buttonStyle.configure('BW.TButton', font=('oswald', 17, 'bold'), foreground='white', background='white')
		labelStyle = ttk.Style()
		labelStyle.configure('BW.TLabel', font=('oswald', 17, 'bold'), foreground='black', background='white')
		
		textLabel = Label(majorWindowCanvas, text='Pick the school whose major you would like to pursue: ', style='BW.TLabel')
		textLabelWindow = majorWindowCanvas.create_window(35, 30, anchor='nw', window=textLabel)

		schoolsList = getSchoolsList()
		numOfSchools = len(schoolsList)


		ButtonImage = PhotoImage(file='design/smallButton.png')
		for i in range(numOfSchools):
			school = schoolsList[i]
			curButton = Button(majorWindowCanvas, text=school, image=ButtonImage, compound='center',style='BW.TButton', command=lambda school=school:showDepartments(ID, school, majorWindow))
			curButton.image = ButtonImage
			curButtonWindow = majorWindowCanvas.create_window(200, 75+i*60, anchor='nw',window=curButton)

def showDepartments(ID, school, window):
	window.destroy()
	#Creating new window
	depWindow = Toplevel()
	depWindow.title('Department Portal')
	depWindow.geometry('600x450')
	depWindow.resizable(False, False)
	#Setting up the canvas with scrolls
	depWindowFrame = Frame(depWindow, width=580, height=450)
	depWindowFrame.pack()

	depWindowCanvas = Canvas(depWindowFrame, width=580, height=450, bg='white')
	depWindowCanvas.pack(side=LEFT, fill=BOTH, expand=1)

	depWindowScrollBar = Scrollbar(depWindowFrame, orient=VERTICAL, command=depWindowCanvas.yview)
	depWindowScrollBar.pack(side=RIGHT, fill=Y)

	depWindowCanvas.configure(yscrollcommand=depWindowScrollBar.set)
	depWindowCanvas.bind("<Configure>", lambda e:depWindowCanvas.configure(scrollregion=depWindowCanvas.bbox('all')))

	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 14, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 14, 'bold'), foreground='black', background='white')

	allDepartments = getDepartments(school)
	numOfDepartments = len(allDepartments)

	textLabel = Label(depWindowCanvas, text='Select the department you want your as new major: ', style='BW.TLabel')
	textLabelWindow = depWindowCanvas.create_window(35, 30, anchor='nw', window=textLabel)

	ButtonImage = PhotoImage(file='design/smallButton.png')
	major = getStudentMajor(ID)
	for i in range(numOfDepartments):
		if allDepartments[i] != major:
			department = allDepartments[i]
			curButton = Button(depWindowCanvas, text=department, image = ButtonImage, style='BW.TButton', compound='center', command=lambda department=department:setDepartment(ID, department, depWindow))
			curButton.image = ButtonImage
			curButtonWindow = depWindowCanvas.create_window(200, 75+i*50, anchor='nw', window=curButton)

def setDepartment(ID, department, window):
	window.destroy()
	sqlcommand = 'UPDATE student SET major = %s, majorchangevar = %s WHERE id = %s;'
	vals = (department, 1, ID)
	mycursor.execute(sqlcommand, vals)
	conn.commit()
	NotificationShow(8)
#--------------------------------------------------------------------------------------------------------------------------------------
def changeGradingComponent(ID):
	#Let's see if this technique works or not
	(gradeWindow, gradeFrame, gradeCanvas) = getScrollableWindow('Grade Component', '600x450', 580, 450)
	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 14, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 14, 'bold'), foreground='black', background='white')
	#Executing command to get all the courses that teacher teaches
	sqlcommand = 'SELECT course_title, c_id FROM course_teacher_map WHERE teacher_id = %s;'
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	coursesTaught = mycursor.fetchall()
	numOfCourses = len(coursesTaught)

	smallButtonImage = PhotoImage(file='design/smallButton3.png')

	for i in range(numOfCourses):
		(cTitle, cID) = coursesTaught[i]
		course = (cTitle, cID)
		curButton = Button(gradeCanvas, text=cTitle + '\t' + str(cID), image=smallButtonImage, style='BW.TButton', compound='center', command=lambda course=course:openInputBoxes(ID, course, gradeWindow))
		curButton.image = smallButtonImage
		curButtonWindow = gradeCanvas.create_window(200, 60+i*50, anchor='nw', window=curButton) 

def openInputBoxes(ID, course, window):
	window.destroy()

	(gradeWindow, gradeFrame, gradeCanvas) = getScrollableWindow('Grade Component', '600x450', 580, 450)
	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 14, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 14, 'bold', 'underline'), foreground='black', background='white')

	ComponentList = ['CP:', 'Assignment:', 'Quiz:', 'MidTerm:', 'Final:']
	EntryBoxList = []

	for i in range(5):
		curLabel = Label(gradeCanvas, text=ComponentList[i], style='BW.TLabel')
		curLabelWindow = gradeCanvas.create_window(50, 30+i*70, anchor='nw', window=curLabel)
		curEntryBox = Text(gradeCanvas, width=10, height=1, font=('oswald', 14, 'bold'))
		curEntryWindow = gradeCanvas.create_window(180, 30+i*70, anchor='nw', window=curEntryBox)
		EntryBoxList.append(curEntryBox)

	submitImg = PhotoImage(file='design/submitButton.png')
	submissionButton = Button(gradeCanvas, image=submitImg, command=lambda:getDataFromBoxes(ID, EntryBoxList, course, gradeWindow))
	submissionButton.image = submitImg
	submitButtonWindow = gradeCanvas.create_window(115, 30+5*70, anchor='nw', window=submissionButton)

def getDataFromBoxes(ID, BoxList, course, window):
	vals = [] #Gathering values from the entry boxes
	CountCheck = 0
	for i in range(len(BoxList)):
		x = BoxList[i].get('1.0','end')
		val = int(x)
		CountCheck += val
		vals.append(val)
	if CountCheck != 100:
		NotificationShow(9)
	else:
		notAllowedinput = None
		for i in vals:
			if i > 100 or i < 0:
				notAllowedinput = True
				break

		if notAllowedinput == True:
			NotificationShow(10)
		else:
			sqlcommand = '''UPDATE course
							SET cp_component = %s, assignment_component = %s, quiz_component = %s, midterm_component = %s, final_component = %s
							WHERE title = %s AND id = %s;'''
			(courseTitle, courseID) = course
			values = (vals[0], vals[1], vals[2], vals[3], vals[4], courseTitle, courseID)
			mycursor.execute(sqlcommand, values)
			conn.commit()

			buttonStyle = ttk.Style()
			buttonStyle.configure('BW.TButton', font=('oswald', 14, 'bold'), foreground='black', background='white')
			newWindow = Toplevel()
			newWindow.title('Notification')
			ButtonSuccess = Button(newWindow, text='The changes in the component have been madde.\nClick the button to proceed', style='BW.TButton', command=lambda:deleteTwoWindows(window, newWindow))
			ButtonSuccess.grid(row=0, column=0)
#--------------------------------------------------------------------------------------------------------------------------------------
def showDepartmentTeachers(ID):
	teacherPost = getTeacherPost(ID)
	if teacherPost != 'HOD':
		NotificationShow(11)
	else: 
		(depWindow, depFrame, depCanvas) = getScrollableWindow('Department Teachers', '1014x618', 994, 618)
		teacherDepartment = getTeacherDepartment(ID)
		sqlcommand = '''SELECT * FROM teacher WHERE department_name = %s;'''
		vals = (teacherDepartment, )
		mycursor.execute(sqlcommand, vals)
		allTeachers = mycursor.fetchall()
		numOfTeachers = len(allTeachers)

		labelStyle = ttk.Style()
		labelStyle.configure('BW.TLabel', font=('oswald', 11, 'bold', 'underline'), foreground='white', background='black')

		stripeImg = PhotoImage(file='design/stripeButton.png')

		for i in range(numOfTeachers):
			(tid, tname, tdept, tsalary, tpost) = allTeachers[i]
			tid = str(tid)
			tsalary = str(tsalary)

			dispText = 'ID: ' + tid + '\tName: ' + tname + '\tDepartment: ' + tdept + '\tSalary: Rs.' + tsalary + '\tPost: ' + tpost
			curLabel = Label(depCanvas, text=dispText, image = stripeImg, compound='center', style='BW.TLabel')
			curLabel.image = stripeImg
			curLabelWindow = depCanvas.create_window(35, 15+50*i, anchor='nw', window=curLabel)

#--------------------------------------------------------------------------------------------------------------------------------------
def assignGrades(ID):
	sqlcommand = '''SELECT course_teacher_map.course_title, course_teacher_map.c_id, student_id, student.name_
					FROM ((course_teacher_map
					INNER JOIN student_course_map ON course_teacher_map.c_id = student_course_map.c_id AND course_teacher_map.course_title = student_course_map.course_title)
					INNER JOIN student ON student.id = student_course_map.student_id)
					WHERE teacher_id = %s
					ORDER BY c_id, course_title;'''
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	taughtStudents = mycursor.fetchall()
	numOfStudents = len(taughtStudents)

	stripeButton = PhotoImage(file='design/stripeButton.png')

	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 12, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 12, 'bold', 'underline'), foreground='black', background='white')

	(gradeWindow, gradeFrame, gradeCanvas) = getScrollableWindow('Grade assignment', '1014x618', 994, 618)
	for i in range(numOfStudents):
		(courseTitle, courseID, studentID, studentName) = taughtStudents[i]
		dispText = courseTitle + ' : ' + str(courseID) + ' : ' + studentName + ' : ' + str(studentID)
		taughtStudent = (courseTitle, courseID, studentID, studentName)

		curButton = Button(gradeCanvas, text=dispText, compound='center', image=stripeButton, style='BW.TButton', command=lambda taughtStudent=taughtStudent:openGradeBox(ID, taughtStudent, gradeWindow))
		curButton.image = stripeButton
		curButtonWindow = gradeCanvas.create_window(35, 15+50*i, anchor='nw', window=curButton)

def openGradeBox(ID, taughtStudent, window):
	(gradeWindow, gradeFrame, gradeCanvas) = getScrollableWindow('Grade assignment', '600x300', 580, 300)
	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 15, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 15, 'bold'), foreground='black', background='white')

	textLabel = Label(gradeCanvas, text='Assign the grade to the selected student: ', style='BW.TLabel')
	textLabelWindow = gradeCanvas.create_window(30, 30, anchor='nw', window=textLabel)

	gradeBox = Text(gradeCanvas, height=1, width=5, font=('oswald', 15, 'bold'))
	gradeBoxWindow = gradeCanvas.create_window(50, 80, anchor='nw', window=gradeBox)

	submitImg = PhotoImage(file='design/submitButton.png')
	enterButton = Button(gradeCanvas, image=submitImg, command=lambda:giveGrade(ID, taughtStudent, gradeBox, gradeWindow, window))
	enterButton.image = submitImg
	enterButtonWindow = gradeCanvas.create_window(50, 130, anchor='nw', window=enterButton)

def giveGrade(ID, taughtStudent, gradeBox, window1, window2):
	inputGrade = gradeBox.get('1.0', 'end')
	inputGrade = inputGrade[:-1]
	if inputGrade != 'A+' and inputGrade != 'A' and inputGrade != 'B' and inputGrade != 'C' and inputGrade != 'D' and inputGrade != 'F':
		NotificationShow(12)
	else:
		(courseTitle, courseID, studentID, studentName) = taughtStudent
		sqlcommand = '''UPDATE student_course_map
						SET grade = %s
						WHERE student_id = %s AND course_title = %s AND c_id = %s;'''
		vals = (inputGrade, studentID, courseTitle, courseID)
		mycursor.execute(sqlcommand, vals)
		conn.commit()
		window1.destroy()

		NotificationShow(13)

#--------------------------------------------------------------------------------------------------------------------------------------
def addCourse():
	(courseWindow, courseFrame, courseCanvas) = getScrollableWindow('Add Course', '700x800', 680, 800)

	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='black', background='white')

	textLabel = Label(courseCanvas, text='Enter details of the new course: ', style='BW.TLabel')
	textLabelWindow = courseCanvas.create_window(15, 30, anchor='nw', window=textLabel)

	courseTitleLabel = Label(courseCanvas, text='Title: ', style='BW.TLabel')
	courseTitleLabelWindow = courseCanvas.create_window(15, 90, anchor='nw', window=courseTitleLabel)
	courseTitleField = Text(courseCanvas, width=20, height=1, font=('oswald', 13, 'bold'))
	courseTitleFieldWindow = courseCanvas.create_window(115, 90, anchor='nw', window=courseTitleField)
	courseIDLabel = Label(courseCanvas, text='ID: ', style='BW.TLabel')
	courseIDLabelWindow = courseCanvas.create_window(15, 150, anchor='nw', window=courseIDLabel)
	courseIDField = Text(courseCanvas, width=20, height=1, font=('oswald', 13, 'bold'))
	courseIDFieldWindow = courseCanvas.create_window(115, 150, anchor='nw', window=courseIDField)
	courseDeptLabel = Label(courseCanvas, text= 'Department: ', style='BW.TLabel')
	courseDeptLabelWindow = courseCanvas.create_window(15, 210, anchor='nw', window=courseDeptLabel)
	courseDeptField = Text(courseCanvas, width=20, height=1, font=('oswald', 13, 'bold'))
	courseDeptFieldWindow = courseCanvas.create_window(115, 210, anchor='nw', window=courseDeptField)
	courseCHLabel = Label(courseCanvas, text= 'Credit Hours: ', style='BW.TLabel') #CH = Credit Hour
	courseCHLabelWindow = courseCanvas.create_window(15, 270, anchor='nw', window=courseCHLabel)
	courseCHField = Text(courseCanvas, width=20, height=1, font=('oswald', 13, 'bold'))
	courseCHFieldWindow = courseCanvas.create_window(115, 270, anchor='nw', window=courseCHField)

	submitImg = PhotoImage(file='design/submitButton.png')
	submitButton = Button(courseCanvas, image = submitImg, command=lambda:getDataFromBoxes2(courseTitleField, courseIDField, courseDeptField, courseCHField, courseWindow))
	submitButton.image = submitImg
	submitButtonWindow = courseCanvas.create_window(60, 350, anchor='nw', window=submitButton)

def getDataFromBoxes2(cT, cI, cD, cC, window):
	cTitle = cT.get('1.0', 'end')
	cTitle = cTitle[:-1]
	cID = cI.get('1.0', 'end')
	cID = int(cID)
	cCH = cC.get('1.0', 'end')
	cCH = int(cCH)

	sqlcommandcTcheck = "SELECT COUNT(title) FROM course WHERE title = %s AND id = %s LIMIT 0,1;"
	vals = (cTitle, cID)
	mycursor.execute(sqlcommandcTcheck, vals)
	courseUniqueCheck = mycursor.fetchone()
	(courseUniqueCheck, ) = courseUniqueCheck

	if courseUniqueCheck == 1:
		NotificationShow(14)
	else:
		cDept = cD.get('1.0', 'end')
		cDept = cDept[:-1]
		sqlcommandcDcheck = "SELECT COUNT(title) FROM department WHERE title = %s LIMIT 0, 1;"
		vals = (cDept, )
		mycursor.execute(sqlcommandcDcheck, vals)
		courseDeptCheck = mycursor.fetchone()
		(courseDeptCheck, ) = courseDeptCheck
		if courseDeptCheck == 0:
			NotificationShow(15)
		else:
			(timeWindow, timeFrame, timeCanvas) = getScrollableWindow('Available slots', '1014x618', 994, 618)
			sqlcommand = '''SELECT id, room_number, starting_time, finishing_time, day_ #Get those slots that are free for the course
							FROM room_timeslot
							WHERE NOT EXISTS (SELECT course_enroll_map.schedule_id FROM course_enroll_map WHERE schedule_id = room_timeslot.id);'''

			mycursor.execute(sqlcommand)
			availableSlots = mycursor.fetchall()
			numOfSlots = len(availableSlots)

			if numOfSlots == 0:
				NotificationShow(16)
				timeWindow.destroy()
				window.destroy()
			else:
				inputTuple = (cTitle, cID, cDept, cCH)
				buttonStyle = ttk.Style()
				buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='white', background='black')
				labelStyle = ttk.Style()
				labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='white', background='black')

				stripeButton = PhotoImage(file='design/stripeButton.png')

				textLabel = Label(timeCanvas, text='Select one of the free slots for the course: ', compound='center', style='BW.TLabel', image=stripeButton)
				textLabel.image = stripeButton
				textLabelWindow = timeCanvas.create_window(35, 15, anchor='nw', window=textLabel)

				for i in range(numOfSlots):
					(timeslotID, roomNumber, startingTime, finishingTime, day_) = availableSlots[i]
					dispText = 'Room: ' + str(roomNumber) + '\tStarting Time: ' + startingTime + '\tFinishing Time: ' + finishingTime + '\tDay: ' + day_
					availableSlot = (timeslotID, roomNumber, startingTime, finishingTime, day_)
					curButton = Button(timeCanvas, text=dispText, style='BW.TButton', compound='center', image=stripeButton, command=lambda availableSlot=availableSlot:allocateTeacher(availableSlot, inputTuple, timeWindow))
					curButton.image = stripeButton
					curButtonWindow = timeCanvas.create_window(35, 15+(i+1)*50, anchor='nw', window=curButton)

def allocateTeacher(availableSlot, inputTuple, window):
	window.destroy()
	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='white', background='black')

	(cTitle, cID, cDept, cCH) = inputTuple
	(timeslotID, roomNumber, startingTime, finishingTime, day_) = availableSlot
	sqlcommand = '''SELECT id FROM teacher WHERE department_name = %s;'''
	vals = (cDept, )
	mycursor.execute(sqlcommand, vals)
	deptTeachers = mycursor.fetchall()
	numOfTeachers = len(deptTeachers)

	availableTeachers = []

	startingTimehours = startingTime[:2]
	startingTimemin = startingTime[-2:]
	startingTimehours = int(startingTimehours)
	startingTimemin = int(startingTimemin)

	finishingTimehours = finishingTime[:2]
	finishingTimemin = finishingTime[-2:]
	finishingTimehours = int(finishingTimehours)
	finishingTimemin = int(finishingTimemin)

	bookedRange = (finishingTimehours*60 + finishingTimemin) - (startingTimehours*60 + startingTimemin)

	for i in range(numOfTeachers):
		sqlcommandClashCheck = '''SELECT starting_time, finishing_time, day_
								FROM ((course_enroll_map
								INNER JOIN course_teacher_map ON course_title = course_title_ref AND course_ref = c_id)
								INNER JOIN room_timeslot ON course_enroll_map.schedule_id = room_timeslot.id)
								WHERE teacher_id = %s;'''
		(teacherID, ) = deptTeachers[i]
		vals = (teacherID, )
		mycursor.execute(sqlcommandClashCheck, vals)

		fetchTimeslots = mycursor.fetchall() #Already booked slots
		numOfTimeSlots = len(fetchTimeslots)

		for i in range(numOfTimeSlots):
			(st, ft, dy) = fetchTimeslots[i]

			sthours = st[:2]
			stmin = st[-2:]

			sthours = int(sthours)
			stmin = int(stmin)

			fthours = ft[:2]
			ftmin = ft[-2:]

			fthours = int(sthours)
			ftmin = int(ftmin)

			newRange = (fthours*60 + ftmin) - (sthours*60 + stmin)

			if bookedRange == newRange and day_ == dy:
				continue
			else:
				availableTeachers.append(teacherID)
				break

	numOfAvailableTeachers = len(availableTeachers)

	(teacherWindow, teacherFrame, teacherCanvas) = getScrollableWindow('Available Teachers', '1014x618', 994, 618)
	stripeButton = PhotoImage(file='design/stripeButton.png')

	textLabel = Label(teacherCanvas, image=stripeButton, text='Select one of the available teacher: ', compound='center', style='BW.TLabel')
	textLabelWindow = teacherCanvas.create_window(35, 15, anchor='nw', window=textLabel)

	for i in range(numOfAvailableTeachers):
		sqlcommand = '''SELECT id, name_, department_name FROM teacher WHERE id = %s LIMIT 1;'''
		val = availableTeachers[i]
		vals = (val, )
		mycursor.execute(sqlcommand, vals)

		fetchTeacherData = mycursor.fetchone()
		(tID, tName, tDept) = fetchTeacherData

		dispText = 'ID: ' + str(tID) + '\tName: ' + tName + '\tDepartment: ' + tDept
		teacherTuple = (tID, tName, tDept)
		curButton = Button(teacherCanvas, image=stripeButton, text=dispText, compound='center', style='BW.TButton', command=lambda teacherTuple=teacherTuple:allocateAllThings(teacherTuple, availableSlot, inputTuple, teacherWindow))
		curButton.image = stripeButton
		curButtonWindow = teacherCanvas.create_window(35, 65+i*50, anchor='nw', window=curButton)

def allocateAllThings(teacherTuple, availableSlot, inputTuple, window):
	(tID, tName, tDept) = teacherTuple
	(timeslotID, roomNumber, startingTime, finishingTime, day_) = availableSlot
	(cTitle, cID, cDept, cCH) = inputTuple
	#Insertion in course table
	dGC = '20' #Default Grade Component
	sqlcommand = "INSERT INTO course VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
	vals = (cTitle, cID, cDept, cCH, dGC, dGC, dGC, dGC, dGC)
	mycursor.execute(sqlcommand, vals)
	conn.commit()
	#Insertion in course_teacher_map table
	sqlcommand = 'INSERT INTO course_teacher_map(teacher_id, course_title, c_id) VALUES (%s, %s, %s);'
	vals = (tID, cTitle, cID)
	mycursor.execute(sqlcommand, vals)
	conn.commit()
	#Insertion in course_enroll_map table
	sqlcommand = 'INSERT INTO course_enroll_map VALUES (%s, %s, %s);'
	vals = (timeslotID, cID, cTitle)
	mycursor.execute(sqlcommand, vals)
	conn.commit()
	window.destroy()

	NotificationShow(17)

def activateSemester():
	#End enrollment period
	sqlcommand = '''UPDATE enrollment_timer SET timer = 0;'''
	mycursor.execute(sqlcommand)
	conn.commit()

	#Updating the mapping of courses with students
	sqlcommand = '''INSERT INTO student_course_map(course_title, student_id, c_id)
					SELECT course_title_ref, student_id, course_ref
					FROM enrollment
					INNER JOIN course_enroll_map ON req_id = schedule_id;'''
	mycursor.execute(sqlcommand)
	conn.commit()

	#Updating the schedules of the students
	sqlcommand = '''INSERT INTO student_schedule(studentid, course_idsch, course_titlesch, starting_t, finishing_t, day_t)
					SELECT student_id, course_ref, course_title_ref, starting_time, finishing_time, day_
					FROM ((enrollment
					INNER JOIN course_enroll_map ON req_id = schedule_id)
					INNER JOIN room_timeslot ON schedule_id = room_timeslot.id);'''
	mycursor.execute(sqlcommand)
	conn.commit()

	#Deleting every tuple from it and making it ready for enrollment for new semester
	sqlcommand = '''DELETE FROM enrollment;'''
	mycursor.execute(sqlcommand)
	conn.commit()

	NotificationShow(18)

def finishSemester():
	#Start enrollment period
	sqlcommand = '''UPDATE enrollment_timer SET timer = 1;'''
	mycursor.execute(sqlcommand)
	conn.commit()
	
	#Updating tables for students when the courses are passed
	sqlcommand = '''INSERT INTO student_passed_courses(student_id, course_ref, course_title_ref, grade)
					SELECT student_course_map.student_id, c_id, course_title, student_course_map.grade
					FROM student_course_map 
					WHERE student_course_map.grade <> 'F' AND student_course_map.grade <> '-';'''
	mycursor.execute(sqlcommand)
	conn.commit()
	#Deleting tuples 
	sqlcommand = '''DELETE FROM student_course_map;'''
	mycursor.execute(sqlcommand)
	conn.commit()
	#Deleting tuples from schedule
	sqlcommand = '''DELETE FROM student_schedule;'''
	mycursor.execute(sqlcommand)
	conn.commit()

	NotificationShow(19)

#--------------------------------------------------------------------------------------------------------------------------------------
def displayAllCourses():
	(courseWindow, courseFrame, courseCanvas) = getScrollableWindow('Courses Display', '1014x618', 994, 618)
	sqlcommand = '''SELECT * FROM course;'''
	mycursor.execute(sqlcommand)
	allCourses = mycursor.fetchall()
	numOfCourses = len(allCourses)

	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='white', background='black')

	stripeButton = PhotoImage(file='design/stripeButton.png')

	for i in range(numOfCourses):
		(cTitle, cID, cDept, cCH, __, __, __, __, __) = allCourses[i]

		dispText = 'Title: ' + cTitle + '\tID: ' + str(cID) + '\tDepartment: ' + cDept + '\tCredit hours: ' + str(cCH)
		curLabel = Label(courseCanvas, text=dispText, style='BW.TLabel', image=stripeButton, compound='center')
		curLabel.image = stripeButton
		curLabelWindow = courseCanvas.create_window(35, 15+i*50, anchor='nw', window=curLabel)
#--------------------------------------------------------------------------------------------------------------------------------------
def displayAllStudents():
	(studentWindow, studentFrame, studentCanvas) = getScrollableWindow('Student Display', '1014x618', 994, 618)
	sqlcommand = '''SELECT * FROM student;'''
	mycursor.execute(sqlcommand)
	allStudents = mycursor.fetchall()
	numOfStudents = len(allStudents)

	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='white', background='black')

	stripeButton = PhotoImage(file='design/stripeButton.png')

	for i in range(numOfStudents):
		(sID, sName, sGPA, __, __, sMajor, __) = allStudents[i]

		dispText = 'ID: ' + str(sID) + '\tName: ' + sName + '\tGPA: ' + str(sGPA) + '\tMajor: ' + sMajor
		curLabel = Label(studentCanvas, text=dispText, style='BW.TLabel', image=stripeButton, compound='center')
		curLabel.image = stripeButton
		curLabelWindow = studentCanvas.create_window(35, 15+i*50, anchor='nw', window=curLabel)

#--------------------------------------------------------------------------------------------------------------------------------------
def displayAllTeachers():
	(studentWindow, studentFrame, studentCanvas) = getScrollableWindow('Student Display', '1014x618', 994, 618)
	sqlcommand = '''SELECT * FROM teacher;'''
	mycursor.execute(sqlcommand)
	allStudents = mycursor.fetchall()
	numOfStudents = len(allStudents)

	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='white', background='black')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='white', background='black')

	stripeButton = PhotoImage(file='design/stripeButton.png')

	for i in range(numOfStudents):
		(sID, sName, sGPA, __, __) = allStudents[i]

		dispText = 'ID: ' + str(sID) + '\tName: ' + sName + '\tGPA: ' + sGPA
		curLabel = Label(studentCanvas, text=dispText, style='BW.TLabel', image=stripeButton, compound='center')
		curLabel.image = stripeButton
		curLabelWindow = studentCanvas.create_window(35, 15+i*50, anchor='nw', window=curLabel)

#--------------------------------------------------------------------------------------------------------------------------------------
def setEnrollmentTimer(): #When students are allowed to enroll for new courses
	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='black', background='white')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='black', background='white')

	activationWindow = Toplevel()
	sqlcommand = 'SELECT timer FROM enrollment_timer;'
	mycursor.execute(sqlcommand)
	currentTimer = mycursor.fetchone()
	(currentTimer, ) = currentTimer

	activationButton = Button(activationWindow, text='Activate Enrollment', style='BW.TButton', command=lambda:ActivateEnroll(currentTimer, activationWindow))
	activationButton.grid(row=0, column=0, padx=5, pady=5)
	deactivationButton = Button(activationWindow, text='Deactivate Enrollment', style='BW.TButton', command=lambda:DeactivateEnroll(currentTimer, activationWindow))
	deactivationButton.grid(row=1, column=0, padx=5, pady=5)

def ActivateEnroll(cT, acW):
	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='black', background='white')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='black', background='white')

	NotificationWindow = Toplevel()
	if cT == 1:
		actButton = Button(NotificationWindow, text='The Enrollment timer is already active.\nClick the button to proceed. ',style='BW.TButton', command=NotificationWindow.destroy)
		actButton.grid(row=0, column=0, padx=5, pady=5)
	if cT == 0:
		sqlcommand = 'UPDATE enrollment_timer SET timer = 1;'
		mycursor.execute(sqlcommand)
		conn.commit()
		actButton = Button(NotificationWindow, text='The Enrollment timer is now active.\nClick the button to proceed. ', style='BW.TButton',command=lambda:deleteTwoWindows(NotificationWindow, acW))
		actButton.grid(row=0, column=0, padx=5, pady=5)

def DeactivateEnroll(cT, acW):
	buttonStyle = ttk.Style()
	buttonStyle.configure('BW.TButton', font=('oswald', 13, 'bold'), foreground='black', background='white')
	labelStyle = ttk.Style()
	labelStyle.configure('BW.TLabel', font=('oswald', 13, 'bold'), foreground='black', background='white')

	NotificationWindow = Toplevel()
	if cT == 0:
		actButton = Button(NotificationWindow, text='The Enrollment timer is already not active.\nClick the button to proceed. ',style='BW.TButton', command=NotificationWindow.destroy)
		actButton.grid(row=0, column=0, padx=5, pady=5)
	if cT == 1:
		sqlcommand = 'UPDATE enrollment_timer SET timer = 0;'
		mycursor.execute(sqlcommand)
		conn.commit()
		actButton = Button(NotificationWindow, text='The Enrollment timer is now deactivated.\nClick the button to proceed. ', style='BW.TButton',command=lambda:deleteTwoWindows(NotificationWindow, acW))
		actButton.grid(row=0, column=0, padx=5, pady=5)
#--------------------------------------------------------------------------------------------------------------------------------------
def studentFunction(ID, pw, root):
	#Creating a topWindow to show the options
	topWindow = Toplevel()
	topWindow.geometry('1014x618')
	topWindow.title('Portal')
	topWindow.resizable(False, False)
	#Setting up the background image for the portal
	portalImg = PhotoImage(file='design/portal.gif')
	portalLabel = Label(topWindow, image=portalImg)
	portalLabel.image = portalImg
	portalLabel.place(x=0, y=0)

	#DisplayInfo button
	DisplayInfoImg = PhotoImage(file='design/displayInfo.png')
	ButtonDisplayInfo = Button(topWindow, image=DisplayInfoImg, command=lambda:displayInfo(ID))
	ButtonDisplayInfo.image = DisplayInfoImg
	ButtonDisplayInfo.place(x=75, y=60)
	#PasswordChange button
	DisplayPWChangeImg = PhotoImage(file='design/passwordChangeButton.png')
	ButtonPasswordChange = Button(topWindow, image=DisplayPWChangeImg, command=lambda:passwordChange(ID, pw, root))
	ButtonPasswordChange.image = DisplayPWChangeImg
	ButtonPasswordChange.place(x=75, y=145)
	#Enrollment Button
	EnrollmentButtonImg = PhotoImage(file='design/enrollmentButton.png')
	ButtonEnrollinCourses = Button(topWindow, image=EnrollmentButtonImg, command=lambda:enrollForCourses(ID))
	ButtonEnrollinCourses.image = EnrollmentButtonImg
	ButtonEnrollinCourses.place(x=75, y=230)
	#Button to show currently enrolled courses
	showEnrolledCoursesButtonImg = PhotoImage(file='design/showEnrolledCoursesButton.png')
	ButtonShowEnrolledCourses = Button(topWindow, image=showEnrolledCoursesButtonImg, command=lambda:showCurrentEnrolledCourses(ID))
	ButtonShowEnrolledCourses.image = showEnrolledCoursesButtonImg
	ButtonShowEnrolledCourses.place(x=75, y=315)
	#Button to drop course/s
	dropCourseButtonImg = PhotoImage(file='design/dropEnrolledCourseButton.png')
	ButtonDropCourse = Button(topWindow, image=dropCourseButtonImg, command=lambda:dropCourse(ID))
	ButtonDropCourse.image = dropCourseButtonImg
	ButtonDropCourse.place(x=75, y=400)
	#Button to show schedule
	scheduleButtonImg = PhotoImage(file='design/scheduleButton.png')
	ButtonShowSchedule = Button(topWindow, image=scheduleButtonImg, command=lambda:showSchedule(ID))
	ButtonShowSchedule.image = scheduleButtonImg
	ButtonShowSchedule.place(x=75, y=485)
	#Button to request major change
	majorChangeButtonImg = PhotoImage(file='design/majorChange.png')
	ButtonMajorChange = Button(topWindow, image=majorChangeButtonImg, command=lambda:majorChangeRequest(ID))
	ButtonMajorChange.image = majorChangeButtonImg
	ButtonMajorChange.place(x=600, y=60)

def teacherFunction(ID, pw, root):
	#Creating a topWindow to show the options
	topWindow = Toplevel()
	topWindow.geometry('1014x618')
	topWindow.title('Portal')
	topWindow.resizable(False, False)
	#Setting up the background image for the portal
	portalImg = PhotoImage(file='design/portal.gif')
	portalLabel = Label(topWindow, image=portalImg)
	portalLabel.image = portalImg
	portalLabel.place(x=0, y=0)

	#DisplayInfo button
	DisplayInfoImg = PhotoImage(file='design/displayInfo.png')
	ButtonDisplayInfo = Button(topWindow, image=DisplayInfoImg, command=lambda:displayInfo(ID))
	ButtonDisplayInfo.image = DisplayInfoImg
	ButtonDisplayInfo.place(x=75, y=60)
	#PasswordChange button
	DisplayPWChangeImg = PhotoImage(file='design/passwordChangeButton.png')
	ButtonPasswordChange = Button(topWindow, image=DisplayPWChangeImg, command=lambda:passwordChange(ID, pw, root))
	ButtonPasswordChange.image = DisplayPWChangeImg
	ButtonPasswordChange.place(x=75, y= 145)

	#Button to change grading component of the course that teacher teaches
	gradeComponentImg = PhotoImage(file='design/gradeComponentButton.png')
	ButtonGradeComponent = Button(topWindow, image=gradeComponentImg, command=lambda:changeGradingComponent(ID))
	ButtonGradeComponent.image = gradeComponentImg
	ButtonGradeComponent.place(x=75, y= 230)
	#Button to see department teachers
	departmentImg = PhotoImage(file='design/departmentButton.png')
	ButtonSeeDepartmentTeachers = Button(topWindow, image=departmentImg, command=lambda:showDepartmentTeachers(ID))
	ButtonSeeDepartmentTeachers.image = departmentImg
	ButtonSeeDepartmentTeachers.place(x=75, y=315)
	#Button to assign grade to students
	assignGradeImg = PhotoImage(file='design/assignGradeButton.png')
	ButtonAssignGrade = Button(topWindow, image=assignGradeImg, command=lambda:assignGrades(ID))
	ButtonAssignGrade.image = assignGradeImg
	ButtonAssignGrade.place(x=75, y=400)

def workerFunction(ID, pw, root):
	#Creating a topWindow to show the options
	topWindow = Toplevel()
	topWindow.geometry('1014x618')
	topWindow.title('Portal')
	topWindow.resizable(False, False)
	#Setting up the background image for the portal
	portalImg = PhotoImage(file='design/portal.gif')
	portalLabel = Label(topWindow, image=portalImg)
	portalLabel.image = portalImg
	portalLabel.place(x=0, y=0)

	#DisplayInfo button
	DisplayInfoImg = PhotoImage(file='design/displayInfo.png')
	ButtonDisplayInfo = Button(topWindow, image=DisplayInfoImg, command=lambda:displayInfo(ID))
	ButtonDisplayInfo.image = DisplayInfoImg
	ButtonDisplayInfo.place(x=75, y=60)
	#PasswordChange button
	DisplayPWChangeImg = PhotoImage(file='design/passwordChangeButton.png')
	ButtonPasswordChange = Button(topWindow, image=DisplayPWChangeImg, command=lambda:passwordChange(ID, pw, root))
	ButtonPasswordChange.image = DisplayPWChangeImg
	ButtonPasswordChange.place(x=75, y= 145)

def managerFunction(ID, pw, root):
	#Creating a topWindow to show the options
	topWindow = Toplevel()
	topWindow.geometry('1014x618')
	topWindow.title('Portal')
	topWindow.resizable(False, False)
	#Setting up the background image for the portal
	portalImg = PhotoImage(file='design/portal.gif')
	portalLabel = Label(topWindow, image=portalImg)
	portalLabel.image = portalImg
	portalLabel.place(x=0, y=0)

	#Button to add a new course
	addCourseImg = PhotoImage(file='design/addCourseButton.png')
	ButtonAddCourse = Button(topWindow, image=addCourseImg, command=addCourse)
	ButtonAddCourse.image = addCourseImg
	ButtonAddCourse.place(x=75, y=60)
	#Button to activate semester --Mainly processes the tables for the semester
	activationImg = PhotoImage(file='design/activationButton.png')
	ButtonActivate = Button(topWindow, image=activationImg, command=activateSemester)
	ButtonActivate.image = activationImg
	ButtonActivate.place(x=75, y=145)
	#Button to finish the semester --Mainly process tables -passed courses, grades etc.
	finishImg = PhotoImage(file='design/finishButton.png')
	ButtonFinishSemester = Button(topWindow, image=finishImg, command=finishSemester)
	ButtonFinishSemester.image = finishImg
	ButtonFinishSemester.place(x=75, y=230)
	#Button to display course list
	displayCourseImg = PhotoImage(file='design/displayCoursesButton.png')
	ButtonDisplayCourses = Button(topWindow, image=displayCourseImg, command=displayAllCourses)
	ButtonDisplayCourses.image = displayCourseImg
	ButtonDisplayCourses.place(x=75, y=315)
	#Button to display all students
	displayStudentImg = PhotoImage(file='design/displayStudentsButton.png')
	ButtonDisplayStudents = Button(topWindow, image=displayStudentImg, command=displayAllStudents)
	ButtonDisplayStudents.image = displayStudentImg
	ButtonDisplayStudents.place(x=75, y=400)
	#Button to display all teachers
	displayTeacherImg = PhotoImage(file='design/displayTeachersButton.png')
	ButtonDisplayTeachers = Button(topWindow, image=displayTeacherImg, command=displayAllTeachers)
	ButtonDisplayTeachers.image = displayTeacherImg
	ButtonDisplayTeachers.place(x=75, y=485)
	#Button to activate or deactivate enrollment
	displayEnrollmentImg = PhotoImage(file='design/setEnrollmentButton.png')
	ButtonSetEnrollment = Button(topWindow, image=displayEnrollmentImg, command=setEnrollmentTimer)
	ButtonSetEnrollment.image = displayEnrollmentImg
	ButtonSetEnrollment.place(x=600, y=60)

#--------------------------------------------------------------------------------------------------------------------------------------

#To check that the input login is in the database table or not
def getLogin(IDField, pwField, root):
	#Get ID input
	IDinput = IDField.get('1.0', 'end')
	IDinput = int(IDinput)
	#Get Password input
	PWinput = pwField.get('1.0', 'end')
	PWinput = PWinput[:-1]

	print(len(PWinput))
	print(IDinput, PWinput)

	#SQL command to check if the login exists or not.
	sqlcommand = 'SELECT COUNT(id) FROM loginTable WHERE id = %s AND pw = %s LIMIT 1;'
	vals = (IDinput, PWinput)
	mycursor.execute(sqlcommand, vals)
	#Fetching result
	loginResult = mycursor.fetchone()
	(loginResult, ) = loginResult

	#Logging in according to the given inputs
	if loginResult != 1: #The result is not found
		NotificationShow(0)
	else:
		#The main portal that shows all the functionalities
		ID = IDinput
		pw = PWinput
		#Going to the portal according to the ID
		if ID//10000 == 1:
			print('Student: ID', ID, 'logged in.')
			studentFunction(ID, pw, root)
		elif ID//10000 == 2:
			print('Teacher: ID', ID, 'logged in.')
			teacherFunction(ID, pw, root)
		elif ID//10000 == 3:
			print('Worker: ID', ID, 'logged in.')
			workerFunction(ID, pw, root)
		elif ID == 40404:
			print('Manager: ID', ID, 'logged in.')
			managerFunction(ID, pw, root)
		else:
			print('Invalid Login')

#--------------------------------------------------------------------------------------------------------------------------------------
#Helper functions: 
def NotificationShow(switch): #To show different kind of notifications
	#Style for the button
	buttonStyle = ttk.Style()
	buttonStyle.configure('W.TButton', font=('oswald', 20, 'bold'), foreground='black', background='black')
	#Creating the window to show the notification
	NotificationWindow = Toplevel()
	NotificationWindow.resizable(False, False)
	#dispText = display text
	dispText = None
	if switch==0:
		dispText = 'Invalid Login.\nClick the button to proceed.'
	elif switch==1:
		dispText = 'Your entered password does not match your current password.\nClick the button to proceed.'
	elif switch==2:
		dispText = 'You have already selected the course.\nClick the button to proceed.'
	elif switch==3:
		dispText = 'The course capacity is filled.\nClick the button to proceed.'
	elif switch==4:
		dispText = 'Your request has been added in the enrollment chart.\nClick the button to proceed.'
	elif switch==5:
		dispText = 'The enrollment time is not active now.\nClick the button to proceed.'
	elif switch==6:
		dispText = 'Time clash found with already enrolled course.\nClick the button to proceed.'
	elif switch==7:
		dispText = 'You have already changed your major once.\nClick the button to proceed.'
	elif switch==8:
		dispText = 'Your request has been processed and major has been changed.\nClick the button to proceed.'
	elif switch==9:
		dispText = 'The sum of all the grade components has to be 100.\nClick the button to proceed.'
	elif switch==10:
		dispText = 'No grade component can be negative or more than 100.\nClick the button to proceed.'
	elif switch==11:
		dispText = 'Only head of departments have access to the command.\nClick the button to proceed.'
	elif switch==12:
		dispText = 'Allowed grades to enter: A+, A, B, C, D, F\nClick the button to proceed'
	elif switch==13:
		dispText = 'Grade has been assigned.\nClick the button to proceed'
	elif switch==14:
		dispText = 'The course with this title and name are already present.\nClick the button to proceed.'
	elif switch==15:
		dispText = 'There is no department with such title.\nClick the button to proceed.'
	elif switch==16:
		dispText = 'There are no timeslots left to add more courses.\nClick the button to proceed.'
	elif switch==17:
		dispText = 'The course has been added in the course list.\nClick the button to proceed'
	elif switch==18:
		dispText = 'The semester is activated.\nClick the button to proceed'
	elif switch==19:
		dispText = 'The semester is finished and processes have been carried out.\nClick the button to proceed'
	elif switch==20:
		dispText = 'You have exceeded the credit hour limit.\nClick the button to proceed.'

	#Button to show the notification
	NotificationButton = Button(NotificationWindow, text=dispText, style='W.TButton', command=NotificationWindow.destroy)
	NotificationButton.grid(row=0, column=0)
def destroy_all(root): #To destroy all toplevel windows
    for widget in root.winfo_children():
        if isinstance(widget, Toplevel):
            widget.destroy()
def deleteTwoWindows(w1, w2):
	w1.destroy();
	w2.destroy();
def getGetEnrollmentTimer(): #To check if enrollment is allowed or not
	sqlcommand = "SELECT timer FROM enrollment_timer;"
	mycursor.execute(sqlcommand)
	timer = mycursor.fetchone()
	(timer, ) = timer
	return timer
def getStudentMajor(ID): #Get the major of the student
	sqlcommand = 'SELECT major FROM student WHERE id = %s LIMIT 1;'
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	major = mycursor.fetchone()
	(major, ) = major
	return major
def getMajorChangeVar(ID): #Get whether the student has changed the major already or not
	sqlcommand = 'SELECT majorchangevar FROM student WHERE id = %s LIMIT 1;'
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	var = mycursor.fetchone()
	(var, ) = var
	return var
def getTeacherDepartment(ID):
	sqlcommand = 'SELECT department_name FROM teacher WHERE id = %s LIMIT 1;'
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	department = mycursor.fetchone()
	(department, ) = department
	return department
def getTeacherPost(ID):
	sqlcommand = 'SELECT post FROM teacher WHERE id = %s LIMIT 1;'
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	post = mycursor.fetchone()
	(post, ) = post
	return post 
def getSchoolsList():
	sqlcommand = 'SELECT name_ FROM school;'
	mycursor.execute(sqlcommand)
	allSchools = mycursor.fetchall()
	listLen = len(allSchools)
	for i in range(listLen):
		(allSchools[i], ) = allSchools[i]

	return allSchools
def getDepartments(school):
	sqlcommand = '''SELECT title
					FROM department
					INNER JOIN school ON of_school = name_
					WHERE name_ = %s;'''
	vals = (school, )
	mycursor.execute(sqlcommand, vals)
	allDepartments = mycursor.fetchall()
	listDep = len(allDepartments)
	for i in range(listDep):
		(allDepartments[i], ) = allDepartments[i]

	return allDepartments

def getCurrentCreditHoursTaken(ID):
	sqlcommand = '''SELECT SUM(course.credit_hours)
					FROM ((enrollment
					INNER JOIN course_enroll_map ON schedule_id = req_id)
					INNER JOIN course ON course_ref = course.id AND course_title_ref = course.title)
					WHERE student_id = %s ;'''
	vals = (ID, )
	mycursor.execute(sqlcommand, vals)
	currentCH = mycursor.fetchone()
	(currentCH, ) = currentCH
	if currentCH == None:
		currentCH = 0
	return currentCH

def getScrollableWindow(title, geometry, width, height):
	depWindow = Toplevel()
	depWindow.title(title)
	depWindow.geometry(geometry)
	depWindow.resizable(False, False)
	#Setting up the canvas with scrolls
	depWindowFrame = Frame(depWindow, width=width, height=height)
	depWindowFrame.pack()

	depWindowCanvas = Canvas(depWindowFrame, width=width, height=height, bg='white')
	depWindowCanvas.pack(side=LEFT, fill=BOTH, expand=1)

	depWindowScrollBar = Scrollbar(depWindowFrame, orient=VERTICAL, command=depWindowCanvas.yview)
	depWindowScrollBar.pack(side=RIGHT, fill=Y)

	depWindowCanvas.configure(yscrollcommand=depWindowScrollBar.set)
	depWindowCanvas.bind("<Configure>", lambda e:depWindowCanvas.configure(scrollregion=depWindowCanvas.bbox('all')))

	return depWindow, depWindowFrame, depWindowCanvas

#--------------------------------------------------------------------------------------------------------------------------------------
#main function --to start the program
def main():
	root = Tk()
	root.geometry('545x400')
	root.title('Login Portal')
	root.resizable(False, False)

	loginImg = PhotoImage(file='design/login.gif')

	#Background Image
	loginLabelBackground = Label(root, image=loginImg)
	loginLabelBackground.image = loginImg
	loginLabelBackground.place(x=0, y=0, relwidth=1, relheight=1)

	#Entry box for ID
	IDEntry = Text(root, width=15, height=1, font=('oswald', 20, 'bold'))
	IDEntry.place(x=235, y=137)

	#Entry box for password
	PasswordEntry = Text(root, width=15, height=1, font=('oswald', 20, 'bold'))
	PasswordEntry.place(x=235, y=211)

	#Taking the input from the text boxes
	loginButtonImg = PhotoImage(file='design/loginButton.gif')
	loginButton = Button(image = loginButtonImg, command=lambda:getLogin(IDEntry, PasswordEntry, root))
	loginButton.place(x=180, y=286)

	root.mainloop()

main()

conn.close()