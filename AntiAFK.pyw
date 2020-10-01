from PyQt5.QtGui import*
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys, time, os
import pyautogui

class MovingThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        print("MovingThread Initialized")
        self.createVars()

    def run(self):
        print("MT - Running")
        self.createVars()
        self.delay = screen.retrieveSpinValue()*4
        while True:
            moving = self.isMoving()
            if moving == False and self.typing == False:
                self.falseCounter += 1
            elif moving == True or self.typing == True:
                self.falseCounter = 0
            if (self.falseCounter % self.delay == 0) and (self.falseCounter > 0):
                self.trigger()

    def createVars(self):
        self.falseCounter = 0
        self.typing = False
        self.delay = 40
        print("MT - Vars reinitialized")
                
    def isMoving(self): #Detects if mouse is moving
        delay = 0.25
        firstPos = pyautogui.position()
        time.sleep(delay)
        secondPos = pyautogui.position()
        if secondPos == firstPos:
            return False
        else:
            return True

    def on_press(self, key):
        self.typing = True

    def on_release(self, key):
        self.typing = False

    def trigger(self):
        print("MT - Pressing F15")
        pyautogui.press('f15')

class Window(QWidget):
    def __init__(self):
        self.createVars()

        iconPath = self.resource_path(".\Resources\icon.png")
        icon = QIcon(iconPath)
        
        QWidget.__init__(self)
        self.setFixedSize(250, 125)

        self.setWindowTitle("Anti AFK")
        self.setWindowIcon(icon)

        #MAIN SOFTWARE GUI SETUP

        layout = QGridLayout()
        self.setLayout(layout)

        label = QLabel("Enable Anti-AFK")
        layout.addWidget(label, 1, 0, 1, 2)

        self.startProgramCheckBox = QCheckBox()
        self.startProgramCheckBox.setChecked(False)
        self.startProgramCheckBox.stateChanged.connect(lambda:self.enableBox(self.startProgramCheckBox))
        layout.addWidget(self.startProgramCheckBox, 1, 2, 1, 1)

        label = QLabel("Delay (in seconds):")
        layout.addWidget(label, 2,0)

        self.spinBox = QSpinBox()
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(9999)
        self.spinBox.setValue(10)
        layout.addWidget(self.spinBox, 3, 0 ,1, 3)

        #SYSTEM TRAY SETUP        


        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(icon)
        self.tray.setVisible(True)

        
        #self.mainMenuBar = QMenuBar(self)
        #exitAction = QAction('Exit', self)
        #exitAction.triggered.connect(qApp.quit)
        #self.mainMenuBar.addAction(exitAction)
        #self.mainMenuBar.setGeometry(QRect(0, 0, 46, 30))
        
        menu = QMenu(self)

        restore = QAction("Restore", self)
        restore.triggered.connect(self.restoreSoftware)
        menu.addAction(restore)
        
        close = QAction("Quit", self)
        close.triggered.connect(qApp.quit)
        menu.addAction(close)

        self.tray.setContextMenu(menu)

    def createVars(self):
        self.messageShown = False #QOL - only show first time or whenever a state has been changed.
        self.programRunning = False
        self.messageTime = 500

    def restoreSoftware(self):
        self.show()

    def exitSoftware(self):
        self.tray.setVisible(False)
        qApp.quit()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        if not self.messageShown:
            if self.programRunning:
                self.tray.showMessage(
                    "Anti AFK",
                    ("Minimized to Tray.\nApplication will continue to check for AFK every %s seconds."%str(self.spinBox.value())),
                    QSystemTrayIcon.Information,
                    self.messageTime
                    )
            else:
                self.tray.showMessage(
                    "Anti AFK",
                    "Minimized to Tray. Program is not currently checking for AFK.",
                    QSystemTrayIcon.Information,
                    self.messageTime
                    )                
            self.messageShown = True
        
    def keyPressEvent(self, e):
        if e.key():
            movingThread.falseCounter = 0
            
    def enableBox(self, cb):
        if not movingThread.isRunning(): 
            self.spinBox.setEnabled(False)
            print("MT - starting thread.")
            movingThread.start()
            self.programRunning = True
            self.messageShown = False
        else:
            self.spinBox.setEnabled(True)
            print("MT - Stopping thread.")
            movingThread.terminate()
            self.programRunning = False
            self.messageShown = False

    def retrieveSpinValue(self):
        return self.spinBox.value()

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    
    screen = Window()
    screen.setWindowFlags(screen.windowFlags() & Qt.CustomizeWindowHint)
    screen.setWindowFlags(screen.windowFlags() & ~Qt.WindowMinMaxButtonsHint)
    screen.show()
    
    movingThread = MovingThread()
    app.exec_()

