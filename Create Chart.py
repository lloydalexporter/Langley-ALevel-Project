##########################################################################\
# Pi Chart Creator and Launcher -=- For Use within Budget Calculator
# By : Lloyd Alex Porter -=- Created : Mon-17-Feb-2020
##########################################################################/





###|Importing Modules|####################################################\
import time
import sys
import sqlite3 as lite
import numpy as np
import matplotlib.pyplot as pychart
from decimal import *
try:
	from tkinter import *
	from tkinter import messagebox
except:
	from Tkinter import *
	import tkMessageBox as messagebox
##########################################################################/





###|Connecting to Database|###############################################\
connection = lite.connect("budgets.db")
cursor = connection.cursor()
##########################################################################/





###|Setting Up Variables|#################################################\
valueIncomesTotal = 0
valueOutgoingsTotal = 0
valueTotal = 0
twoDecimalPlaces = Decimal(10) ** -2
##########################################################################/





###|Getting Total Income|#################################################\
print("coolbeans -=- Getting Total from Income Column")

column = "(columnWeeklyIncomeName, columnWeeklyIncomeAmount)"
cursor.execute("CREATE TABLE IF NOT EXISTS tableWeeklyIncome" + column)
cursor.execute("SELECT SUM(columnWeeklyIncomeAmount) FROM tableWeeklyIncome")
	
data = cursor.fetchall()
	
gaps = 0
	
try:
	print("     warmbeans -=- Is Income Unique?")
	valueIncomesTotal = float(str(data[0]).strip("(,)"))
	valueIncomesTotal = Decimal(valueIncomesTotal).quantize(twoDecimalPlaces)
	print("          hotbeans -=- Yep")
except:
	print("          hotbeans -=- Nope")
	valueIncomesTotal = Decimal(0).quantize(twoDecimalPlaces)
	messagebox.showerror("-=| Error |=-","To Create A Chart,\nPlease Enter An Income Values.")
	close()

connection.commit()
##########################################################################/





###|Getting Total Outgoings|##############################################\
print("coolbeans -=- Getting Total from Outgoings Column")

column = "(columnWeeklyOutgoingsName, columnWeeklyOutgoingsAmount)"
cursor.execute("CREATE TABLE IF NOT EXISTS tableWeeklyOutgoings" + column)
cursor.execute("SELECT SUM(columnWeeklyOutgoingsAmount) FROM tableWeeklyOutgoings")
	
data = cursor.fetchall()
	
gaps = 0
	
try:
	print("     warmbeans -=- Is Outgoings Unique?")
	valueOutgoingsTotal = float(str(data[0]).strip("(,)"))
	valueOutgoingsTotal = Decimal(valueOutgoingsTotal).quantize(twoDecimalPlaces)
	print("          hotbeans -=- Yep")
except:
	print("          hotbeans -=- Nope")
	valueOutgoingsTotal = Decimal(0).quantize(twoDecimalPlaces)
	messagebox.showerror("-=| Error |=-","To Create A Chart,\nPlease Enter An Outgoing Value.")
	close()
	
connection.commit()
##########################################################################/





###|Ring Colours|#########################################################\
piIncomes = pychart.cm.Greens
piOutgoings = pychart.cm.Reds
##########################################################################/





###|Creating Chart and Axis|##############################################\
piChart, piAxis = pychart.subplots()
piAxis.axis("equal")
piAxis.set_title("Your Budget:")
piChart.canvas.set_window_title("Budget Pie Chart")
##########################################################################/





###|Calculaing Inside Ring : Incomes|#####################################\
column = "(columnWeeklyIncomeName, columnWeeklyIncomeAmount)"
cursor.execute("CREATE TABLE IF NOT EXISTS tableWeeklyIncome " + column)
cursor.execute("SELECT * FROM tableWeeklyIncome ORDER BY columnWeeklyIncomeAmount ASC")


incomeDataName = []
incomeDataAmount = []

data = cursor.fetchall()
	
dataName = [i[0] for i in data]
dataAmount = [i[1] for i in data]
	
for row in data:
	tempName = str(row[0]).strip("(,)")
	tempAmount = str(row[1]).strip("(,)")
	tempAmount = int(float(tempAmount)*100)
	
	incomeDataName.append(tempName)
	incomeDataAmount.append(tempAmount)

connection.commit()
##########################################################################/





###|Calculaing Inside Ring : Outgoings|###################################\
column = "(columnWeeklyOutgoingsName, columnWeeklyOutgoingsAmount)"
cursor.execute("CREATE TABLE IF NOT EXISTS tableWeeklyOutgoings " + column)
cursor.execute("SELECT * FROM tableWeeklyOutgoings ORDER BY columnWeeklyOutgoingsAmount ASC")


outgoingsDataName = []
outgoingsDataAmount = []

data = cursor.fetchall()
	
dataName = [i[0] for i in data]
dataAmount = [i[1] for i in data]
	
for row in data:
	tempName = str(row[0]).strip("(,)")
	tempAmount = str(row[1]).strip("(,)")
	tempAmount = int(float(tempAmount)*100)
	
	outgoingsDataName.append(tempName)
	outgoingsDataAmount.append(tempAmount)

connection.commit()
##########################################################################/





###|Inside Ring Configurations|###########################################\
insideNames = incomeDataName + outgoingsDataName

insideSizes = []
amountDataConcatenate = incomeDataAmount + outgoingsDataAmount
amountDataSum = sum(amountDataConcatenate)

for x in range(0,len(amountDataConcatenate)):
	tempAmount = amountDataConcatenate[x]
	insideSizes.append(tempAmount)
##########################################################################/





###|Inside Ring Colour Setup|#############################################\
insideIncomesCount = len(incomeDataAmount)
insideOutgoingsCount = len(outgoingsDataAmount)

print(insideIncomesCount)
print(insideOutgoingsCount)

print("coolbeans -=- Preparing Income Colour Scheme")

colourNumbers = [0.3,0.4,0.5,0.6,0.7,0.8,0.7,0.6,0.5,0.4,0.3,0.4,0.5,0.6,0.7,0.8,0.7,0.6,0.5,0.4,0.3,0.4,0.5,0.6,0.7,0.8,0.7,0.6,0.5,0.4,0.3]

tempIncomes = []

colourChart = []

georgiex = 0
for y in range(0,insideIncomesCount):
        colourChart.append(piIncomes(colourNumbers[georgiex]))
        georgiex += 1

georgiex = 0
for y in range(0,insideOutgoingsCount):
        colourChart.append(piOutgoings(colourNumbers[georgiex]))
        georgiex += 1


print(colourChart)

"""
for x in range(0, insideIncomesCount):
	print("     warmbeans -=- Appending Incomes Colour Scheme", x)
	tempIncomesColour = "piIncomes(" + str(colourNumbers[x]) + ")"
	print(tempIncomesColour)
	tempIncomes.append(tempIncomesColour)

tempOutgoings = []
for x in range(0, insideOugoingsCount):
	print("     warmbeans -=- Appending Outgoings Colour Scheme", x)
	tempOutgoingsColour = "piOutgoings(" + str(colourNumbers[x]) + ")"
	print(tempOutgoingsColour)
	tempOutgoings.append(tempOutgoingsColour)

colourChart = []
tempColour = tempIncomes + tempOutgoings

tempColour = "[%s]" % (', '.join(tempColour))
print("[" +tempColour+ "]")
colourChart.append(tempColour)
print(colourChart)

"""
#colourChart = [piIncomes(0.3), piIncomes(0.4), piIncomes(0.3), piOutgoings(0.4)]
print()
print(colourChart)
##########################################################################/





###|Outside Ring Configurations|##########################################\
outsideNames=['Incomes', 'Outgoings']

outsideIncomesSize = sum(incomeDataAmount)
outsideOutgoingsSize = sum(outgoingsDataAmount)

outsideSizes=[outsideIncomesSize,outsideOutgoingsSize]
##########################################################################/





###|Attach Outside Ring|##################################################\
piOutsideRing, _ = piAxis.pie(outsideSizes, radius=1.2, labels=outsideNames, colors=[piIncomes(0.6), piOutgoings(0.6)])
pychart.setp(piOutsideRing, width=0.2, edgecolor="black")
##########################################################################/





###|Attach Inside Ring|###################################################\
piInsideRing, _ = piAxis.pie(insideSizes, radius=1.2-0.2, labels=insideNames, labeldistance=0.6, colors=colourChart)
pychart.setp(piInsideRing, width=0.6, edgecolor="black")
pychart.margins(0,0)
##########################################################################/





###|Show Chart|###########################################################\
pychart.show()
##########################################################################/



###|Shutdown Program|#####################################################\
quit()###### Without: could only be called once, then break button.#######|
##########################################################################/
