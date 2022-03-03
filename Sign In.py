##########################################################################\
# Sign In System -> Launch Python Program Script
# By : Lloyd Alex Porter -=- Created : Mon-17-Feb-2020
##########################################################################/





###|Importing Modules|####################################################\
import time
import sys
import base64
try:
	from tkinter import *
	from tkinter import messagebox
except:
	from Tkinter import *
	import tkMessageBox as messagebox
##########################################################################/





###|Setting Sign In Details|##############################################\
valueUsername = "admin"
valuePassword = "password"
valuePasswordEncoded = base64.b64encode(valuePassword.encode("utf-32"))
##########################################################################/





###|Main Window|##########################################################\
window = Tk()
window.title("-=| Sign In |=-")
window.geometry("350x465")
window.resizable(False,False)
window.configure(background="Plum")
##########################################################################/





###|Title|################################################################\
title = Label(window, text="Sign In", font=("Georgia",82,"bold italic"), fg="Dark Orchid", bg="Plum", justify="center")
title.grid(row=0,column=0,sticky=W)
##########################################################################/





###|Setting Up Variables|#################################################\
valueUsernameEntry = StringVar(window)
valuePasswordEntry = StringVar(window)
##########################################################################/





###|Setting Up Variables|#################################################\
labelUsername = Label(window, text = "Username :", font=("Courier New",20,"bold underline"), fg="Black", bg="Plum")
labelUsername.place(x = 5 , y = 150)
labelPassword = Label(window, text = "Password :", font=("Courier New",20,"bold underline"), fg="Black", bg="Plum")
labelPassword.place(x = 5 , y = 250)
##########################################################################/





###|Setting Up Entries|###################################################\
entryUsername = Entry(window, textvariable=valueUsernameEntry, font=("Courier New",20), fg="Black", bg="Plum", bd = 0, width = 22)
entryUsername.place(x = 26 , y = 190)
entryPassword = Entry(window, textvariable=valuePasswordEntry, font=("Courier New",20), fg="Black", bg="Plum", bd = 0, width = 22, show = "*")
entryPassword.place(x = 26 , y = 290)
##########################################################################/





###|Clear Entries - FUNCTION|############################################\
def clearEntries():
	print("coolbeans -=- Clearing the Entries")
	
	valueUsernameEntry.set("")
	valuePasswordEntry.set("")
#########################################################################/





###|Submit Data - FUNCTION|##############################################\
def submitEntries():
	print("coolbeans -=- Submitting the Entries")


	getUsernameEntry = valueUsernameEntry.get()
	getPasswordEntry = valuePasswordEntry.get()
	getPasswordEntryEncoded = base64.b64encode(getPasswordEntry.encode("utf-32"))


	if (getUsernameEntry == valueUsername) and (getPasswordEntryEncoded == valuePasswordEncoded):
			print("     warmbeans -=- Username and Password are correct")

			print("          hotbeans -=- Quitting Sign In Program")
			window.destroy()
			print("          hotbeans -=- External Program Launched")

			try:
				actualProgram = __import__("Budget Calculator.py")
				import actualProgram
			except Exception as e:
				print("!Profoundly: Take it from here Jimmy!")
				print(e)

	elif (getUsernameEntry or getPasswordEntry) == "":
		print("     warmbeans -=- Username or Password is empty")
		messagebox.showerror("-=| Error |=-","          Please enter value\nfor Username and Password")

	else:
		print("     warmbeans -=- Username or Password is incorrect")
		valuePasswordEntry.set("")
		messagebox.showerror("-=| Error |=-","Username or Password\n            is incorrect")
##########################################################################/





###|Setting Up Buttons|###################################################\
buttonSumbit = Button(window, font=("Courier New",18,"bold"), fg="Black", bg="Plum", activeforeground="Red", text="Sign In",command=submitEntries, width = 17, height = 3)
buttonSumbit.place(x = 30 , y = 370)
buttonClear = Button(window, font=("Courier New",18,"bold"), fg="Black", bg="Plum", activeforeground="Red", text="Clear",command=clearEntries, width = 7, height = 3)
buttonClear.place(x = 230 , y = 370)
##########################################################################/





###|Running the Program and Start Up|#####################################\
window.mainloop()
##########################################################################/
