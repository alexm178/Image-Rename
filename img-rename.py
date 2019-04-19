import sys
from PyQt5.QtWidgets import *
import os
import csv

class CSVGroup(QGroupBox):
    def __init__(self, parent=None):
        super(CSVGroup, self).__init__(parent)
        self.parent = parent
        self.imgFileNames = []
        self.nameDuplicates = []
        self.csvBox = QVBoxLayout()
        self.createDisplayTable()
        self.createUploadButton()
        self.setLayout(self.csvBox)

    def createUploadButton(self):
        self.csvUploadButton = QPushButton("Import CSV")
        self.csvUploadButton.clicked.connect(self.csvUpload)
        self.csvBox.addWidget(self.csvUploadButton)

    def createDisplayTable(self):
        self.nameTable = QTableWidget(10, 2)
        self.nameTable.setHorizontalHeaderLabels(["Old Name", "New Name"])
        self.nameTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.nameTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.csvBox.addWidget(self.nameTable)

    def csvUpload(self):
        csvFile = QFileDialog.getOpenFileName(filter = "csv(*.csv)")[0]
        try:
            self.readCSV(csvFile)
            self.displayNames()
        except(err):
            print(err)
            return

    def readCSV(self, csvFile):
        with open(csvFile, mode='r') as csv_file:
            reader = csv.reader(csv_file)
            index = 1
            for row in reader:
                fileNames = [row[0], row[1]]
                if any(row[0] in sublist for sublist in self.imgFileNames):
                    self.nameDuplicates.append(fileNames)
                else:
                    self.imgFileNames.append(fileNames)
                index = index + 1

    def displayNames(self):
        self.alertParent()
        self.nameTable.setRowCount(len(self.imgFileNames))
        row = 0
        for imgNames in self.imgFileNames:
            self.nameTable.setItem(row, 0, QTableWidgetItem(imgNames[0]))
            self.nameTable.setItem(row, 1, QTableWidgetItem(imgNames[1]))
            row = row + 1

    def alertParent(self):
        self.parent.handleCSV(self.imgFileNames)

class FolderGroup(QGroupBox):
    def __init__(self, parent=None):
        super(FolderGroup, self).__init__(parent)

        self.parent = parent
        self.folder = None
        self.createWidgets();


    def createWidgets(self):
        verticalBox = QVBoxLayout()
        verticalBox.addWidget(self.scrollBox())
        verticalBox.addWidget(self.folderUploadButton())
        self.setLayout(verticalBox)

    def scrollBox(self):
        scroll = QScrollArea()
        widget = QWidget()
        grid = QGridLayout(widget)
        if self.folder == None:
            row = 0
            for filenames in self.parent.imgNames:
                print(row)
                label = QLabel("No Folder Selected")
                entry = QLineEdit(filenames[0])
                grid.addWidget(label, row, 0)
                grid.addWidget(entry, row, 1)
                row = row + 1
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)
        return scroll

    def folderUploadButton(self):
        button = QPushButton("Select Folder")
        button.clicked.connect(self.folderUpload)
        return button

    def folderUpload(self):
        print('test')



class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.text = "test"
        self.setGeo()
        self.createWidgets()
        self.show()


    def setGeo(self):
        # self.resize(800, 800)
        self.setMinimumHeight(500)
        self.setMinimumWidth(800)
        self.grid = QGridLayout()
        # self.grid.setRowStretch(1, 1)
        # self.grid.setRowStretch(2, 1)
        # self.grid.setColumnStretch(0, 1)
        # self.grid.setColumnStretch(1, 1)
        self.setLayout(self.grid)
        self.setWindowTitle("Image Rename")



    def createWidgets(self):
        self.csvGroup = CSVGroup(self)
        self.grid.addWidget(self.csvGroup, 0, 0)

    def handleCSV(self, names):
        self.imgNames = names
        self.folderGroup = FolderGroup(self)
        self.grid.addWidget(self.folderGroup, 0, 1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
