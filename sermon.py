#!/bin/python

import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import logging
import sys

# Logging configuration 
logging.basicConfig(filename='/var/log/server_monitor.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_email(subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = "<sender-email>"
        msg["To"] = "<receiver-email>"
        msg["Subject"] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # SMTP server setup
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("<sender-email>", "<password>")
        
        # Email sending 
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()
        
        logging.info("Email sent successfully to %s", msg["To"])
    except Exception as e:
        logging.error("Failed to send email: %s", str(e))

def collect_system_info():
    try:
        logging.info("Collecting SYSTEM info")
        system_info = subprocess.check_output(["uname", "-a"]).decode()
        return system_info
    except Exception as e:
        logging.error("Error collecting system info: %s", str(e))
        return ""

def collect_time_info():
    try:
        logging.info("Collecting current time info")
        time_info = subprocess.check_output(["date"]).decode()
        return time_info
    except Exception as e:
        logging.error("Error collecting time info: %s", str(e))
        return ""

def collect_disk_info():
    try:
        logging.info("Collecting DISK info")
        disk_info = subprocess.check_output(["df", "-h"]).decode()
        return disk_info
    except Exception as e:
        logging.error("Error collecting disk info: %s", str(e))
        return ""

def collect_network_info():
    try:
        logging.info("Collecting NETWORK info")
        network_info = subprocess.check_output(["netstat", "-r"]).decode()
        return network_info
    except Exception as e:
        logging.error("Error collecting network info: %s", str(e))
        return ""

def collect_vm_info():
    try:
        logging.info("Collecting VM info")
        vm_info = subprocess.check_output(["vmstat", "1", "3"]).decode()
        return vm_info
    except Exception as e:
        logging.error("Error collecting VM info: %s", str(e))
        return ""

def collect_all_info():
    # Collect all the information
    system_info = collect_system_info()
    time_info = collect_time_info()
    disk_info = collect_disk_info()
    network_info = collect_network_info()
    vm_info = collect_vm_info()
    
    # Compile into a single report
    report = (
        f"System Info:\n{system_info}\n"
        f"Current Time:\n{time_info}\n"
        f"Disk Info:\n{disk_info}\n"
        f"Network Info:\n{network_info}\n"
        f"VM Info:\n{vm_info}\n"
    )
    
    return report

def main():
    try:
        logging.info("Server monitoring script started")
        
        # System information collection and report preparation 
        report = collect_all_info()
        
        # Send the report via email
        send_email("Server Monitoring Report", report)

        logging.info("Server monitoring script finished successfully")
    except Exception as e:
        logging.error("An error occurred in the main function: %s", str(e))
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
