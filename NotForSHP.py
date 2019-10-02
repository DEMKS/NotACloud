from sys import argv
import re
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.uic import loadUi
from functools import partial

import math
class NumCalculator():
    def Calculate(self):
        if (self.o == "+"):
            return(self.a+self.b)
        elif (self.o == "**"):
            return(self.a**self.b)
        elif (self.o == "sqrt"):
            return(math.sqrt(self.a))
        elif (self.o == "sin"):
            if (self.a<0):
                self.a=self.a*-1
            return(math.sin(self.a))
        elif (self.o == "cos"):
            if (self.a<0):
                self.a=self.a*-1
            return(math.sin(self.a))
        elif (self.o == "%"):
            return(self.a % self.b)
        elif (self.o == "-"):
            return(self.a-self.b)
        elif (self.o == "/"):
            if self.b!=0:
                return (self.a/self.b)
            else:
                return("Division by zero imposible")
        elif (self.o == "*"):
            return(self.a*self.b)
    def __init__(self,o,a,b=0):
        self.o = o
        self.a = a
        self.b = b

        self.result=(self.Calculate())



class CalculatorWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = loadUi("calculator.ui", self)
        self.sign = "NaN"
        self.label.setText("")
        self.Btn1.clicked.connect(partial(self.BtnClick, "1"))
        self.Btn2.clicked.connect(partial(self.BtnClick, "2"))
        self.Btn3.clicked.connect(partial(self.BtnClick, "3"))
        self.Btn4.clicked.connect(partial(self.BtnClick, "4"))
        self.Btn5.clicked.connect(partial(self.BtnClick, "5"))
        self.Btn6.clicked.connect(partial(self.BtnClick, "6"))
        self.Btn7.clicked.connect(partial(self.BtnClick, "7"))
        self.Btn8.clicked.connect(partial(self.BtnClick, "8"))
        self.Btn9.clicked.connect(partial(self.BtnClick, "9"))
        self.Btn0.clicked.connect(partial(self.BtnClick, "0"))
        self.multiply.clicked.connect(partial(self.BtnClick, "*"))
        self.minus.clicked.connect(partial(self.BtnClick, "-"))
        self.divide.clicked.connect(partial(self.BtnClick, "/"))
        self.sin.clicked.connect(partial(self.BtnClick, "sin"))
        self.cos.clicked.connect(partial(self.BtnClick, "cos"))
        self.sqrt.clicked.connect(partial(self.BtnClick, "sqrt"))
        self.pow.clicked.connect(partial(self.BtnClick, "pow"))
        self.equal.clicked.connect(partial(self.BtnClick, "="))
        self.plus.clicked.connect(partial(self.BtnClick, "+"))
        self.CA.clicked.connect(self.clear)

    def clear(self):
        self.label.setText('')
        self.sign = ''

    def BtnClick(self, arg):
        if arg == "cos" or arg=="sin" or arg=="sqrt":

            self.label.setText(arg+"("+self.label.text()+")")
        elif arg == "pow":
            self.label.setText(arg+"("+self.label.text()+")")
        elif self.sign=="pow":

            self.label.setText(self.label.text()[:len(self.label.text())-1]+","+arg+")")
        else:
            self.label.setText(self.label.text()+arg)
        if(arg == "="):
            print("Calculating")
            try:
                print(self.sign)
                s = self.label.text()
                s1=s.replace("=","")
                s1=s1.split(self.sign)
                if(self.sign=="sqrt" ):
                    self.label.setText(str(NumCalculator(str(self.sign), float(s1[0])).result))
                elif (self.sign=="pow"):
                    s1=s1.replace("(","").replace(")", "")
                    s1=s1.split(",")
                    self.label.setText(str(NumCalculator("**", float(s1[0]),float(s1[1])).result))
                elif (self.sign=="cos" or self.sign=="sin" ):

                    self.label.setText(str(NumCalculator(str(self.sign), float(s1[1].replace("(","").replace(")", ""))).result))
                else:
                    self.label.setText(str(NumCalculator(str(self.sign), int(s1[0]),int(s1[1])).result))
            except:
                    self.label.setText(str(0))
        if(arg == "*"):
            self.sign = "*"
        elif(arg == "/"):
            self.sign = "/"
        elif(arg == "cos"):
            self.sign = "cos"
        elif(arg == "sin"):
            self.sign = "sin"
        elif(arg == "sqrt"):
            self.sign = "sqrt"
        elif(arg == "pow"):
            self.sign = "pow"
        elif(arg == "+"):
            self.sign = "+"
        elif (arg == "-"):
            self.sign = "-"

    def Show(self):
        self.ui.show()


if __name__ == '__main__':
    app = QApplication(argv)
    calc = CalculatorWindow()
    calc.Show()
    app.exec_()