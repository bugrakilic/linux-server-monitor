#!/bin/python

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys
import subprocess

# definition. 
def main():
    try:
        def mail_func():
            msg = MIMEText("Recent server monitoring statistics.")
            msg["Subject"] = ""
            msg["From"] = ""
            msg["To"] = ""
            
            server = smtplib.SMTP("smtp.gmail.com",587)
            server.ehlo()
            server.starttls()
            server.login("", "")
        
            server.sendmail(msg["From"],msg["To"],msg.as_string())
            print("Mail sent successfully.")
        
        def sys_fun():
            print ("\n>>> Collecting SYSTEM info: \n") 
            subprocess.call(["uname", "-a"])

        def time_fun():
            print ("\nCurrent time: ")
            subprocess.call(["date"]) 
            
        def disc_fun():
            print ("\n>>> Collecting DISC info: \n")
            subprocess.call(["df", "-h"])

        def net_fun():
            print ("\n>>> Collecting NETWORK info: \n")
            subprocess.call(["netstat", "-r"])

        def vm_fun():
            print ("\n>>> Collecting VM  info: \n")
            subprocess.call(["vmstat", "1", "3"])
        
        ''' def io_fun():
            print ("\n>>> Collecting IO info: \n") 
            subprocess.call(["iostat", "1", "3"]) '''

        def serv_func(): 
            sys_fun()
            time_fun()
            disc_fun()
            net_fun()
            vm_fun()
            mail_func()
        
        serv_func()

    # In case of an error occurs. 
    except:
        print("Error Found:", sys.exc_info()[0])

main()