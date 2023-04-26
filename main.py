import sys
from Crypto.Cipher import AES
from PySide6 import QtCore, QtWidgets


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D&E")
        self.setLayout(QtWidgets.QVBoxLayout(self))
        self.keyEdit = QtWidgets.QLineEdit(self)
        self.ivEdit = QtWidgets.QLineEdit(self)
        self.inputEdit = QtWidgets.QLineEdit(self)
        self.outputEdit = QtWidgets.QLineEdit(self)
        self.inputBtn = QtWidgets.QPushButton("...", self)
        self.outputBtn = QtWidgets.QPushButton("...", self)
        self.layout1 = QtWidgets.QHBoxLayout()
        self.layout2 = QtWidgets.QHBoxLayout()
        self.layout1.addWidget(self.inputEdit)
        self.layout1.addWidget(self.inputBtn)
        self.layout2.addWidget(self.outputEdit)
        self.layout2.addWidget(self.outputBtn)
        
        self.keyEdit.setPlaceholderText("KEY")
        self.ivEdit.setPlaceholderText("IV")
        self.layout().addWidget(self.keyEdit)
        self.layout().addWidget(self.ivEdit)
        self.layout().addItem(self.layout1)
        self.layout().addItem(self.layout2)
        self.encrypoBtn = QtWidgets.QPushButton("Encrypo", self)
        self.decrypoBtn = QtWidgets.QPushButton("Decrypo", self)
        self.layout().addWidget(self.encrypoBtn)
        self.layout().addWidget(self.decrypoBtn)
        self.inputBtn.clicked.connect(self.get_input)
        self.encrypoBtn.clicked.connect(self.encrypo)
        self.decrypoBtn.clicked.connect(self.decrypo)
        
    @QtCore.Slot()
    def get_input(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open", QtCore.QCoreApplication.applicationDirPath())
        
        if path is not None:
            self.inputEdit.setText(path)
            self.outputEdit.setText(path + '.tmp')
        
    @QtCore.Slot()
    def get_output(self):
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save", QtCore.QCoreApplication.applicationDirPath())
        
        if path is not None:
            self.outputEdit.setText(path)
            
    @QtCore.Slot()
    def encrypo(self):
        data = b''
        name1 = self.inputEdit.text()
        name2 = self.outputEdit.text()
        if len(name1) == 0 and len(name2):
            return
        
        with open(name1, "rb") as infile:
            data = infile.read()
        
        key = bytes.fromhex(self.keyEdit.text())
        iv = bytes.fromhex(self.ivEdit.text())
        aes = AES.new(key, AES.MODE_CBC, iv)
        data = aes.encrypt(self.pkcs7_padding(data))
        
        with open(name2, "wb") as outfile:
            outfile.write(data)
            
    @QtCore.Slot()
    def decrypo(self):
        data = b''
        name1 = self.inputEdit.text()
        name2 = self.outputEdit.text()
        if len(name1) == 0 and len(name2):
            return
        
        with open(name1, "rb") as infile:
            data = infile.read()
        
        key = bytes.fromhex(self.keyEdit.text())
        iv = bytes.fromhex(self.ivEdit.text())
        aes = AES.new(key, AES.MODE_CBC, iv)
        data = aes.decrypt(data)
        data = self.pkcs7_depadding(data)
        with open(name2, "wb") as outfile:
            outfile.write(data)
    
    def pkcs7_padding(self, data):
        padding_size = 16 - (len(data) % 16)
        return data + (chr(padding_size) * padding_size).encode("ascii")
    
    def pkcs7_depadding(self, data):
        padding = int(data[-1])
        return data[0:-padding]          
                

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    w = MainWindow()
    w.show()
    
    sys.exit(app.exec())
        
        