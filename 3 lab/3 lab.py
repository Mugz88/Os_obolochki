from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton

import sys
import os

class MainWindow(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        
        self.inputName =  QLineEdit("name")
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.inputName)
                    
        self.inputPath =  QLineEdit("path")
        self.mainLayoutt = QVBoxLayout()
        self.mainLayout.addWidget(self.inputPath)
    
        self.runCheak = QPushButton('Run')
        self.mainLayout.addWidget(self.runCheak)
        self.runCheak.clicked.connect(self.run)
        
        self.runNCheak = QPushButton('Run(NoCheak)')
        self.mainLayout.addWidget(self.runNCheak)
        self.runNCheak.clicked.connect(self.runNoCheak)
        
        self.setLayout(self.mainLayout)
        self.show()
    def run(self):
        path = self.inputPath.text()
        print('path=', path)
        name = self.inputName.text()
        print('name=', name)
        os.chdir(path)
        cheak=0
        for i in path:
            if (i!="/"):
                cheak+=1;
        if (cheak>36):
            print("gnoms mine so deep!", cheak)   
        else:
            print("normali",cheak)
            if not os.path.isdir(name):
                os.mkdir(name)
    def runNoCheak(self):
        name = self.inputName.text()
        print('name=', name)
        path = self.inputPath.text()
        print('path=', path)
        os.chdir(path)
        name=self.inputName.text()
        path=self.inputPath.text()
        if not os.path.isdir(name):
            os.mkdir(name)
app = QApplication(sys.argv)
mainWin=MainWindow()
sys.exit(app.exec())