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

# if __name__ == "__main__":
# 	get_regression_suite_files()

