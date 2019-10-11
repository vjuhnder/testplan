#!/usr/bin/python3
import sys, os, subprocess

#Get files added of a revision
def get_regression_suite_files(file_list):
	regression_test_files = []
	for eachfile in file_list:
		if str(eachfile).find('egression-suites', 0) == True:
			# print(eachfile)
			regression_test_files.append(eachfile)
	return regression_test_files

def clone_jrt_repo():
	# Checks if the repo is already cloned else clone
	if os.path.isdir('jenkins-regression-tests'):
	    with ChDir('jenkins-regression-tests'):
	        cmd = ' hg pull --quiet && hg up -C --quiet'
	        ret_st = os.system(cmd)
	        if ret_st:
	            print("Error: Cannot pull/update repo")
	            sys.exit(-1)
	else:
	    cmd = 'hg clone https://bitbucket.org/uhnder/jenkins-regression-tests' + ' --quiet'
	    ret_st = os.system(cmd)
	    if ret_st:
	        print("Error: Cannot clone repo(%s) into %s" %(args.repo_name, os.path.abspath(workspace+'/'+test_folder_name)))
	        sys.exit(-1)	
# if __name__ == "__main__":
# 	get_regression_suite_files()

