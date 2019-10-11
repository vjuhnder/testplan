#!/usr/bin/python3
import os
import filecmp
import argparse
from testplan.mod_test_plan import jenkinsJobs, utils_jrt
from repo import jrt_repo

#python3 ./gen_test_plan.py --cps --out '/home/jenkins/.jenkins/testplan_workspace/' --folder '/home/jenkins/.jenkins/testplan_workspace/jenkins-regression-tests/'

#get newly added files
#validate it as per format
#generate email if it fails to the committer and QA
#Generate test plan excel

jj = jenkinsJobs()

def main():
	parser = argparse.ArgumentParser()
#	parser.add_argument('--createplan', action='store_true', help='Create test plan')
	parser.add_argument('--test3', action='store_true', help='Test jrt repo cloning')
	parser.add_argument('--test2', action='store_true', help='Check a changeset for valid job file tempate')
	parser.add_argument('--test1', action='store_true', help='To get job files and job files with path')
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

	if args.test2:
		changeset_id = 'd5bc72f6a4f9'
		author, emailID, jobfiles = jj.parse_repository(changeset_id)
		file_report = jj.parse_job_files(jobfiles)
		jj.send_email(changeset_id, author, emailID, file_report)
		
	if args.test1:
		utils_jrt().logAllJobFileNames(jj.getWorkspacePath(), 'jobfiles-list.txt')
		utils_jrt().logAllFileNamesAndPath(jj.getWorkspacePath(), 'jobfilesWPath-list.txt')

	if args.test3:
		jrt_repo.clone_jrt_repo()

	if not(args.test2) and not(args.cps) and not(args.test1) and not(args.test2) and not(args.test3):
		print('Use --help to get more info')


if __name__ == "__main__":
	main()