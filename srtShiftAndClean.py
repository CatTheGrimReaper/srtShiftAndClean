from PyQt5 import QtGui
from PyQt5.QtWidgets import *
import re
import srt
import datetime

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("(Japanese) SRT Shifter & Cleaner")

        self.filenames = []
        self.lines = []
        self.timeShift = 0
        self.currentlySelected = 0

        layout = QVBoxLayout()
        self.currentSelectionLabel = QLabel("0")
        self.currentSelectionLabel.setStyleSheet("font-size: 40px")
        self.currentSelectionLabel.setText(self.currentlySelected.__str__())
        animeNameLabel = QLabel("Select subtitles: ")
        chooseSRTButton = QPushButton("Select SRT files")
        chooseSRTButton.clicked.connect(self.getSRT)
        chooseSRTButton.setStyleSheet("background: lightgreen")
        cleanSubsButton = QPushButton("Clean subtitles")
        cleanSubsButton.clicked.connect(self.cleanSubs)
        timeBox = QSpinBox()
        timeBox.valueChanged.connect(self.getTimeShift)
        timeBox.setMaximum(999999)
        shiftNegativeButton = QPushButton("Shift to show subs earlier")
        shiftNegativeButton.clicked.connect(self.shiftSubsNegative)
        shiftPositiveButton = QPushButton("Shift to show subs later")
        shiftPositiveButton.clicked.connect(self.shiftSubsPositive)

        layout.addWidget(QLabel("Currently selected Subtitles"))
        layout.addWidget(self.currentSelectionLabel)
        layout.addWidget(animeNameLabel)
        layout.addWidget(chooseSRTButton)
        layout.addWidget(cleanSubsButton)
        layout.addWidget(QLabel("Select shift for subtitles (milliseconds)"))
        layout.addWidget(timeBox)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(shiftNegativeButton)
        buttonLayout.addWidget(shiftPositiveButton)
        layout.addLayout(buttonLayout)

        SRTFilesList = QWidget()
        SRTFilesList.setLayout(layout)

        self.setCentralWidget(SRTFilesList)
        self.setMinimumWidth(600)
        self.setMinimumHeight(300)


    def getTimeShift(self, value):
        self.timeShift = value
        print(self.timeShift)

    def getSRT(self):
        self.filenames = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "", "SRT Files (*.srt)")
        self.currentSelectionLabel.setText(len(self.filenames[0]).__str__())

    def cleanSubs(self):
        for filename in self.filenames[0]:
            with open(filename, "r", encoding="utf8") as file:
                lines = file.readlines()
                file.close()
            validLines = []
            for line in lines:
                line = re.sub("（.*）", "", line)
                line = re.sub("\\(.*\\)", "", line)
                validLines.append(line)
            sub = ''.join(map(str, validLines))
            subGen = srt.parse(sub)
            subtitles = list(subGen)
            clean = []
            for sub in subtitles:
                if sub.content is not None:
                    clean.append(sub)
            final = srt.compose(clean)
            with open(filename, "w", encoding="utf8") as file:
                for f in final:
                    file.write(f)
                file.close()
        dlg = QDialog(self)
        dlg.setWindowTitle("Done!")
        layout = QVBoxLayout()
        dlg.setLayout(layout)
        dlg.layout().addWidget(QLabel("Success!"))
        dlg.exec_()

    def shiftSubsNegative(self):
        for filename in self.filenames[0]:
            with open(filename, "r", encoding="utf8") as file:
                lines = file.readlines()
                file.close()
            sub = ''.join(map(str, lines))
            subGen = srt.parse(sub)
            subtitles = list(subGen)
            retimed = []
            for sub in subtitles:
                sub.start = sub.start - datetime.timedelta(milliseconds=self.timeShift)
                sub.end = sub.end - datetime.timedelta(milliseconds=self.timeShift)
                retimed.append(sub)
            final = srt.compose(retimed)
            with open(filename, "w", encoding="utf8") as file:
                for f in final:
                    file.write(f)
                file.close()
        dlg = QDialog(self)
        dlg.setWindowTitle("Retiming done!")
        layout = QVBoxLayout()
        dlg.setLayout(layout)
        dlg.layout().addWidget(QLabel("Retiming successful!"))
        dlg.exec_()

    def shiftSubsPositive(self):
        for filename in self.filenames[0]:
            with open(filename, "r", encoding="utf8") as file:
                lines = file.readlines()
                file.close()
            sub = ''.join(map(str, lines))
            subGen = srt.parse(sub)
            subtitles = list(subGen)
            retimed = []
            for sub in subtitles:
                sub.start = sub.start + datetime.timedelta(milliseconds=self.timeShift)
                sub.end = sub.end + datetime.timedelta(milliseconds=self.timeShift)
                retimed.append(sub)
            final = srt.compose(retimed)
            with open(filename, "w", encoding="utf8") as file:
                for f in final:
                    file.write(f)
                file.close()
        dlg = QDialog(self)
        dlg.setWindowTitle("Retiming done!")
        layout = QVBoxLayout()
        dlg.setLayout(layout)
        dlg.layout().addWidget(QLabel("Retiming successful!"))
        dlg.exec_()



app = QApplication([])
QApplication.setStyleSheet(app, "QPushButton{background-color: #d1d1d1; font-size:20px; border:1px solid black}"
                                "QPushButton:hover{border:2px solid black}"
                                "QLabel{font-size:20px} "
                                "QSpinBox{border:2px solid black; height: 30px; font-size:20px}")

window = MainWindow()
window.show()

app.exec_()
