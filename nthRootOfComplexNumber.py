#Author : VStructures
#Program: Nth Root Of Complex Number

import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon   

class GUILayout(QDialog):           

    def __init__(self, parent=None):   
        super().__init__(parent)        
        
        self.setWindowTitle("Complex number n-th root calculator by VStructures")
        self.setWindowIcon(QIcon('img/nthrootofcomplexnumber.ico'))
        self.setFont(QFont(None, 12))                                       #Default font, size 12
                     
        # Create Horizontal layout and add widgets      This GUI has 2 horiz/al boxes and 1 vertical
        self.inputHorizontal = QHBoxLayout()            #Horizontal box creation
        self.realBox = QLineEdit()                      #textbox for the real number
        self.realBox.setFixedWidth(40)                  #Static size when resizing the window
        self.imaginaryBox = QLineEdit()                
        self.imaginaryBox.setFixedWidth(40)
        self.powerBox = QLineEdit()
        self.powerBox.setFixedWidth(40)
        self.precisionBox = QLineEdit()
        self.precisionBox.setFixedWidth(40)
        self.inputHorizontal.addStretch()               ##This adds the padding on the sides of the box in order to keep the contents in the center when resizing
        self.inputHorizontal.addWidget(QLabel("z ="))   #Adding to the box that stacks content horizontally, in this order
        self.inputHorizontal.addWidget(self.realBox)
        self.inputHorizontal.addWidget(QLabel("+"))
        self.inputHorizontal.addWidget(self.imaginaryBox)
        self.inputHorizontal.addWidget(QLabel("i   Root power:"))
        self.inputHorizontal.addWidget(self.powerBox)
        self.inputHorizontal.addWidget(QLabel(" Decimal precision:"))
        self.inputHorizontal.addWidget(self.precisionBox)
        self.inputHorizontal.addStretch()               ##padding for the other side##

        self.outputHorizontal = QHBoxLayout()           #Another one
        self.ouText = ""                                #Some zero length string for the initialization of outBox
        self.outBox = QPlainTextEdit(self.ouText)       #This is the big box that displays the output
        self.outBox.setReadOnly(True)                   #We can't write to BiG bOx now
        self.outputHorizontal.addWidget(self.outBox)    #add box in another box

        # Create Vertical layout and add widgets    
        self.layout = QVBoxLayout()           #This is the biggest box of them all and it stacks vertically
        self.layout.addSpacing(20)            #Some padding
        self.layout.addLayout(self.inputHorizontal)     #Add this box
        self.layout.addSpacing(20)                      #More padding
        self.layout.addLayout(self.outputHorizontal)    #Then the other box
        self.layout.addSpacing(20)                      #AND THE FINAL PADDING!

        self.button = QPushButton("Calculate")          #Create a button
        self.layout.addWidget(self.button)              #Add this to the biggest box too

        self.setLayout(self.layout)                     #set the design of the GUI, layout
        self.setGeometry(450, 250, 450, 350)            #Initial window size
        
        # Add button signal to printOnButton method
        self.button.clicked.connect(self.printOnButton)     

    def printOnButton(self):
        #Get the string to print from the complexNumNthRootCalc function
        self.ouText = complexNumNthRootCalc(self.powerBox.text(), self.realBox.text(), self.imaginaryBox.text(), self.precisionBox.text())
        #Print it on the BiG oUtPuT bOx and replace the previously outputed string
        self.outBox.setPlainText(self.ouText)

def complexNumNthRootCalc(power, real, imag, prec):   

    try:                                    #Check input
        power = int(power)                  #Make integer, if you can, else raise an error and the try-except block will catch it
        if power < 2:                       #If < 2 raise my special exception for the try-except block to catch
            raise NLessThan2Exception
        real = float(real)                  #Same as make integer
        imag = float(imag)
    except:
        return "Enter valid input.\n Power is an integer greater than or equal to 2,\n Precision is optional,\n No scientific notations"

    try:                                #This also checks input, but it makes it = 2 when an error is raised
        prec = int(prec)                #Make int
        if prec < 1:                    #Too small
            prec = 2
        elif prec > 16:                 #Too big for python's floats
            prec = 16
        elif type(prec) != type(1):     #Integer type? Have to make sure
            prec = 2
    except:
        prec = 2
        
    #Using De Moivre's theorem
    absZ = math.hypot(real, imag)       #This calculates the absolute value of Z
    if absZ == 0:                       #Handle exception
        return "ζ = 0 + 0i"
    
    absZNthRoot = absZ ** (1/power)     #Find nth root of absZ
    argz = math.acos(real/absZ)         #Get phase

    if real < 0 and imag < 0:           #sign handling
        argz *= -1
    
    roots = []  #create an empty list, it will be filled with #k strings
    for k in range(power):               #Use De Moivre's formula for all k's
        realProd = absZNthRoot * math.cos( (argz + 2 * math.pi * k) / power )   #get real
        imagProd = absZNthRoot * math.sin( (argz + 2 * math.pi * k) / power )   #get imaginary

        if real < 0 and imag < 0:       #sign handling because De Moivre's formula doesn't care
            pass
        else:
            if real < 0:            
                realProd *= -1
            if imag < 0:
                imagProd *= -1

        roots.append("ζ{} = {}{}{}i\n\n".format(k+1, round(removeDotZero(realProd), prec), " + " if imagProd >= 0 else " - ", round(removeDotZero(math.fabs(imagProd)), prec)))

    roots = ''.join(roots)
    return roots

def NLessThan2Exception(ValueError):
    pass

def removeDotZero(num):     #removes the .0 from integers eg. 7.0
    if num % 1 == 0:    #spotting the .0
        return int(num)  #removing the .0
    else:
        return num    #don't remove the .0

if __name__ == '__main__':      
    
    app = QApplication(sys.argv)
    
    gui = GUILayout()
    gui.show()
    
    sys.exit(app.exec_())
