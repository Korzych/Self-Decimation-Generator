from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from tkinter import filedialog   
import  sys,tkinter,re,random
root = tkinter.Tk()
root.withdraw()
filePath = ""

class RGenerator:
    def __init__(self,lfsr:list):
        self.lfsr = lfsr
        self.d=5
        self.k=11
        self.regTable= {
        #T=2/3*T0 >1 000 000 2^21 > 1 000 000
        21 : [18,20],
        22 : [20,21],
        23 : [17,22],
        24 : [19,20,22,23],
        25 : [21,24]
       
       }
       
        #Wybór rozmiaru lfsr w przedziale 21-25
        #

    def execLFSR(self):
        index= self.regTable.get(len(self.lfsr))
        val=self.lfsr[index[0]]
        for i in range(1,len(index)):
            val=val ^ self.lfsr[index[i]]
        value=self.lfsr.pop()
        self.lfsr.insert(0,val)
        return value   

    def fillLFSR(self,rng):
        for i in range(rng):
            if i==0 :
                self.lfsr.append(1)
            elif i==(rng-1) :
                self.lfsr.append(0)
            else: 
                self.lfsr.append(random.randrange(2))

    def printLFSR(self):
        for i in range(len(self.lfsr)):
            print(self.lfsr[i])
    def run(self):
        res=self.execLFSR()
        if res==0:
            return self.execute(self.d)
        elif res==1:
            return self.execute(self.k)

    def execute(self,num):
        if num==self.d:
            for i in range(self.d):
                res=self.execLFSR()
                if i==(self.d-1):
                    return res
        elif num==self.k:
             for i in range(self.k):
                res=self.execLFSR()
                if i==(self.k-1):
                    return res

    def generateToFile(self,rng,filename):
        f=open(filename, "a",encoding="utf8")             
        for i in range (int(rng)):
            r=self.run()
           # print(r)
            f.write(str(r))
        f.close()

class Window(QMainWindow):
        def __init__(self, *args, **kwargs):
                lfsr=[]
                self.gen=RGenerator(lfsr)
                self.gen.fillLFSR(21)
                super(Window, self).__init__(*args, *kwargs)
                self.setWindowTitle("Generator samodecymujący Rueppela")
                #Tytułowy
                titleText = QLabel()
                titleText.setText("Generator samodecymujący Rueppela")
                titleText.setAlignment(Qt.AlignCenter)
                titleText.setStyleSheet("QLabel { color : rgb(178,183,187) ;}")
                titleText.setFont(QFont('Capriola',21))

                self.firstText=QLabel()
                self.firstText.setText("Uzupełnij dane do generacji")
                self.firstText.setStyleSheet("QLabel { color : rgb(122,193,66) ;}")
                self.firstText.setAlignment(Qt.AlignCenter)
                self.firstText.setFont(QFont('Capriola',18))

                #Pole Directory
                self.fDir = QLineEdit()
                self.fDir.setPlaceholderText("Ścieżka pliku")
                self.fDir.setStyleSheet("  background-color : rgb(178,183,187);color : rgb(0,42,92);")
                self.fDir.setFont(QFont('Arial',15))

                #Pole d
                self.dField = QLineEdit()
                self.dField.setPlaceholderText("d")
                self.dField.setStyleSheet("  background-color : rgb(178,183,187);color : rgb(0,42,92);")
                self.dField.setFont(QFont('Arial',15))
                validator = QIntValidator(1, 9, self)
                self.dField.setValidator(validator)

                #Pole k
                self.kField = QLineEdit()
                self.kField.setPlaceholderText("k")
                self.kField.setStyleSheet("  background-color : rgb(178,183,187);color : rgb(0,42,92);")
                self.kField.setFont(QFont('Arial',15))
                self.kField.setValidator(validator)

                #Pole dlugosci pliku
                self.fileLength = QLineEdit()
                self.fileLength.setPlaceholderText("Długość pliku")
                self.fileLength.setStyleSheet("  background-color : rgb(178,183,187);color : rgb(0,42,92);")
                self.fileLength.setFont(QFont('Arial',15))
                validator2 = QIntValidator(1, 1000000, self)
                self.fileLength.setValidator(validator2)
              

                #Wybór pliku
                selectButton = QPushButton()
                selectButton.setText("Wybierz plik")
                selectButton.clicked.connect(self.selectClick)
                selectButton.setFont(QFont('Impact',15))
                selectButton.setStyleSheet("  background-color : rgb(178,183,187);color : rgb(0,42,92);")

                #Przycisk zapisu
                saveButton = QPushButton()
                saveButton.setText("Generuj Plik")
                saveButton.clicked.connect(self.saveClick)
                saveButton.setFont(QFont('Impact',15))
                saveButton.setStyleSheet("  background-color : rgb(178,183,187);color : rgb(0,42,92);")

                #Help button
                self.helpButton = QPushButton()
                self.helpButton.setText("( i )")
                self.helpButton.clicked.connect(self.helpClick)
                self.helpButton.setFont(QFont('Impact',15))
                self.helpButton.setStyleSheet("  background-color : rgb(178,183,187);color : rgb(0,42,92);")
                
                helpLayout = QHBoxLayout()
                helpLayout.addWidget(self.helpButton)
                helpLayout.setAlignment(Qt.AlignLeft)
                helpLayoutW = QWidget()
                helpLayoutW.setLayout(helpLayout)

                fieldsLayout=QHBoxLayout()
                fieldsLayout.addWidget(self.dField)
                fieldsLayout.addWidget(self.kField)
                fieldsLayout.addWidget(self.fileLength)
                fieldsLayoutW=QWidget()
                fieldsLayoutW.setLayout(fieldsLayout)

                #Layout przycisku Wyboru pliku
                selectLayout = QHBoxLayout()
                selectLayout.addWidget(selectButton)
                selectLayout.addWidget(self.fDir)
               # selectLayout.addWidget(self.firstMessage)
                selectLayoutW = QWidget()
                selectLayoutW.setLayout(selectLayout)
               
                #Layout directory 
                dirLayout= QHBoxLayout()
                dirLayout.addWidget(saveButton)
                dirLayout.setAlignment(Qt.AlignCenter)
                dirLayWid=QWidget()
                dirLayWid.setLayout(dirLayout)
                #Layout Zaszyfrowanego i szyfruj
                
                     
                mainMenu = QVBoxLayout()
               
                mainMenu.addWidget(helpLayoutW)
                mainMenu.setAlignment(Qt.AlignCenter)
                mainMenu.addWidget(titleText)
                mainMenu.addWidget(self.firstText)
                mainMenu.addWidget(selectLayoutW)
                mainMenu.addWidget(fieldsLayoutW)
                mainMenu.addWidget(dirLayWid)
               # mainMenu.addWidget(textLayoutWid1)
                mainMenuWid= QWidget()
                mainMenuWid.setLayout(mainMenu)
                
               
                
                self.setCentralWidget(mainMenuWid)
        def helpClick(self):    
            info= QMessageBox()
            info.setWindowTitle("Info")
            info.setStyleSheet("QMessageBox{background-color : white}")
            info.setText("Autor: Krzysztof Sułkowski\nIndeks: 140785\n\nGenerator samodecymujący Rueppela\nGenerator samodecymujący Rueppela jest generatorem który steruje własnym wejściem zegarowym. Zależnie od wyniku wykonania się pierwszego cyklu rejestru LFSR liczba impulsów jest równa k albo d. LFSR jest taktowany d lub k krotnie (zależnie od pierwszego wykonania LFSR. Po wykonaniu ostatniego cyklu LFSR zwraca liczbę, która jest liczbą wynikową generatora.\nProgram przewiduje podanie liczb d i k w przedziale 1-9 oraz liczby generowanych liczb w przedziale 1-9999999")  
                # info.setFont(QFont("Arial",13))
            info.exec_()              
        def selectClick(self):
            filePath = filedialog.askopenfilename()
            if(len(filePath)>0):
                self.fDir.setText(filePath)
        def saveClick(self):#generacja będzie tutaj
            d=  self.fDir.text()
            c=len(d)
            if (c<1):
                info= QMessageBox()
                info.setWindowTitle("Błąd")
                info.setText("Niepoprawna nazwa pliku")
                info.setStyleSheet("QMessageBox{background-color : white}")
                info.exec()
            elif (d[c-1]=='/'):
                info= QMessageBox()
                info.setWindowTitle("Błąd")
                info.setText("Niepoprawna nazwa pliku ")
                info.setStyleSheet("QMessageBox{background-color : white}")
                info.exec()
            else:
                self.d=self.dField.text()
                self.k=self.kField.text()
                rng=self.fileLength.text()

                if (len(self.dField.text())==0 or len(self.kField.text())==0 or len(self.fileLength.text())==0):
                    info= QMessageBox()
                    info.setWindowTitle("Błąd")
                    info.setText("Niepoprawne dane ")
                    info.setStyleSheet("QMessageBox{background-color : white}")
                    info.exec()
                else:
                    f=  self.fDir.text()
                    self.gen.generateToFile(rng,f)
        def openEncrypted(self):
            print("Opening")
        

app = QApplication(sys.argv)

window = Window()
window.setFixedSize(500,300)
window.setStyleSheet("background-color: rgb(0,42,92);")
#window.setStyleSheet("background-color: pink;")
window.show()

app.exec()

