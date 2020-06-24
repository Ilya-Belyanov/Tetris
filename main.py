import sys

from PyQt5 import QtWidgets

from interface import MyWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    sys.exit(app.exec())
