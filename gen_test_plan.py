#!/usr/bin/python3
import os
import filecmp
import argparse
from testplan import mod_test_plan
from testplan.mod_test_plan import jenkinsJobs
from repo import repo_lib, jrt_repo
mp = mod_test_plan

#get newly added files
#validate it as per format
#generate email if it fails to the committer and QA
#Generate test plan excel
REPO_PATH = '/mnt/c/code/jenkins-regression-tests/'

jj = jenkinsJobs()

def parse_repository(changeset):

	files_changed, committer, emailID = repo_lib.get_repo_log(REPO_PATH, changeset)
	# for eachfile in files_changed:
	# 	print(eachfile)
	print(committer, ' ', emailID)
	reg_files = jrt_repo.get_regression_suite_files(files_changed)
	return committer, emailID, reg_files

def parse_job_files(regression_files):

	file_notOk_report = []
	file_ok_report = []
	file_err_report = []
	for eachfile in regression_files:
		validity = jj.checkJobFile(REPO_PATH+eachfile)
		if validity == 7 :
			# print(REPO_PATH + eachfile + " - File Valid ")
			file_ok_report.append(REPO_PATH + eachfile + " - File Valid ")
		elif validity == -1:
			# print(REPO_PATH + eachfile + " - File not found/error ")
			file_err_report.append(REPO_PATH + eachfile + " - File not found/error ")
		else:
			# print(REPO_PATH + eachfile + " - File Invalid ")
			file_notOk_report.append(REPO_PATH + eachfile + " - File Invalid ")

	return file_notOk_report

def send_email(changeset, name, emailID, report):

	if len(report) > 0 :
		print("---- Email ----")
		print(name, emailID)
		for eachItem in report:
			print(eachItem)
	else:
		print(changeset, " is fine")

def main():
	parser = argparse.ArgumentParser()
#	parser.add_argument('--createplan', action='store_true', help='Create test plan')
	parser.add_argument('--s1', action='store_true', help='Test ground')
	parser.add_argument('--cps', action='store_true', help='Create test plans')
	parser.add_argument('--print', action='store_true', help='Enable debug print')
	args = parser.parse_args()

	if args.print:
		jj.enableprint()

	if args.cps:
		jj.createTestPlanWorkbook()

	if args.s1:
		changeset_id = 'd5bc72f6a4f9'
		author, emailID, jobfiles = parse_repository(changeset_id)
		file_report = parse_job_files(jobfiles)
		send_email(changeset_id, author, emailID, file_report)
		# print(str(jj.checkJobFile('/mnt/c/code/jenkins-regression-tests/regression-suites/carle-linux-x86-scans/test_beamforming_cal_1D.job')))
		# print(str(jj.checkJobFile('/mnt/c/code/jenkins-regression-tests/regression-suites/carle-linux-x86-scans/test_beamforming_cal_2D.job')))

	if not(args.s1) and not(args.cps):
		print('Use --help to get more info')


if __name__ == "__main__":
	main()