from PyQt5.QtWidgets import *
import sys
#from PyQt5 import QMainWindow, QInputDialog

def get_api_key():
    user_api_key, ok  = (QInputDialog.getText("Input", 'Enter API Key'))#, 'Input Dialog', 'Enter your API key:'))
    if ok:
        print(f'API key: {user_api_key}')

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setWindowTitle("API Key")

    def initUI(self):
        self.user_api_key, ok  = (QInputDialog.getText(self, "Input", 'Enter API Key'))#, 'Input Dialog', 'Enter your API key:'))
        if ok:
            print(f'API key: {self.user_api_key}')
        #self.apiKeyDialog = QInputDialog()
        #self.mainWindow.addWidget(self.apiKeyDialog)

def main():
    app = QApplication(sys.argv)
    window = mainWindow()
    #window.show()
    sys.exit(app.exec_())

main()