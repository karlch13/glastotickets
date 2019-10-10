#!/usr/bin/env python3
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os
import time
import subprocess

from glasto_ui import *
import sys
def get_platform():
    platforms = {
            'linux1' : 'Linux',
            'linux2' : 'Linux',
            'darwin' : 'OS X',
            'win32' : 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform
        
    return platforms[sys.platform]
def handleChromeDriver():
    system = get_platform()
    try:
        check = os.environ.get('CHROMEDRIVER')
        if 'CHROMEDRIVER' in os.environ:
            pass
        else:
            cd = os.path.dirname(os.path.abspath(__file__))
            find_resources = os.listdir(cd)
            for folder in find_resources:
                if folder == 'ChromeDriver':
                    cdir = ''.join([cd,'\\ChromeDriver'])
                    if os.path.isdir(cdir) == True:
                        find_resource = os.listdir(cdir)
                        for rsr in find_resource:
                            if rsr == "chromedriver":
                                cdir_1 = ''.join([cdir,'\\ChromeDriver\\chromedriver.exe'])
                                if system == 'Windows':
                                    old_path = os.getenv('PATH')
                                    commplete_path = old_path, '{};'.format(cdir_1)
                                    os.environ["CHROMEDRIVER"]= "{}".format(cdir_1)
                                    subprocess.call('SETX PATH "%PATH%;{};"'.format(''.join(commplete_path)))
                                else:
                                    cdir_1 = ''.join([cdir,'\\ChromeDriver\\chromedriver'])
                                    os.environ["CHROMEDRIVER"]= "{}".format(cdir_1)
                                    command = ['env', 'CHROMEDRIVER={}', 'sqsub', '-np', var1, '{}'.format(cdir,cdir_1)]
                                    subprocess.check_call(command)
    except Exception as e:
        raise e
handleChromeDriver()


import glasto as gl



class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main,self).__init__(parent)
        #uic.loadUi('first.ui', self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui = uic.loadUi('first_edit.ui', self)
        self.show()
        #self.Init_Ui()
        self.buttons()
        #self.handleChromeDriver()

    def buttons(self):
        self.ui.pushButton.clicked.connect(self.Init_Ui)
        self.ui.pushButton_2.clicked.connect(self.Exit_)
    def Init_Ui(self):
        # incognito??
        incognito = True
        # disable js??
        disablejs = False
        # disable images for faster loading?
        disableimages=True
        # change cache size?
        cache=4096
        # try a proxy with "8.8.8.8:88"
        proxy=None
        # run without browser - kind of pointless but faster.
        headless=False
        # refresh rate - seconds
        refreshrate = 0.0001
        # try one of these URLS
        # DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2020-deposits/worthy-farm/1300000"
        # DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/addregistrations"
        # DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2020/worthy-farm/1300001"
        # DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2020-ticket-coach-travel-deposits/worthy-farm/1450012"
        # DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2020-ticket-coach-travel-deposits/worthy-farm/1450013"
        url_input = self.ui.lineEdit_13.text()
        if len(url_input) > 0:
            DEPOSIT_20_URL = "{}".format(url_input)
        else:
            DEPOSIT_20_URL = "https://glastonbury.seetickets.com/event/glastonbury-2020-deposits/worthy-farm/1450000"

        number1 = self.ui.numLE1.text()
        number2 = self.ui.numLE2.text()
        number3 = self.ui.numLE3.text()
        number4 = self.ui.numLE4.text()
        number5 = self.ui.numLE5.text()
        number6 = self.ui.numLE6.text()

        postCode1 = self.ui.postcodeLE1.text()
        postCode2 = self.ui.postcodeLE2.text()
        postCode3 = self.ui.postcodeLE3.text()
        postCode4 = self.ui.postcodeLE4.text()
        postCode5 = self.ui.postcodeLE5.text()
        postCode6 = self.ui.postcodeLE6.text()

        numbers = [number1,number2,number3,number4,number5,number6]
        postCodes = [postCode1,postCode2,postCode3,postCode4,postCode5,postCode6]
        

        REG_DETAILS=[]
        for i in numbers:
            if len(i) > 0:
                for x in postCodes:
                    if len(x) > 0:
                        if postCodes.index(x) == numbers.index(i):
                            REG_DETAILS.append({'number':"{}".format(i),'postcode':"{}".format(x)})
            else:
                # Default REG_DETAILS
                REG_DETAILS=[
                    {
                        'number': "123456789", 
                        'postcode': "SW1 1SQ"
                    },
                    {
                        'number': "123456780", 
                        'postcode': "SW1 1SQ"
                    },
                ]
        # first is lead booker
        # REG_DETAILS=[
        #     {
        #         'number': "123456789", 
        #         'postcode': "SW1 1SQ"
        #     },
        #     {
        #         'number': "123456780", 
        #         'postcode': "SW1 1SQ"
        #     },
        # ]
        if len(REG_DETAILS) == 0:
            raise RuntimeError(
                "Must have at least one registration!")

        if len(REG_DETAILS) > 6:
            raise RuntimeError(
                "Cannot accept more than 1 + 5 registration details!")
        PHRASES_TO_CHECK = [gl.Twenty20.REGISTRATION_PHRASE]
        def attemptconnection(client, url):
            if client.establishconnection(url, phrases_to_check=PHRASES_TO_CHECK):
                print("success")
                print(client.attempts)
                try:
                    gl.tofile(client.content, "reg_page_2020.html")
                except:
                    pass
                if client.submit_registration(REG_DETAILS):
                    print("Registration details submission success!")
                    # save the html data
                    try:
                        gl.tofile(client.content, "reg_check_2020.html")
                    except:
                        pass

                    try:
                        # then click 'confirm' button and save html data again
                        client.clickbutton('Confirm')
                        gl.tofile(client.pagesource, "payment_page_2020.html")
                    except:
                        pass

                    # we cannot go beyond this automated, 
                    # since entering credit cards details automatically
                    # is terribly risky.
                    # instead leave the page open for us to do that
                    # and save the content

                    # todo: ????
                    return
                else:
                    print("Registration details submission failed!")

            # try again??
            # attemptconnection(client, url)

        # main
        s = gl.Service(gl.DRIVER_PATH)
        c = gl.Twenty20(s, timeout=4, refreshrate=refreshrate, verbose=False, 
            disablejs=disablejs, incognito=incognito, disableimages=disableimages, 
            cache=cache, headless=headless, proxy=proxy)
        attemptconnection(c, DEPOSIT_20_URL)

        # backup sleep 
        time.sleep(1000000) # Hack - leave it open to fill in details

    def Exit_(self):
        a = QtWidgets.QWidget()
        self.A1 = QtWidgets.QMessageBox.question(a, "Glasto", 'Do you want to exit ?!'
                                       , QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if self.A1 == QtWidgets.QMessageBox.Yes:
            sys.exit()
        else:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
