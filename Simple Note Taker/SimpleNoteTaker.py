from PyQt5.QtWidgets import (
    QWidget,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QFileDialog,
    QAction,
    QMenu,
    QMenuBar,
    QHBoxLayout,
    QColorDialog)

import os


class SimpleNoteTaker(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.menubar = QMenuBar(self)
        file = QMenu("&File",self)
        file.addActions([QAction("Clear Note", self),
                         QAction("Save Note", self),
                         QAction("Load Note", self),
                         file.addSeparator(),
                         QAction("Exit", self)])

        file.actions()[0].triggered.connect(self.clearNote)
        file.actions()[1].triggered.connect(self.saveNote)
        file.actions()[2].triggered.connect(self.loadNote)
        file.actions()[4].triggered.connect(self.close)
        self.menubar.addMenu(file)

        self.setWindowTitle("Simple Note Taker")
        self.setMinimumSize(500, 300)
        self.resize(600, 600)
        self.show()

        self.textarea = QTextEdit(self)
        self.textarea.setPlaceholderText("Start typing...")
        self.boxlayout = QVBoxLayout()
        self.boxlayout.setMenuBar(self.menubar)
        self.boxlayout_h = QHBoxLayout()
        self.boxlayout.addWidget(self.textarea)

        self.colorpicker = QPushButton("...", self)
        self.colorpicker.setFixedWidth(40)
        self.colorpicker.setStatusTip("Color Picker")
        self.colorpicker.clicked.connect(self.colorPicker)
        self.clearnote = QPushButton("Clear Note", self)
        self.clearnote.clicked.connect(self.clearNote)
        self.boxlayout_h.addWidget(self.colorpicker)
        self.boxlayout_h.addWidget(self.clearnote)
        self.savenote = QPushButton("Save Note", self)
        self.savenote.clicked.connect(self.saveNote)
        self.loadnote = QPushButton("Load Note", self)
        self.loadnote.clicked.connect(self.loadNote)

        self.boxlayout.addLayout(self.boxlayout_h)
        self.boxlayout.addWidget(self.savenote)
        self.boxlayout.addWidget(self.loadnote)

        self.setLayout(self.boxlayout)

    def saveNote(self) -> None:
        text = self.textarea.toPlainText()

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        file, _ = QFileDialog.getSaveFileName(self, "Save Note","", "Simple Notes (*.simp)", options=options)

        if len(text) > 0 and file:
            with open(file, "w") as f:
                f.write(text)
        else:
            QMessageBox.warning(self, "Cannot save file", "Enter a file name")

    def loadNote(self) -> None:

        fileNote = QFileDialog.getOpenFileName(self, "Open Simp file","","Simp File (*.simp)")
        print(fileNote)
        if os.path.exists(fileNote[0]):
            with open(fileNote[0], "r") as file:
                self.textarea.setText(file.read())
        else:
            QMessageBox.warning(self, "File does not exist", "The file you are trying to load does not exist")

    def clearNote(self) -> None:
        text = self.textarea.toPlainText()

        if len(text) > 0:
            choice = QMessageBox.question(self,
                                          "Clear text area",
                                          "Clear text area? You will lose everything.",
                                          QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)

            match choice:
                case QMessageBox.Yes:
                    self.textarea.clear()
                case QMessageBox.No:
                    pass

    def colorPicker(self):
        textcolor = self.textarea.textColor()
        newcolor = QColorDialog.getColor()
        textcolor.setNamedColor(newcolor.name())


        if textcolor.isValid() and len(self.textarea.toPlainText()) >= 0:
            self.textarea.setTextColor(newcolor)
            self.textarea.setPlaceholderText("Start typing...")