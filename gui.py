import os
import sys
from threading import Thread
from PyQt5.QtWidgets import QMainWindow,QVBoxLayout,QWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
import manage

from PyQt5.QtWebEngineWidgets import *


def start_startview():
    app=QApplication(sys.argv)
    mainWindow=QMainWindow()
    widget=QWidget()

    web=QWebEngineView()

    web.load(QUrl('http://localhost:8000/'))
    #
    # web=QWebView()
    # web.load(QUrl('http://localhost:8000/'))
    mainWindow.setCentralWidget(web)
    mainWindow.show()
    sys.exit(app.exec_())


def start_startdjango():
    if sys.platform in['win32','win64']:
        os.system("python manage.py runserver {}:{}".format('127.0.0.1','8000'))
    else:
        os.system("python3 manage.py runserver {}:{}".format('127.0.0.1', '8000'))

if __name__=='__main__':
    Thread(target=start_startdjango).start()
    start_startview()
