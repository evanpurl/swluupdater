# -*- coding: utf-8 -*-
import os.path
import urllib.request
import zipfile


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

from backend.getversion import getlatestversion


class Ui_Dialog(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(400, 300)
        Dialog.setWindowFlags(Dialog.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)
        self.versionlabel = QtWidgets.QLabel(Dialog)
        self.versionlabel.setGeometry(QtCore.QRect(10, 280, 191, 21))
        self.versionlabel.setText("Latest Version: {}".format(getlatestversion()))
        self.versionlabel.setObjectName("versionlabel")
        self.downloadbar = QtWidgets.QProgressBar(Dialog)
        self.downloadbar.setGeometry(QtCore.QRect(10, 240, 311, 23))
        self.downloadbar.setProperty("value", 0)
        self.downloadbar.setObjectName("downloadbar")
        # self.unzipbutton = QtWidgets.QPushButton(Dialog)
        # self.unzipbutton.setGeometry(QtCore.QRect(320, 265, 75, 23))
        # self.unzipbutton.setObjectName("unzipbutton")
        self.downloadbutton = QtWidgets.QPushButton(Dialog)
        self.downloadbutton.setGeometry(QtCore.QRect(320, 240, 75, 23))
        self.downloadbutton.setObjectName("downloadbutton")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(10, 60, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(90, 60, 301, 21))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(90, 100, 301, 21))
        self.label2.setText("")
        self.label2.setObjectName("label2")
        self.label3 = QtWidgets.QLabel(Dialog)
        self.label3.setGeometry(QtCore.QRect(15, 25, 355, 21))
        self.label3.setText("Please select an empty folder, or an existing SWLU Installer Directory.")
        self.label3.setObjectName("label3")


        self.downloadbutton.clicked.connect(self.Download)
        self.pushButton.clicked.connect(self.selectdirectory)
        #self.unzipbutton.clicked.connect(self.unzip)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "SWLU Updater"))
        self.downloadbutton.setText(_translate("Dialog", "Download"))
        # self.unzipbutton.setText(_translate("Dialog", "Unzip"))
        self.pushButton.setText(_translate("Dialog", "Set Directory"))

    def selectdirectory(self):
        file = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        self.label.setText(file)
        return file

    def Handle_Progress(self, blocknum, blocksize, totalsize):
        ## calculate the progress
        readed_data = blocknum * blocksize

        if totalsize > 0:
            download_percentage = readed_data * 100 / totalsize
            self.downloadbar.setValue(int(download_percentage))
            QApplication.processEvents()

    # method to download any file using urllib
    def Download(self):
        try:
            # specify the url of the file which is to be downloaded
            down_url = 'https://www.x3collective.com/LU/SWLU/SWLULatest.zip'  # specify download url here

            if self.label.text() == "":
                error = QMessageBox()
                error.setWindowTitle("Directory Error")
                error.setText("You must select a directory before downloading!")
                error.setIcon(QMessageBox.Critical)
                retval = error.exec_()
            else:
                self.downloadbutton.setEnabled(False)
                self.pushButton.setEnabled(False)
                # self.unzipbutton.setEnabled(False)
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'SWLU Updater')]
                urllib.request.install_opener(opener)
                self.label2.setText("Downloading!")
                urllib.request.urlretrieve(down_url, self.label.text() + "/SWLULatest.zip", self.Handle_Progress)
                opener.close()
                zip_ref = zipfile.ZipFile(self.label.text() + "/SWLULatest.zip", 'r')
                for a, b in enumerate(zip_ref.namelist()):
                    self.label2.setText("Extracting {}".format(b))
                    download_percentage = (((a + 1) * 100) / len(zip_ref.namelist()))
                    self.downloadbar.setValue(int(download_percentage))
                    self.downloadbar.setFormat("%.02f %%" % download_percentage)
                    zip_ref.extract(path=self.label.text(), member=b)
                zip_ref.close()
                os.remove(self.label.text() + "/SWLULatest.zip")
                self.label2.setText("Done! :)")
                self.downloadbutton.setEnabled(True)
                self.pushButton.setEnabled(True)
                # self.unzipbutton.setEnabled(True)
        except urllib.request.HTTPError as e:
            print(e)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
