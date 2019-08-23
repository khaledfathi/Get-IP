#!/usr/bin/python3

#Description --: Get External IP address and send it to Email 
#Created ------: 21/08/2019
#version ------: 0.1
#author -------: Khaled [KhaledFathi@protonmail.com]
#Code ---------: Python 3.6.8 | PyQT5 5.13.0
#Repository ---: None 

import requests , datetime , smtplib , os , sys , threading , shutil
from PyQt5.QtWidgets import QApplication , QMainWindow , QWidget , QPushButton , QLabel , \
     QLineEdit , QTabWidget , QSpinBox , QFileDialog , QTextBrowser , QVBoxLayout ,QSpinBox,\
     QCheckBox ,QInputDialog, QMessageBox  
from PyQt5.QtGui import QPixmap , QIcon  , QFont 
from PyQt5.Qt import Qt

#################
## Main Window ##
#################
class app (QMainWindow):
    "Application main window "
    def __init__ (self):
        super().__init__()
        self.title = "Get/Send External IP Address"
        self.left , self.top , self.width , self.height = 100,100,450,400
        self.initUI()
    
    def initUI(self) :
        "main window "
        self.setWindowTitle(self.title)
        self.setGeometry(self.left , self.top , self.width , self.height)
        self.setMaximumHeight(self.height)
        self.setMinimumHeight(self.height)
        self.setMaximumWidth(self.width)
        self.setMinimumWidth(self.width)
        self.tabs()
        self.buttons()
        self.show()
    
    def tabs(self):
        "Tabs widgets"
        self.tab_1 = tab_send_ip(self)
        self.tab_2 = tab_config(self,self.tab_1)
        self.tab_3 = tab_about(self)
        self.tab_4 = tab_source_code(self)
        all_tabs = QTabWidget(self)
        all_tabs.setGeometry(10,10,430,340)
        
        all_tabs.addTab(self.tab_1,QIcon("ip"),"Get/Send IP")
        all_tabs.addTab(self.tab_2 , QIcon("config"),"Config")
        all_tabs.addTab(self.tab_3,QIcon("about"),"About")
        all_tabs.addTab(self.tab_4 , QIcon("source_code"),"Source Code")
    
    def buttons(self):
        "buttons widget"
        quit_ = QPushButton("Quit" , self)
        quit_.move(180,360)
        quit_.setStyleSheet("background:red;color:white")
        quit_.setToolTip("Exit")
        quit_.clicked.connect(self.close)
        
##################
## Tabs Widgets ##
##################

## Tab send IP ##
class tab_send_ip (QWidget):
    "(parent : QWidget)"
    def __init__(self,parent):
        super().__init__(parent)
        self.labels()
        self.buttons()
        self.show()
    
    def labels (self):
        "labels widgets"
        self.res = QLabel("Your IP = 0.0.0.0",self)
        self.res.setGeometry(0,20,430,50)
        self.res.setFont(QFont("Time",18))
        self.res.setAlignment(Qt.AlignCenter)
        
        self.stat = QLabel(". . . ." , self)
        self.stat.setGeometry(0,170,430,100)
        self.stat.setFont(QFont("Time",25))
        self.stat.setAlignment(Qt.AlignCenter)

    def buttons (self):
        "buttons widget"
        get_button = QPushButton("Get IP",self)
        get_button.setFont(QFont("Time",15))
        get_button.setGeometry (40,100,160,40)
        get_button.clicked.connect(self.get_ip_button)
        
        self.send_button = QPushButton("Send to E-mail",self)
        self.send_button.setFont(QFont("Time", 15))
        self.send_button.setGeometry(230,100,160,40)
        self.send_button.setDisabled(True)
        self.send_button.clicked.connect(self.send_email_button)
    
    def error (self, error):
        QMessageBox.about(self,"Sending Error" , error)
        
    #################
    ## Slot Method ##
    #################
    def get_ip_button(self):
        get_ip().start()
    
    def send_email_button (self):
        send_to,key_press =  QInputDialog.getText(self , "Send To" , "Send To E-mail")
        if send_to and key_press :
            if "@" in send_to and "." in send_to :
                send_email(send_to).start()
            else:
                QMessageBox.about(self, "E-mail Error", "Wrong E-mail format\nE-mail should be in form [ name@domain.com ]")

## Tab Configurations ##
class tab_config (QWidget):
    "(parent=None : QWidget , tab_1=None : object) \
    tab_1 is another object that need to change some of its attribute from here "
    def __init__(self,parent,tab_1="None"):
        super().__init__(parent)
        self.tab_1 = tab_1 
        self.labels()
        self.data_entry()
        self.check_boxs()
        self.buttons()
        
        self.check_config_mode() #set configuration when app start 

        self.show()
        
    def labels(self):
        "labels widget"
        smtp_lable = QLabel("SMTP Server",self)
        smtp_lable.move(20,50)
        port_lable = QLabel("Port" ,self)
        port_lable.move(250,50)
        account_lable = QLabel("Account" , self)
        account_lable.move(20,90)
        password_lable = QLabel("Password",self)
        password_lable.move(20,130)
        subject_lable = QLabel("Message Subject",self)  
        subject_lable.move(20,170)

    def data_entry (self):
        "inputs widgets"
        self.smtp_value = QLineEdit(self)
        self.smtp_value.move(110,45)
        self.smtp_value.setToolTip("Ex : smtp.google.com")
        
        self.port_value = QSpinBox(self)
        self.port_value.move(285,45)
        self.port_value.setMinimum(1)
        self.port_value.setMaximum(65535)
        self.port_value.setValue(587)
        self.port_value.setToolTip("1 to 65535")
        
        self.account_value = QLineEdit(self)
        self.account_value.move(110,85)
        self.account_value.setToolTip("Full Sender Email Address")
        
        self.password_value = QLineEdit(self)
        self.password_value.move(110,125)
        self.password_value.setToolTip("Sender Email Password")
        self.password_value.setEchoMode(QLineEdit.Password)
        
        self.subject_value = QLineEdit(self)
        self.subject_value.move(130,165)
        self.subject_value.setToolTip("Message subject")
        
                    
    def check_boxs(self):
        "check_boxs widget"
        self.no_config = QCheckBox("Set Default Configuration" , self)
        self.no_config.move(20,10)
        self.no_config.setChecked(True)
        self.no_config.clicked.connect(self.default_config)
        
        self.show_password = QCheckBox("Show Password",self)
        self.show_password.move(250,127)
        self.show_password.clicked.connect(self.show_hide_password)
    
    def buttons (self):
        "buttons widget"
        self.import_button = QPushButton(QIcon("import"),"Import",self)
        self.import_button.move(180,215)
        self.import_button.setToolTip("Import Configuration from file")
        self.import_button.clicked.connect(self.import_config)
        
        self.export_button = QPushButton(QIcon("export")," Export",self)
        self.export_button.move(180,245)
        self.export_button.setToolTip("Export Configuration to file")
        self.export_button.clicked.connect(self.export_config)
        
        self.save_button = QPushButton("Save Configuration",self)
        self.save_button.setGeometry(20,220 , 130,40)
        self.save_button.setStyleSheet("background:green")
        self.save_button.clicked.connect(self.save_custom_config)
        
        self.clear_button = QPushButton(" Clear",self)
        self.clear_button.move(290,233)
        self.clear_button.setIcon(QIcon("clear"))
        self.clear_button.clicked.connect(self.clear_all)
    
    ##################
    ## Core Methods ##
    ##################
    def disable_enable_config(self,stat):
        "disable or enable all configuration inputs (stat : bool)"
        self.show_password.setDisabled(stat)
        self.smtp_value.setDisabled(stat)
        self.port_value.setDisabled(stat)
        self.account_value.setDisabled(stat)
        self.password_value.setDisabled(stat)
        self.subject_value.setDisabled(stat)
        self.export_button.setDisabled(stat)
        self.import_button.setDisabled(stat)
        self.clear_button.setDisabled(stat)
        self.save_button.setDisabled(stat)
    
    def clear_all (self):
        "clear all configuration inputs"
        self.smtp_value.clear()
        self.account_value.clear()
        self.password_value.clear()
        self.subject_value.clear()
   
    def config_from_file (self,file="default_config"):
        "read and set configuration values into config inputs"
        with open (file,"r") as f :
            config = f.read().split(":")
        #index 0 if mode (not use here)
        self.smtp_value.setText(config[0])
        self.port_value.setValue(int(config[1]))
        self.account_value.setText(config[2])
        self.password_value.setText(config[3])
        self.subject_value.setText(config[4])
    
    def read_config(self):
        return {
            "smtp" : self.smtp_value.text(),\
            "port" : self.port_value.value(),\
            "account" : self.account_value.text(),\
            "password" : self.password_value.text(),\
            "subject" : self.subject_value.text()
            }
            
    def check_config_mode (self):
        try:
            with open ("custom_config","r") as f :
                self.config_from_file("custom_config")
            self.disable_enable_config(False)
            self.no_config.setChecked(False)
            self.tab_1.send_button.setDisabled(False)
        except :
            self.default_config()
            
            
    ##################
    ## Slot Methods ##
    ##################
            
    def show_hide_password(self):
        if self.show_password.isChecked():
            self.password_value.setEchoMode(False)
        else :
            self.password_value.setEchoMode(QLineEdit.Password)
    
    def default_config(self):
        if self.no_config.isChecked() :
            try :
                os.remove("custom_config")
            except :
                pass
            self.config_from_file()
            self.disable_enable_config(True) 
            self.tab_1.send_button.setDisabled(False)
        else :
            try :
                self.config_from_file("custom_config")
                self.disable_enable_config(False)
            except :
                self.clear_all()
                self.disable_enable_config(False)
                self.tab_1.send_button.setDisabled(True)
    
    def save_custom_config (self):
        config = self.read_config() #read from Entry fields
        
        #validate entry 
        if not config["smtp"] or not config["port"] or not config["account"] or not config["password"] or not config["subject"]:
            return QMessageBox.about(self,"Field Error" , "some field still empty")
        if "@" not in config["account"] or "." not in config["account"]:
            return QMessageBox.about(self,"Account Error", "Account shold be full Email form\nEx : name@domain.com") 
        
        text = config["smtp"]+":"+str(config["port"])+":"+config["account"]+":"+config["password"]+":"+config["subject"]
        with open ("custom_config","w") as f : #saving configuration to file with name custom_config
            f.write(text)
            QMessageBox.about(self,"Configuration Saved","DONE : Config saved")
        self.tab_1.send_button.setDisabled(False)
    
    def import_config(self):
        options = QFileDialog().options()
        options |=QFileDialog.DontUseNativeDialog
        file_name , type_ = QFileDialog.getOpenFileName(self,"Import Configuration" , "" , "All Files (*);;Text File (*.txt)" , options=options) 
        if file_name : 
            shutil.copyfile(file_name , os.getcwd()+"/custom_config")
            self.config_from_file("custom_config")
            QMessageBox.about(self,"Configuration Saved","DONE : Config saved")

            
    def export_config(self):
        self.save_custom_config()
        options = QFileDialog().options()
        options |= QFileDialog.DontUseNativeDialog
        file_name , type_ = QFileDialog.getSaveFileName(self,"Export Configuration" , "get_ip_config.txt","Text Files (*.txt)",options=options)
        if file_name :
            shutil.copyfile(os.getcwd() + "/custom_config" , file_name)
         

    
## Tab about ##        
class tab_about (QWidget):
    "(parent : QWidget)"
    def __init__(self,parent):
        super().__init__(parent)
        x= QLabel(self)
        x.setGeometry(0,0,432,310)
        x.setPixmap(QPixmap("about_picture.png"))
        self.show()

## Tab Source Code ##
class tab_source_code (QWidget):
    "(parent : QWidget)"
    def __init__(self,parent):
        super().__init__(parent)
        self.res = QTextBrowser(self)
        self.res.setGeometry(10,10,400,290)
        try :
            with open ("get_ip.py","r") as f :
                self.res.setText(f.read())
        except :
            self.res.setText("ERROR : Can't Read Source File")
        self.show()


##############
## Back End ##        
##############
#thread geting ip 
class get_ip(threading.Thread):
    def __init__(self):
        super().__init__()
        
    def run (self):
        ex.setDisabled(True)
        ex.tab_1.stat.setText("Getting IP . . .")
        result = ip().get_ip()
        if result[0] :
            ex.tab_1.res.setText(result[1])
            ex.tab_1.stat.setText("Done")
            print (result)
        elif not result[0]:
            ex.tab_1.stat.setText(result[1])
            print (result)
        ex.setDisabled(False)


#Thread send Email
class send_email (threading.Thread) :
    def __init__(self , send_to):
        super().__init__()
        self.send_to = send_to
    
    def run (self) :
        ex.setDisabled(True)
        ex.tab_1.stat.setText("SENDING . . .")
        config = ex.tab_2.read_config()
        send_email = ip().send_ip(config["smtp"],config["port"],config["account"],config["password"],config["subject"],self.send_to)
        if send_email == "sent" :
            ex.tab_1.res.setText(ip().get_ip())
            ex.tab_1.stat.setText("IP Sent")
            print (send_email)
            ex.setDisabled(False)
        else : 
            ex.setDisabled(False)
            ex.tab_1.stat.setText("Failed to Send\nCheck configuration")

#get/send ip class
class ip  :
    def get_ip (self) :
        try :
            stat = True
            message = "IP Address : " + requests.get("https://api.ipify.org").text
            return (stat , message)
        except :
            stat = False
            message = "Field to use API\nCheck Connection"
            return (stat , message)

    def send_ip(self , smtp_server , port , account , password , subject ,send_to):
        msg = self.get_ip()
        try :
            with smtplib.SMTP(smtp_server , port ) as conn :
                conn.ehlo()
                conn.starttls() #encrypt connection 
                conn.ehlo()
                conn.login(account , password)
                conn.sendmail(account , send_to ,"subject:{}\n\n".format(subject) + msg)
                return "sent"
        except Exception as mail_error:
            return "Faild to send Email\nCode : " + str(mail_error)


#run app from here
if __name__ == "__main__":
    APP = QApplication(sys.argv)
    ex = app() 
    sys.exit(APP.exec_())