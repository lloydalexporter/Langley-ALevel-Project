##########################################################################\
# Income & Outgoings (Budget) Calculator using Tkinter and SQL Database
# By : Lloyd Alex Porter -=- Created : Thu-02-May-2019
##########################################################################/





###|Importing Modules|####################################################\
import time
import sys
import sqlite3 as lite
from decimal import *
try:
        from tkinter import *
        from tkinter import messagebox
except:
        from Tkinter import *
        import tkMessageBox as messagebox
##########################################################################/





###|Global Variables|#####################################################\
totalIncome = 0
totalOutgoings = 0
totalNET = 0
twoDecimalPlaces = Decimal(10) ** -2
arrayTimeScales = ["Weekly","Monthly","Yearly"]
##########################################################################/





###|Connecting to Database|###############################################\
connection = lite.connect("budgets.db")
cursor = connection.cursor()
##########################################################################/





###|Main Window|##########################################################\
window = Tk()
window.title("-=| A Whole Lotta Outgoings |=-")
window.geometry("1175x720")
window.resizable(False,False)
window.configure(background="Plum")
##########################################################################/





###|Title|################################################################\
title = Label(window, text="BUDGET CALCULATOR", font=("Georgia",42,"bold italic"), fg="Dark Orchid", bg="Plum", justify="center")
title.grid(row=0,column=0,sticky=W)
##########################################################################/





###|Menu Bar|#############################################################\
menuBar = Menu(window)

fileMenu = Menu(menuBar, tearoff = 0)
fileMenu.add_command(label="Save")
fileMenu.add_command(label="Export")
fileMenu.add_command(label="Close", command=quit)
fileMenu.add_separator()

fileMenu.add_command(label="Exit", command=quit)
menuBar.add_cascade(label="File", menu=fileMenu)
editMenu = Menu(menuBar, tearoff=0)
editMenu.add_command(label="Undo")

editMenu.add_separator()

editMenu.add_command(label="Cut")
editMenu.add_command(label="Copy")
editMenu.add_command(label="Paste")
editMenu.add_command(label="Delete")
editMenu.add_command(label="Select All")

menuBar.add_cascade(label="Edit", menu=editMenu)
helpMenu = Menu(menuBar, tearoff=0)
helpMenu.add_command(label="Help Index")
helpMenu.add_command(label="About...")
menuBar.add_cascade(label="Help", menu=helpMenu)
##########################################################################/





###|Setting Up Variables|#################################################\
valueOutgoingsTotal = StringVar(window)
valueIncomeTotal = StringVar(window)
valueTotal = StringVar(window)
valueName = StringVar(window)
valueAmount = StringVar(window)
selectInOrOut = StringVar(window)
selectInOrOut.set("Unchosen")
selectTimeScale = StringVar(window)
selectTimeScale.set("Weekly")
progress = StringVar(window)
progressStats = StringVar(window)
##########################################################################/





###|Setting Up Labels|####################################################\
labelName = Label(window, text = "Name   :", font=("Courier New",20,"bold"), fg="Black", bg="Plum")
labelName.place(x = 100 , y = 150)
labelAmount = Label(window, text = "Amount :", font=("Courier New",20,"bold"), fg="Black", bg="Plum")
labelAmount.place(x = 100 , y = 200)
labelPositive = Label(window, text = "+ ", font=("Courier New",32,"bold"), fg="Forest Green", bg="Plum")
labelPositive.place(x = 700 , y = 355)
labelNegative = Label(window, text = "- ", font=("Courier New",32,"bold"), fg="Red", bg="Plum")
labelNegative.place(x = 700 , y = 420)
labelSumLine = Label(window, text = "________________________", font=("Courier New",18,"bold"), fg="Black", bg="Plum")
labelSumLine.place(x = 740 , y = 455)
labelSumLine = Label(window, text = "========================", font=("Courier New",18,"bold"), fg="Black", bg="Plum")
labelSumLine.place(x = 740 , y = 530)
labelEquals = Label(window, text = "= ", font=("Courier New",32,"bold"), fg="Black", bg="Plum")
labelEquals.place(x = 700 , y = 485)
##########################################################################/





###|Setting Up Entries|###################################################\
entryName = Entry(window, textvariable=valueName, font=("Courier New",20), fg="Black", bg="Plum", bd = 0, width = 22)
entryName.place(x = 250 , y = 150)
entryAmount = Entry(window, textvariable=valueAmount, font=("Courier New",20), fg="Black", bg="Plum", bd = 0, width = 22)
entryAmount.place(x = 250 , y = 200)
##########################################################################/





###|Making a Progress Bar|################################################\
progressBar = Label(window, textvariable=progress, font=("Courier New",14,"bold"), fg="Black", bg="Plum")
progressBar.place(x = 12, y = 650)
progressInfomation = Label(window, textvariable=progressStats, font=("Courier New",14,"bold"), fg="Black", bg="Plum")
progressInfomation.place(x = 12, y = 675)
##########################################################################/





###|Calculating the Progress Bar - FUNCTION|##############################\
def calculateProgress(totalIncome,totalOutgoings,totalNET):
        print("coolbeans -=- Update Progress Bar")
        
        totalIncome = int(totalIncome * 100)
        totalOutgoings = int(totalOutgoings * 100)
        total = totalIncome + totalOutgoings
        
        try:
                print("     warmbeans -=- Succeeded in Dividing")
                percent = int(totalIncome / total * 100)
                print("     warmbeans -=- Progress Bar is within Capacity")
                output = ">|" + (percent*"█") + ((100-percent)*"░") + "|<"
                statistics = ">| Income : " + str(percent) + "%" + " "*(75-len(str(percent))-len(str(100-percent))) + "Outgoings : " + str(100-percent) + "% |<"
        except:
                print("     warmbeans -=- Failed in Dividing\n     warmbeans -=- Tables are Empty")
                percent = "Null Values"
                output = ">|" + 29*"░" + "!! Enter Income / Outgoing to Begin !!" + 29*"░" + "|<"
                statistics = ">| Income : --%" + " "*67 + "Outgoings : --%" + " |<"
        
        print("Expenditure   : " + str(totalOutgoings))
        print("Income        : " + str(totalIncome))
        print("Percentage    : " + str(percent))
                
        progress.set(output)
        progressStats.set(statistics)
##########################################################################/





###|Update Other Tables - FUNCTION|#######################################\
def updateOtherTables(getValueName,getValueAmount,getTimeScale,getInOrOut):
        print("coolbeans -=- Updating Other Tables")
        
        if getTimeScale == "Weekly":
                print("    warmbeans -=- Weekly Time Scale into Monthly and Yearly")
                getValueAmountW2M = float(getValueAmount) * 4
                getValueAmountW2M = Decimal(getValueAmountW2M).quantize(twoDecimalPlaces)
                column = "(columnMonthly" + getInOrOut + "Name, columnMonthly" + getInOrOut + "Amount)"
                cursor.execute("CREATE TABLE IF NOT EXISTS tableMonthly" + getInOrOut + " " + column)
                cursor.execute("INSERT INTO tableMonthly" + getInOrOut + " " + column + " VALUES (?,?)",(getValueName,float(getValueAmountW2M)))
                getValueAmountW2Y = float(getValueAmount) * 52
                getValueAmountW2Y = Decimal(getValueAmountW2Y).quantize(twoDecimalPlaces)
                column = "(columnYearly" + getInOrOut + "Name, columnYearly" + getInOrOut + "Amount)"
                cursor.execute("CREATE TABLE IF NOT EXISTS tableYearly" + getInOrOut + " " + column)
                cursor.execute("INSERT INTO tableYearly" + getInOrOut + " " + column + " VALUES (?,?)",(getValueName,float(getValueAmountW2Y)))
                connection.commit()
        elif getTimeScale == "Monthly":
                print("    warmbeans -=- Monthly Time Scale into Weekly and Yearly")
                getValueAmountM2W = float(getValueAmount) / 4
                getValueAmountM2W = Decimal(getValueAmountM2W).quantize(twoDecimalPlaces)
                column = "(columnWeekly" + getInOrOut + "Name, columnWeekly" + getInOrOut + "Amount)"
                cursor.execute("CREATE TABLE IF NOT EXISTS tableWeekly" + getInOrOut + " " + column)
                cursor.execute("INSERT INTO tableWeekly" + getInOrOut + " " + column + " VALUES (?,?)",(getValueName,float(getValueAmountM2W)))
                getValueAmountM2Y = float(getValueAmount) * 12
                getValueAmountM2Y = Decimal(getValueAmountM2Y).quantize(twoDecimalPlaces)
                column = "(columnYearly" + getInOrOut + "Name, columnYearly" + getInOrOut + "Amount)"
                cursor.execute("CREATE TABLE IF NOT EXISTS tableYearly" + getInOrOut + " " + column)
                cursor.execute("INSERT INTO tableYearly" + getInOrOut + " " + column + " VALUES (?,?)",(getValueName,float(getValueAmountM2Y)))
                connection.commit()
        elif getTimeScale == "Yearly":
                print("    warmbeans -=- Yearly Time Scale into Weekly and Monthly")
                getValueAmountY2W = float(getValueAmount) / 52
                getValueAmountY2W = Decimal(getValueAmountY2W).quantize(twoDecimalPlaces)
                column = "(columnWeekly" + getInOrOut + "Name, columnWeekly" + getInOrOut + "Amount)"
                cursor.execute("CREATE TABLE IF NOT EXISTS tableWeekly" + getInOrOut + " " + column)
                cursor.execute("INSERT INTO tableWeekly" + getInOrOut + " " + column + " VALUES (?,?)",(getValueName,float(getValueAmountY2W)))
                getValueAmountY2M = float(getValueAmount) / 12
                getValueAmountY2M = Decimal(getValueAmountY2M).quantize(twoDecimalPlaces)
                column = "(columnMonthly" + getInOrOut + "Name, columnMonthly" + getInOrOut + "Amount)"
                cursor.execute("CREATE TABLE IF NOT EXISTS tableMonthly" + getInOrOut + " " + column)
                cursor.execute("INSERT INTO tableMonthly" + getInOrOut + " " + column + " VALUES (?,?)",(getValueName,float(getValueAmountY2M)))
                connection.commit()
##########################################################################/





###|Income Total - FUNCTION|##############################################\
def incomeTotal():
        global totalIncome
        print("coolbeans -=- Getting Total from Income Column")
        cursor.execute("SELECT SUM(column" + selectTimeScale.get() + "IncomeAmount) FROM table" + selectTimeScale.get() + "Income")
        
        data = cursor.fetchall()
        
        gaps = 0
        
        try:
                print("     warmbeans -=- Is Income Unique?")
                totalIncome = float(str(data[0]).strip("(,)"))
                totalIncome = Decimal(totalIncome).quantize(twoDecimalPlaces)
                print("          hotbeans -=- Yep")
        except:
                print("          hotbeans -=- Nope")
                totalIncome = Decimal(0).quantize(twoDecimalPlaces)
        
        incomeLength = len(str(totalIncome))
        
        gaps = 10 - incomeLength
        
        valueIncomeTotal.set("£ "+ " " * gaps +str(totalIncome))
                
        print("Income        : " + str(totalIncome))
        
        connection.commit()
##########################################################################/





###|Outgoings Total - FUNCTION|###########################################\
def outgoingsTotal():
        global totalOutgoings
        print("coolbeans -=- Getting Total from Outgoings Column")
        cursor.execute("SELECT SUM(column" + selectTimeScale.get() + "OutgoingsAmount) FROM table" + selectTimeScale.get() + "Outgoings")
        
        data = cursor.fetchall()
        
        try:
                print("     warmbeans -=- Is Income Unique?")
                totalOutgoings = float(str(data[0]).strip("(,)"))
                totalOutgoings = Decimal(totalOutgoings).quantize(twoDecimalPlaces)
                print("          hotbeans -=- Yep")
        except:
                print("          hotbeans -=- Nope")
                totalOutgoings = Decimal(0).quantize(twoDecimalPlaces)
        
        outgoingsLength = len(str(totalOutgoings))
                
        gaps = 10 - outgoingsLength
                
        valueOutgoingsTotal.set("£ "+ " " * gaps +str(totalOutgoings))
        
        print("Outgoings  : " + str(totalOutgoings))
        
        connection.commit()     
##########################################################################/





###|Do Calculation - FUNCTION|############################################\
def doCalculation():
        global totalIncome, totalOutgoings, totalNET
        print("coolbeans -=- Doing the NET Calculation")
        
        print("Income        : " + str(totalIncome))
        print("Outgoings  : " + str(totalOutgoings))
        totalNET = float(totalIncome)-float(totalOutgoings)
        totalNET = Decimal(totalNET).quantize(twoDecimalPlaces)
        
        print("Total         : " + str(totalNET))
        
        totalLength = len(str(totalNET))
        
        gaps = 10 - totalLength
        
        valueTotal.set("£ "+ " " * gaps +str(totalNET))
        
        calculateProgress(totalIncome,totalOutgoings,totalNET)
##########################################################################/





###|Open Both Databases - FUNCTION|#######################################\
def openDatabases():
        print("coolbeans -=- Time Scale Changed to " + selectTimeScale.get() + "\ncoolbeans -=- Opening Both Databases")
        openIncomeDatabase()
        openOutgoingsDatabase()
        incomeTotal()
        outgoingsTotal()
        doCalculation()
##########################################################################/





###|Open the Income Database - FUNCTION|##################################\
def openIncomeDatabase():
        global listBoxIncome
        print("coolbeans -=- Opening the Income Database")
        
        column = "(column" + selectTimeScale.get() + "IncomeName, column" + selectTimeScale.get() + "IncomeAmount)"
        cursor.execute("CREATE TABLE IF NOT EXISTS table" + selectTimeScale.get() + "Income " + column)
        cursor.execute("SELECT * FROM table" + selectTimeScale.get() + "Income ORDER BY column" + selectTimeScale.get() + "IncomeAmount ASC")
        
        frame = Frame(window)
        frame.place(x = 10 , y = 310)
        
        listBoxIncome = Listbox(frame, height = 13, width = 32, font=("Courier New",14), fg="Black", bg="Plum", selectmode=SINGLE)
        listBoxIncome.pack(side = LEFT, fill = Y)
        
        scroll = Scrollbar(frame, orient = VERTICAL,bg="Plum")
        scroll.config(command = listBoxIncome.yview)
        scroll.pack(side = RIGHT, fill = Y)
        listBoxIncome.config(yscrollcommand = scroll.set)
        
        listBoxIncome.insert(0, "         -=| " + selectTimeScale.get() + " |=-")
        listBoxIncome.insert(1, "Income Name               Amount")
        listBoxIncome.insert(2, "––––––––––––––––––––––––––––––––")
        
        data = cursor.fetchall()
        
        dataName = [i[0] for i in data]
        dataAmount = [i[1] for i in data]
        
        for row in data:
                amount = Decimal(row[1]).quantize(twoDecimalPlaces)
                print(amount)
                lengthName = len(str(row[0]).strip("(,)"))
                lengthAmount = len(str(amount).strip("(,)"))
                gaps = 31 - lengthName - lengthAmount
                inserted = row[0] + (gaps) * " " + "£" + str(amount)
                print(inserted)
                listBoxIncome.insert(3,inserted)
                
        connection.commit()
##########################################################################/





###|Open the Outgoings Database - FUNCTION|###########################\
def openOutgoingsDatabase():
        global listBoxOutgoings
        print("coolbeans -=- Opening the Outgoings Database")
        
        column = "(column" + selectTimeScale.get() + "OutgoingsName, column" + selectTimeScale.get() + "OutgoingsAmount)"
        cursor.execute("CREATE TABLE IF NOT EXISTS table" + selectTimeScale.get() + "Outgoings " + column)
        cursor.execute("SELECT * FROM table" + selectTimeScale.get() + "Outgoings ORDER BY column" + selectTimeScale.get() + "OutgoingsAmount ASC")
        
        frame = Frame(window)
        frame.place(x = 300 , y = 310)
        
        listBoxOutgoings = Listbox(frame, height = 13, width = 32, font=("Courier New",14), fg="Black", bg="Plum", selectmode=SINGLE)
        listBoxOutgoings.pack(side = LEFT, fill = Y)
        
        scroll = Scrollbar(frame, orient = VERTICAL,bg="Plum")
        scroll.config(command = listBoxOutgoings.yview)
        scroll.pack(side = RIGHT, fill = Y)
        listBoxOutgoings.config(yscrollcommand = scroll.set)
        
        listBoxOutgoings.insert(0, "         -=| " + selectTimeScale.get() + " |=-")
        listBoxOutgoings.insert(1, "Outgoing Name         Amount")
        listBoxOutgoings.insert(2, "––––––––––––––––––––––––––––––––")
        
        data = cursor.fetchall()
        
        dataName = [i[0] for i in data]
        dataAmount = [i[1] for i in data]
                
        for row in data:
                amount = Decimal(row[1]).quantize(twoDecimalPlaces)
                print(amount)
                lengthName = len(str(row[0]).strip("(,)"))
                lengthAmount = len(str(amount).strip("(,)"))
                gaps = 31 - lengthName - lengthAmount
                inserted = row[0] + (gaps) * " " + "£" + str(amount)
                print(inserted)
                listBoxOutgoings.insert(3,inserted)
                
        connection.commit()
##########################################################################/





###|Submit Data - FUNCTION|##############################################\
def submitData():
        print("coolbeans -=- Submitting the Data")
        
        getValueName = valueName.get().title().replace(" ","")
        
        try:
                getValueAmount = float(valueAmount.get())
                getValueAmount = Decimal(getValueAmount).quantize(twoDecimalPlaces)
        except:
                getValueAmount = valueAmount.get()
        
        print(getValueAmount)
        
        getTimeScale = selectTimeScale.get()
        getInOrOut = selectInOrOut.get()
        
        stringValue = getValueName.isalpha()
                
        isStringLength = False
        isFloatLength = False
                
        stringLength = len(getValueName)
        if stringLength < 21:
                isStringLength = True
        floatLength = len(str(getValueAmount))
        if floatLength < 11:
                isFloatLength = True
                
        column = "(column" + getTimeScale + getInOrOut + "Name, column" + getTimeScale + getInOrOut + "Amount)"
                
        if getInOrOut != "Unchosen":
                print("     warmbeans -=- Chosen")
                if stringValue == True and isStringLength == True and isFloatLength == True:
                        getValueAmount = Decimal(getValueAmount).quantize(twoDecimalPlaces)
                        getValueAmount = str(getValueAmount)
                        print(getValueAmount)
                        print("          hotbeans -=- Values Verified")
                
                        cursor.execute("CREATE TABLE IF NOT EXISTS table" + getTimeScale + getInOrOut + " " + column)
                        cursor.execute("INSERT INTO table" + getTimeScale + getInOrOut + " " + column + " VALUES (?,?)",(getValueName,getValueAmount))
                        
                        connection.commit()
                        clearEntries()
                        updateOtherTables(getValueName,getValueAmount,getTimeScale,getInOrOut)
                else:
                        print("          hotbeans -=- Value is Null")
                        messagebox.showerror("-=| Error |=-","Please enter valid inputs:\n\n• Name     : String ≤ 20\n• Amount : Float ≤ 10")
                openDatabases()
        else:
                print("     warmbeans -=- Unchosen")
                messagebox.showerror("-=| Error |=-","Please select either:\n\n• Income\n• Outgoing")
#########################################################################/





###|Clear Entries - FUNCTION|############################################\
def clearEntries():
        print("coolbeans -=- Clearing the Entries")
        
        valueName.set("")
        valueAmount.set("")
#########################################################################/





###|Delete Data - FUNCTION|##############################################\
def deleteData():
        print("coolbeans -=- Deleting the Data")
        
        getValueName = valueName.get().title().replace(" ","")
        
        getTimeScale = selectTimeScale.get()
        getInOrOut = selectInOrOut.get()
        
        if getInOrOut != "Unchosen":
                print("     warmbeans -=- Chosen")
                if getValueName != "":
                        print("          hotbeans -=- Name Entry has a Value")
                        
                        messageYouSure = messagebox.askyesno("-=| Are you sure? |=-","Are you sure you want to delete this record?")

                        if messageYouSure == True:
                                print("               burntbeans -=- True")
                                for timeScale in arrayTimeScales:
                                        cursor.execute("DELETE FROM table" + timeScale + getInOrOut + " WHERE column" + timeScale + getInOrOut + "Name = \"" + getValueName + "\"")
                                messageYouSure = False
                                clearEntries()
                                connection.commit()
                        else:
                                print("               burntbeans -=- False")
                else:
                        print("          hotbeans -=- Name Entry is Empty")
                        messagebox.showerror("-=| Error |=-","Please enter valid input:\n\n• Name     : String")
        else:
                print("     warmbeans -=- Unchosen")
                messagebox.showerror("-=| Error |=-","Please select either:\n\n• Income\n• Outgoings")

        openDatabases()
#########################################################################/





###|Launch Chart|########################################################\
def launchChart():
        print("coolbeans -=- Launching the Chart Module")

        try:
                piChartProgram = __import__("Create Chart.py")
                import piChartProgram
        except Exception as e:
                print("!Profoundly: Take it from here Jimmy!")
                print(e)
#########################################################################/



        

###|Setting Up Radio Buttons|############################################\
radioWeekly = Radiobutton(window, text = "Weekly", font=("Courier New",16,"bold"), fg="Black", bg="Plum", variable = selectTimeScale, value = "Weekly", command = openDatabases)
radioWeekly.place(x = 950, y = 10)
radioMonthly = Radiobutton(window, text = "Monthly", font=("Courier New",16,"bold"), fg="Black", bg="Plum", variable = selectTimeScale, value = "Monthly", command = openDatabases)
radioMonthly.place(x = 950, y = 40)
radioYearly = Radiobutton(window, text = "Yearly", font=("Courier New",16,"bold"), fg="Black", bg="Plum", variable = selectTimeScale, value = "Yearly", command = openDatabases)
radioYearly.place(x = 950, y = 70)
radioIncome = Radiobutton(window, text = "Income", font=("Courier New",22,"bold"), fg="Black", bg="Plum", variable = selectInOrOut, value = "Income", command = openDatabases)
radioIncome.place(x = 125, y = 100)
radioOutgoings = Radiobutton(window, text = "Outgoing", font=("Courier New",22,"bold"), fg="Black", bg="Plum", variable = selectInOrOut, value = "Outgoings", command = openDatabases)
radioOutgoings.place(x = 325, y = 100)
##########################################################################/





###|Setting Up Buttons|###################################################\
buttonSumbit = Button(window, font=("Courier New",18,"bold"), fg="Black", bg="Plum", activeforeground="Red", text="Submit",command=submitData, width = 7, height = 2)
buttonSumbit.place(x = 240 , y = 240)
buttonClear = Button(window, font=("Courier New",18,"bold"), fg="Black", bg="Plum", activeforeground="Red", text="Clear",command=clearEntries, width = 7, height = 2)
buttonClear.place(x = 350 , y = 240)
buttonDelete = Button(window, font=("Courier New",18,"bold"), fg="Black", bg="Plum", activeforeground="Red", text="Delete",command=deleteData, width = 7, height = 2)
buttonDelete.place(x = 460 , y = 240)
buttonChart = Button(window, font=("Courier New",18,"bold"), fg="Black", bg="Plum", activeforeground="Red", text="Create Chart",command=launchChart, width = 15, height = 3)
buttonChart.place(x = 900 , y = 630)
##########################################################################/





###|Setting Up Updatable Calculation Label|###############################\
labelUpdatePositive = Label(window, textvariable = valueIncomeTotal, font=("Courier New",32,"bold"), fg="Black", bg="Plum")
labelUpdatePositive.place(x = 755 , y = 355)
labelUpdateNegative = Label(window, textvariable = valueOutgoingsTotal, font=("Courier New",32,"bold"), fg="Black", bg="Plum")
labelUpdateNegative.place(x = 755 , y = 420)
labelUpdateEquals = Label(window, textvariable = valueTotal, font=("Courier New",32,"bold"), fg="Black", bg="Plum")
labelUpdateEquals.place(x = 755 , y = 485)
##########################################################################/





###|Running the Program and Start Up|#####################################\
openDatabases()
window.config(menu=menuBar)
window.mainloop()
##########################################################################/
