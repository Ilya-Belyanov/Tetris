from PyQt5.QtWidgets import QPushButton, QDialog, QRadioButton, QButtonGroup,QVBoxLayout,QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5 import QtGui
from settingsTetris import Setting as st

class ChangeSize(QDialog):
    '''Dialog window'''
    SizeSignal = pyqtSignal()
    def __init__(self):
        super(ChangeSize, self).__init__()
        self.initUI()
        self.loadStyle()

    def loadStyle(self):
        styledialog = "static/styledialog.css"
        with open(styledialog, "r") as f:
            self.setStyleSheet(f.read())

    def initUI(self):
        lb = QLabel('Choise height x width',self)
        radio = QRadioButton('15х10',self)
        radio.setChecked(True)
        radio_2 = QRadioButton('18х12', self)
        radio_3 = QRadioButton('20х15', self)
        radio_4 = QRadioButton('25х20', self)

        self.radioGroup=QButtonGroup()
        self.radioGroup.addButton(radio)
        self.radioGroup.addButton(radio_2)
        self.radioGroup.addButton(radio_3)
        self.radioGroup.addButton(radio_4)
        self.radioGroup.buttonClicked.connect(self.buttonYesClicked)

        self.radioDict = {radio:'1510',radio_2:'1812',radio_3:'2015',radio_4:'2520'}

        layout = QVBoxLayout(self)
        layout.addWidget(lb)
        layout.addWidget(radio)
        layout.addWidget(radio_2)
        layout.addWidget(radio_3)
        layout.addWidget(radio_4)

        qbtn = QPushButton('Cancel', self)
        qbtn.clicked.connect(self.close)
        layout.addWidget(qbtn)

        self.setWindowTitle('Change Size')
        self.setWindowIcon(QtGui.QIcon('Photo/Settings.jpg'))
        self.setFixedSize(250, 200)

    def buttonYesClicked(self,button):
        '''Change parameters of main window'''
        st.board_h = int(self.radioDict[button][:2])
        st.board_w = int(self.radioDict[button][2:])
        self.SizeSignal.emit()
        self.close()

