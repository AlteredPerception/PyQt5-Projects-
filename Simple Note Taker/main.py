import sys
from PyQt5.QtWidgets import QApplication
from SimpleNoteTaker import SimpleNoteTaker

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("windows-vista")
    simple = SimpleNoteTaker()
    sys.exit(app.exec_())