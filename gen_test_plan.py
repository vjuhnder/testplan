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

def main():
	parser = argparse.ArgumentParser()
#	parser.add_argument('--createplan', action='store_true', help='Create test plan')
	# parser.add_argument('--test5', action='store_true', help='Test5')
	# parser.add_argument('--test4', action='store_true', help='Get baseline ID')
	# parser.add_argument('--test3', action='store_true', help='Test jrt repo cloning')
	# parser.add_argument('--test2', action='store_true', help='Check a changeset for valid job file tempate')
	# parser.add_argument('--test1', action='store_true', help='To get job files and job files with path')
	parser.add_argument('--test', default=None, type=int, help='To get job files and job files with path')
	parser.add_argument('--cps', action='store_true', help='Create test plans')
	parser.add_argument('--print', action='store_true', help='Enable debug print')
	parser.add_argument('--folder', default = '~/', type=str , help = 'job files folder' )
	parser.add_argument('--out', default = '~/', type=str , help = 'Output path' )
	parser.add_argument('--pid', default=None, type=int, help='To get job files and job files with path')
	args = parser.parse_args()

	jj.setWorkbookPath(args.out)
	jj.setWorkspacePath(args.folder+'regression-suites/')
	jj.setRepoPath(args.folder)

	if args.print:
		jj.enableprint()

	if args.cps:
		jj.createTestPlanWorkbook()

	if args.test == 1 :
		changeset_id = 'd5bc72f6a4f9'
		author, emailID, jobfiles = jj.parse_repository(changeset_id)
		file_report = jj.parse_job_files(jobfiles)
		jj.send_email(changeset_id, author, emailID, file_report)		
	elif args.test == 2:
		utils_jrt().logAllJobFileNames(jj.getWorkspacePath(), 'jobfiles-list.txt')
		utils_jrt().logAllFileNamesAndPath(jj.getWorkspacePath(), 'jobfilesWPath-list.txt')
	elif args.test == 3:
		jrt_repo.clone_jrt_repo()
	elif args.test == 4:
		jrt_repo.set_baselineID()
		print(jrt_repo.get_baselineID())
	elif args.test == 5:
		p = subprocess.Popen(["sh", ""], stdout = subprocess.PIPE, shell = True, preexec_fn = os.setsid)
		print(str(p.pid))
		print(str(os.getpgid(p.pid)))
		os.environ['KEY_PID'] = str(os.getpgid(p.pid))
		print(os.environ['KEY_PID'])
	elif args.test == 6:
		os.killpg(int(os.environ.get('KEY_PID')), signal.SIGTERM)
	elif args.test == 7:
		#Read baseline ID
		changeset_id = jrt_repo.get_baselineID()
		if changeset_id != -1 :
			jrt_repo.clone_jrt_repo()
			#get recent ID
			tip_id = jrt_repo.get_tipID()
			print('tip ID : ', tip_id)
			id_list = jj.parse_repo_change_log(changeset_id, tip_id)
			for eachID in id_list:
				if len(eachID) > 0 :
					author, emailID, jobfiles = jj.parse_repository(eachID)
					file_report = jj.parse_job_files(jobfiles)
					if len(file_report) > 0 :
						em.send_email('Testplan.xls', eachID, author, emailID, file_report)
			#set recent id as baseline id
			jrt_repo.set_baselineID()

		else:
			print('Error: baseline ID is missing!!!')
			jrt_repo.set_baselineID()
		
	elif args.test == 8:
		emailID = 'vigneswaran@uhnder.com'
		author = 'vigneswaran'
		eachID = '123456'
		filereport = ['testjob1.job', 'testjob2.job']
		em.send_email('Testplan.xls', eachID, author, emailID, filereport)

if __name__ == "__main__":
	main()