#!/usr/bin/python3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import os

def send_email(file, changeset, name, emailID, report, build_number):
	msg = MIMEMultipart()

	#email_id_to = 'vigneswaran@uhnder.com'
	email_id_to = ['vigneswaran@uhnder.com', 'somnath@uhnder.com']
	msg['From'] = 'jenkins@uhnder.com'
	msg['To'] = 'vigneswaran@uhnder.com'
	msg['Subject'] = "Jenkins regression suites repo update: " + str(changeset)[:12] 
	#email_id_cc = ['srikanth@uhnder.com','jaya@uhnder.com', 'ramprasath@uhnder.com', 'vigneswaran@uhnder.com', 'somnath@uhnder.com']
	message = 'Hi All,<br><br>&nbsp;&nbsp;&nbsp;&nbsp;PFA for Jenkins regression suites Test plan file <b>'\
					+str(file)+' </b>,with build number <b>' +str(build_number)+ '</b>. The <b> SRS changeset is '\
					+ str(changeset)[:12] +'</b>. <br> The total number of jobs files failed is  '+ str(len(report))+'</br> <br> Name of the committer <b>'\
					+ str(name)+'</b></br> <br> Email ID of the committer '+ str(emailID)+'</br><br> List of files not having valid header </br>'
	for eachfile in report:
		message += ('<br>' + str(eachfile)+'</br>')
	message += ('<br>Link to is @ <a href=" https://bitbucket.org/uhnder/jenkins-regression-tests">Jenkins-regression-tests</a></br> <br><br>Thanks & Regards, <br> <b>Jenkins</b>')

	msg.attach(MIMEText(message,'html'))

	with open('Testplan.xls', 'rb') as fp:
	    part = MIMEApplication(fp.read(), Name=os.path.basename(file))
	part['Content-Disposition'] = 'attachment; filename="%s"' %(os.path.basename(file))
	msg.attach(part)

	server = smtplib.SMTP('smtp.office365.com',587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('jenkins@uhnder.com', 'yclgghwkbkhmdxyb')
	text = msg.as_string()
	server.sendmail('jenkins@uhnder.com', email_id_to, text)
	server.quit()
	
	print ('Email sent')