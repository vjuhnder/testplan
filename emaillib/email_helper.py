#!/usr/bin/python3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib
import email_to

def send_email(file, changeset, name, emailID, report):
	msg = MIMEMultipart()
	# msg['From'] = 'jenkins@uhnder.com'
	# msg['To'] = 'vigneswaran@uhnder.com'
	# msg['Subject'] = "Jenkins regression suites repo update: " 
	#email_id_cc = ['srikanth@uhnder.com','jaya@uhnder.com', 'ramprasath@uhnder.com', 'vigneswaran@uhnder.com', 'somnath@uhnder.com']
	build_number = 'To be added'
	# message = 'Hi All,<br><br>&nbsp;&nbsp;&nbsp;&nbsp;PFA of the output.html for jenkins regression suites Test plan<b>'\
	# 				+str(testplan)+' </b>,with build number </b>' +str(build_number)+ '</b>. The <b> SRS changeset is '\
	# 				+ str(changeset)+'</b>. <br> The total number of jobs is '+ str(len(report))+'</br><br> No of jobs failed is '\
	# 				+ str(name)+'</br><br> No of jobs with WIP is '+ str(emailID)+'</br><br> No of jobs passed is '\
	# 				+ str(report)+'</br><br>The URL is @ <a href=" https://bitbucket.org/uhnder/jenkins-regression-tests/">\
	# 				 Bitbucket URL </a></br><br><br>Thanks & Regards, <br> <b>Jenkins</b>'
	# msg.attach(MIMEText(message,'html'))
	# with open(file, 'rb') as fp:
	#     part = MIMEApplication(fp.read(), Name=os.path.basename(file))
	# part['Content-Disposition'] = 'attachment; filename="%s"' %(os.path.basename(file))
	# msg.attach(part)
	# server = smtplib.SMTP('smtp.office365.com',587)
	# server.ehlo()
	# server.starttls()
	# server.ehlo()
	# server.login('jenkins@uhnder.com', 'yclgghwkbkhmdxyb')
	# text = msg.as_string()
	# server.sendmail('jenkins@uhnder.com',email_id_to,text)
	# server.quit()
	subject = "Jenkins regression suites repo update: " 



	message = email_to.Message('Hi All,<br><br>&nbsp;&nbsp;&nbsp;&nbsp;')
	message.add('PFA for Jenkins regression suites Test plan file <b>')
	message.add(str(file)+' </b>,with build number </b>' +str(build_number)+ '</b>. The <b> SRS changeset is ')
	message.add(str(changeset)+'</b>. <br> The total number of jobs files failed is '+ str(len(report))+'</br><br> Name of the committer ')
	message.add(str(name)+'</br><br> Email ID of the committer '+ str(emailID)+'</br><br> List of files not having valid header</br><br>')
	for eachfile in report:
		message.add('<br>' + str(eachfile)+'</br>')
	message.add('</br><br>The URL is @ <a href=" https://bitbucket.org/uhnder/jenkins-regression-tests/">Bitbucket URL </a></br><br><br>Thanks & Regards, <br> <b>Jenkins</b>')

	server = email_to.EmailServer('smtp.office365.com',587, 'jenkins@uhnder.com', 'yclgghwkbkhmdxyb' )
	server.send_message(message, 'vigneswaran@uhnder.com', subject )

	print ('Email sent')