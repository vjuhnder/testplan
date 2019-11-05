#!/usr/bin/python3
import os
import filecmp
import argparse
from testplan.mod_test_plan import jenkinsJobs, utils_jrt
from repo import jrt_repo
import subprocess
import signal
from emaillib import email_helper as em
#python3 ./gen_test_plan.py --cps --out '/home/jenkins/.jenkins/testplan_workspace/' --folder '/home/jenkins/.jenkins/testplan_workspace/jenkins-regression-tests/'

#get newly added files
#validate it as per format
#generate email if it fails to the committer and QA
#Generate test plan excel

jj = jenkinsJobs()

def jrt_repo_email(testplan_fname):
	#Read baseline ID
	changeset_id = jrt_repo.get_baselineID()
	if changeset_id != -1 :
		jrt_repo.clone_jrt_repo()
		#get recent ID
		tip_id = jrt_repo.get_tipID()
		print('tip ID : ', tip_id)
		if tip_id != changeset_id:
			id_list = jj.parse_repo_change_log(changeset_id, tip_id)
			for eachID in id_list:
				if len(eachID) > 0 :
					updateRepo(eachID)
					author, emailID, jobfiles, build_num = jj.parse_repository(eachID)
					file_report = jj.parse_job_files(jobfiles)
					if len(file_report) > 0 :
						em.send_email(testplan_fname, eachID, author, emailID, file_report, build_num)

			#set recent id as baseline id
			jrt_repo.set_baselineID()
		else:
			print("Baseline and tip changeset are same")
		
	else:
		print('Error: baseline ID is missing!!!')
		jrt_repo.set_baselineID()

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('--test', default=None, type=int, help='To get job files and job files with path')
	parser.add_argument('--cps', action='store_true', help='Create test plans')
	parser.add_argument('--run', action='store_true', help='Create test plans and send email for each changeset')
	parser.add_argument('--print', action='store_true', help='Enable debug print')
	parser.add_argument('--folder', default = '~/', type=str , help = 'job files folder' )
	parser.add_argument('--out', default = '~/', type=str , help = 'Output path' )
	parser.add_argument('--pid', default=None, type=int, help='To get job files and job files with path')
	args = parser.parse_args()

	jj.setWorkbookPath(args.out)
	jj.setWorkspacePath(args.folder+'regression-suites/')
	jj.setRepoPath(args.folder)

	testplan_fname = 'Testplan.xls'
	#option to enable debug print
	if args.print:
		jj.enableprint()

	if args.cps:
		testplan_fname = jj.createTestPlanWorkbook(testplan_fname)
		jrt_repo_email(testplan_fname)

	if args.run:
		testplan_fname = jj.createTestPlanWorkbook(testplan_fname)
	#Test cases to test the functional elements of the script
	#Test - a specified changeset for file add/modification and email generation
	if args.test == 1 :
		changeset_id = 'd5bc72f6a4f9'
		author, emailID, jobfiles, build_num = jj.parse_repository(changeset_id)
		file_report = jj.parse_job_files(jobfiles)
		jj.send_email(changeset_id, author, emailID, file_report, build_num)
	#Test - job files text report with and without path
	elif args.test == 2:
		utils_jrt().logAllJobFileNames(jj.getWorkspacePath(), 'jobfiles-list.txt')
		utils_jrt().logAllFileNamesAndPath(jj.getWorkspacePath(), 'jobfilesWPath-list.txt')
	#Test - jrt repository cloning
	elif args.test == 3:
		jrt_repo.clone_jrt_repo()
	#Test - Baselining repository version module
	elif args.test == 4:
		jrt_repo.set_baselineID()
		print(jrt_repo.get_baselineID())
	# elif args.test == 5:
	# 	p = subprocess.Popen(["sh", ""], stdout = subprocess.PIPE, shell = True, preexec_fn = os.setsid)
	# 	print(str(p.pid))
	# 	print(str(os.getpgid(p.pid)))
	# 	os.environ['KEY_PID'] = str(os.getpgid(p.pid))
	# 	print(os.environ['KEY_PID'])
	# elif args.test == 6:
	# 	os.killpg(int(os.environ.get('KEY_PID')), signal.SIGTERM)
	#Repository info and email generation - integration test
	elif args.test == 7:
		jrt_repo_email(testplan_fname)
		#Read baseline ID
		# changeset_id = jrt_repo.get_baselineID()
		# if changeset_id != -1 :
		# 	jrt_repo.clone_jrt_repo()
		# 	#get recent ID
		# 	tip_id = jrt_repo.get_tipID()
		# 	print('tip ID : ', tip_id)
		# 	if tip_id != changeset_id:
		# 		id_list = jj.parse_repo_change_log(changeset_id, tip_id)
		# 		for eachID in id_list:
		# 			if len(eachID) > 0 :
		# 				author, emailID, jobfiles, build_num = jj.parse_repository(eachID)
		# 				file_report = jj.parse_job_files(jobfiles)
		# 				if len(file_report) > 0 :
		# 					em.send_email(testplan_fname, eachID, author, emailID, file_report, build_num)

		# 		#set recent id as baseline id
		# 		jrt_repo.set_baselineID()
		# 	else:
		# 		print("Baseline and tip changeset are same")
			

		# else:
		# 	print('Error: baseline ID is missing!!!')
		# 	jrt_repo.set_baselineID()
	# Test email generation functionality	
	elif args.test == 8:
		emailID = 'vigneswaran@uhnder.com'
		author = 'vigneswaran'
		eachID = '123456'
		filereport = ['testjob1.job', 'testjob2.job']
		em.send_email('Testplan.xls', eachID, author, emailID, filereport)

if __name__ == "__main__":
	main()