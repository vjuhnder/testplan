#!/usr/bin/python3
import os
import filecmp
import argparse
from testplan import mod_test_plan
from testplan.mod_test_plan import jenkinsJobs

mp = mod_test_plan

#get newly added files
#validate it as per format
#generate email if it fails to the committer and QA
#Generate test plan excel
# REPO_PATH = '/mnt/c/code/jenkins-regression-tests/'

# repo_path = '/mnt/c/code/jenkins-regression-tests/'

jj = jenkinsJobs()

def main():
	parser = argparse.ArgumentParser()
#	parser.add_argument('--createplan', action='store_true', help='Create test plan')
	parser.add_argument('--s1', action='store_true', help='Test ground')
	parser.add_argument('--cps', action='store_true', help='Create test plans')
	parser.add_argument('--print', action='store_true', help='Enable debug print')
	parser.add_argument('--folder', default = '~/', type=str , help = 'job files folder' )
	parser.add_argument('--out', default = '~/', type=str , help = 'Output path' )
	args = parser.parse_args()

	jj.setWorkbookPath(args.out)
	jj.setWorkspacePath(args.folder+'regression-suites/')
	jj.setRepoPath(args.folder)

	if args.print:
		jj.enableprint()

	if args.cps:
		jj.createTestPlanWorkbook()

	if args.s1:
		changeset_id = 'd5bc72f6a4f9'
		author, emailID, jobfiles = jj.parse_repository(changeset_id)
		file_report = jj.parse_job_files(jobfiles)
		jj.send_email(changeset_id, author, emailID, file_report)
		

	if not(args.s1) and not(args.cps):
		print('Use --help to get more info')


if __name__ == "__main__":
	main()