import sys
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QDoubleValidator, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QMessageBox
from PyQt5.Qt import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
import requests
from bs4 import BeautifulSoup

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Brutto2Netto')
        self.window_width, self.window_height = 300, 300
        self.setFixedSize(self.window_width, self.window_height)

        #font
        font = QtGui.QFont()
        font.setPointSize(17)

        #title lable
        self.text1 = QtWidgets.QLabel(self)
        self.text1.setText('Input brutto & Tax')
        self.text1.move(60, 5)
        self.text1.setFont(font)
        self.text1.setAlignment(QtCore.Qt.AlignCenter)
        self.text1.adjustSize()

        # % lable
        self.text2 = QtWidgets.QLabel(self)
        self.text2.setText('%')
        self.text2.move(250, 54)
        self.text2.setFont(font)
        self.text2.setAlignment(QtCore.Qt.AlignCenter)
        self.text2.adjustSize()
        self.text2.setToolTip('Tax <b>24.74 %</b> is set by default for 2nd part of 2021')

        # netto lable
        self.text3 = QtWidgets.QLabel('0000000000', self)
        self.net = 0
        self.text3.move(85, 100)
        self.text3.setFont(font)
        self.text3.setAlignment(QtCore.Qt.AlignCenter)
        self.text3.adjustSize()
        # self.text3.setStyleSheet("QLabel {background-color: red;}")
        self.text3.setText('PLN')
        self.text3.setStyleSheet('color: #4e54c8; font-size: 17pt; font: bold')

        # byr lable
        self.text4 = QtWidgets.QLabel('0000000000', self)
        self.byr = 0
        self.text4.move(85, 150)
        self.text4.setFont(font)
        self.text4.setAlignment(QtCore.Qt.AlignCenter)
        self.text4.adjustSize()
        self.text4.setText('BYR')
        self.text4.setStyleSheet('color: #F37335; font-size: 17pt; font: bold')

        # usd lable
        self.text5 = QtWidgets.QLabel('0000000000', self)
        self.usd = 0
        self.text5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text5.move(85, 200)
        self.text5.setFont(font)
        self.text5.setAlignment(Qt.AlignCenter)
        self.text5.adjustSize()
        self.text5.setText('$')
        self.text5.setStyleSheet('color: green; font-size: 17pt; font: bold')

        # button
        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(90, 245)
        self.btn.setText('COUNT')
        self.btn.setFont(font)
        self.btn.setFixedWidth(120)
        self.btn.setFixedHeight(40)
        self.btn.clicked.connect(self.calculate)
        self.btn.setEnabled(False)

        # about button
        self.btn_about = QtWidgets.QPushButton(self)
        self.btn_about.move(270, 10)
        self.btn_about.setText('?')
        self.btn_about.setFixedWidth(20)
        self.btn_about.setFixedHeight(20)
        self.btn_about.clicked.connect(self.press_about)

        #input brutto
        self.inp_brutto = QtWidgets.QLineEdit(self)
        self.inp_brutto.move(70, 50)
        self.inp_brutto.setFont(font)
        validator = QRegExpValidator(QRegExp(r'[0-9]+'))#only digital validator
        self.inp_brutto.setValidator(validator)
        self.inp_brutto.setFixedWidth(86)
        self.inp_brutto.setMaxLength(6)
        self.inp_brutto.setFocus()
        self.inp_brutto.textChanged.connect(self.input_detected) #watching input QLineEdit

        # input tax
        self.inp_tax = QtWidgets.QLineEdit(self)
        self.inp_tax.move(170, 50)
        self.inp_tax.setFont(font)
        self.inp_tax.setInputMask('00.00')
        self.inp_tax.setValidator(QDoubleValidator())    #only digital + '.' and ',' validator
        self.inp_tax.setFixedWidth(72)
        self.inp_tax.setMaxLength(5)
        self.inp_tax.setText('27.74')

        self.headers = {
            'authority': 'www.kith.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'accept-language': 'en-US,en;q=0.9',
        }
        self.scrap_pln()
        self.scrap_usd()

    def input_detected(self):
        if len(self.inp_brutto.text()) > 0:
            self.btn.setEnabled(True)
        else:
            self.btn.setEnabled(False)

    def scrap_pln(self):
        url = 'https://select.by/brest/kurs-zlotogo'
        page = requests.get(url)
        doc = BeautifulSoup(page.text, 'html.parser')
        pt = doc.find('tr', class_='text-center h1').find_all('span')[1].text
        self.pln = float(pt.replace(',', '.'))

    def scrap_usd(self):
        url = 'https://select.by/brest/kurs-dollara'
        page = requests.get(url)
        doc = BeautifulSoup(page.text, 'html.parser')
        pt = doc.find('tr', class_='text-center h1').find_all('span')[1].text
        self.usd = float(pt.replace(',', '.'))

    def calculate(self):
        self.brutto = int(self.inp_brutto.text())
        self.tax = float(self.inp_tax.text())
        self.netto = int(self.brutto - (self.brutto / 100 * self.tax))
        self.netto2byr = int(self.netto * self.pln / 10)  # counting price in BYR
        self.byr2usd = int(self.netto2byr / self.usd)  # counting price in USD
        self.text3.setText(f"{self.netto} PLN")
        self.text4.setText(f"{self.netto2byr} BYR")
        self.text5.setText(f"{self.byr2usd} $")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return and len(self.inp_brutto.text()) > 0:
            self.calculate()
        if event.key() == Qt.Key_Escape:
            self.close()

    def press_about(self):
        about = QMessageBox()
        # about.setWindowIcon(QtGui.QIcon('icon.png'))
        about.setWindowTitle('Info')
        about.setText('Converter information')
        about.setIcon(QMessageBox.Information)
        about.setInformativeText('Program converts brutto Poland PLN into netto PLN, Belarusian BYR and American USD. Price of PLN and USD is taken from https://select.by')
        about.setDetailedText('Python + PyQT5\nMade by Evgeny Kolodenets\nhttps://github.com/ekolodenets')
        about.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    b2n = MainWindow()
    # b2n.setWindowIcon(QtGui.QIcon('icon.png')) # add icon if needed
    b2n.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')