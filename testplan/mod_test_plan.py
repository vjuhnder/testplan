#!/usr/bin/python3
import glob
import xlwt
import os
from xlwt import Workbook
import datetime
from repo import repo_lib, jrt_repo

HEADER_STRING = 	"#TEST_DESCR_START\n\
#NAME_single_ln()\n\
#VERSION_single_ln()\n\
#MODULE_NAME_single_ln()\n\
#PLATFORM_single_ln()\n\
#SUMMARY_single_ln()\n\
#DESCRIPTION_multi_ln()\n\
#PASS-CRITERIA_single_ln(Pass: )\n\
#TEST_DESCR_END"

# WORKSPACE = '/mnt/c/code/jenkins-regression-tests/regression-suites/'
# WORKBOOKPATH = '/mnt/c/code/jrt-testplan/'
TESTPLAN_FILENAME = 'Testplan.xls'

jobStr = ['NAME', 'VERSION', 'MODULE_NAME', 'PLATFORM', 'SUMMARY', 'DESCRIPTION', 'PASS-CRITERIA', 'wner']
excelColumn = ['S.No', 'Module Name', 'Test Name',  'Test Summary', 'Owner', 'Description', 'Platform', 'Version', 'Pass-Criteria']

colNameStr = []
colSummStr = []
colCritStr = []
colVerStr = []
colSubDir = []

class jenkinsJobs():
	def __init__(self):
		self.enable_print = False

		self.name_str = ""
		self.ver_str = ""
		self.mod_str = ""
		self.plat_str = ""
		self.summ_str = ""
		self.desc_str = ""
		self.pf_str = ""
		self.own_str = ""

		self.workspace_path = ""
		self.workbook_path = ""
		self.repo_path = ""


	def clearProperties(self):
		self.name_str = ""
		self.ver_str = ""
		self.mod_str = ""
		self.plat_str = ""
		self.summ_str = ""
		self.desc_str = ""
		self.pf_str = ""
		self.own_str = ""

	def setWorkspacePath(self, path):
		self.workspace_path = path

	def getWorkspacePath(self):
		return self.workspace_path

	def setRepoPath(self, path):
		self.repo_path = path

	def getRepoPath(self):
		return self.repo_path

	def setWorkbookPath(self, path):
		self.workbook_path = path

	def getWorkbookPath(self):
		return self.workbook_path

	def enableprint(self):
		self.enable_print = True

	def getJobFiles(self, path):
		return glob.glob(path + "**/*.job", recursive=True)

	def getJobFileNames(self, path):
		jobfiles = []
		for eachval in os.listdir(path):
			dir1 = os.path.join(path,eachval)
			#dir1 = eachval			
			if os.path.isdir(dir1) == False:
				#Level1 job files added
				dir1.replace(self.workspace_path, '')
				if self.enable_print:
					print("Dir...path...",dir1)
				jobfiles.append(dir1)
				#jobfiles.append(eachval)
			else:
				if self.enable_print:
					print('subdir ', eachval)
				for subDirFiles in (os.listdir(dir1)):
					dir2 = os.path.join(dir1,subDirFiles)
					if os.path.isdir(dir2) == False:						
						#Level2 job files added
						dir2.replace(self.workspace_path, '')
						if self.enable_print:
							print("Dir2...", dir2)
						jobfiles.append(dir2)
						#jobfiles.append(eachval + '/' + subDirFiles)
					else:
						if self.enable_print:
							print('subdir2 ', subDirFiles)
						for subDir2Files in (os.listdir(dir2)):
							dir3 = os.path.join(dir2,subDir2Files)
							#Level3 job files added
							dir3.replace(self.workspace_path, '')
							if self.enable_print:
								print("Dir3...", dir3)
							jobfiles.append(dir3)
							#jobfiles.append(eachval + '/' + subDirFiles+ '/' + subDir2Files)
		return jobfiles

	def extractValue(self, strval):
		return strval[strval.find("(")+1:strval.find(")")]

	def getIDExcelColumn(self, columnName):
		foundVal = 0
		for i, eachColumn in enumerate(excelColumn):
			if eachColumn == columnName:
				foundVal = 1
				return i

		if foundVal == 0:
			print("!!!ERROR!!! Invalid Excel Column name ", columnName)
			return 0

	def parseEachJobFile(self, jobfile):
			fp = open(jobfile, 'r')
			#print(jobfile)
			for eachline in fp:
				for i, eachID in enumerate(jobStr):
					if eachline.find(eachID) == True:
						extractField = self.extractValue(eachline)
						if eachID == jobStr[0]:
							self.name_str = extractField
						elif eachID == jobStr[1]:
							self.ver_str = extractField
						elif eachID == jobStr[3]:
							self.plat_str = extractField
						elif eachID == jobStr[4]:
							self.summ_str = extractField
						elif eachID == jobStr[6]:
							self.pf_str = extractField
						elif eachID == jobStr[7]:
							self.own_str = extractField
	#This function will check the job file for valid header
	def checkJobFile(self, jobfile):
		try:
			fp = open(jobfile, 'r')
			validCount = 0
			for eachline in fp:
				for i, eachID in enumerate(jobStr):
					if eachline.find(eachID) == True:
						if eachID == jobStr[0]:
							validCount = validCount + 1
						elif eachID == jobStr[1]:
							validCount = validCount + 1
						elif eachID == jobStr[2]:
							validCount = validCount + 1
						elif eachID == jobStr[3]:
							validCount = validCount + 1
						elif eachID == jobStr[4]:
							validCount = validCount + 1
						elif eachID == jobStr[5]:
							validCount = validCount + 1
						elif eachID == jobStr[6]:
							validCount = validCount + 1
			return validCount
		except:
			print("Unable to open the file")
			return -1

	def createTestPlanSheet(self, folderName, workbook):
		sheetName = folderName
		#excel can accept sheet name upto 30 characters
		if len(sheetName) > 30:
			sheetName = sheetName[:29]

		excelSheet = workbook.add_sheet(sheetName)
		jobFiles = self.getJobFileNames(self.workspace_path + folderName)

		if len(jobFiles) == 0:
			print("No job files in dir ", folderName)

		headStyle = xlwt.easyxf('font: bold 1')
		for i, eachColumn in enumerate(excelColumn):
			excelSheet.write(0, i, eachColumn, headStyle)

		for r, eachjob in enumerate(jobFiles):
			rowIndex = r+1		
			#get the properties from job files ,  
			self.clearProperties()
			self.parseEachJobFile(eachjob)
			## Write excel sheet
			excelSheet.write(rowIndex, self.getIDExcelColumn('S.No'), rowIndex)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Module Name'), eachjob.replace((self.workspace_path + folderName + '/'), ''))
			excelSheet.write(rowIndex, self.getIDExcelColumn('Test Name'), self.name_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Test Summary'), self.summ_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Pass-Criteria'), self.pf_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Version'), self.ver_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Platform'), self.plat_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Owner'), self.own_str)

	def createTestPlanWorkbook(self):
		#create and populate test plan
		print("Folder to process ", self.workspace_path)

		workb = Workbook()
		#parse job folder
		for eachdir in (os.listdir(self.workspace_path)):
			if os.path.isdir(os.path.join(self.workspace_path,eachdir)) == True:
				if self.enable_print:
					print("Dir...", eachdir)
				
				self.createTestPlanSheet(eachdir, workb)

		try:
			workb.save(self.workbook_path + TESTPLAN_FILENAME)
			print("File saved as ", self.workbook_path + TESTPLAN_FILENAME)
		except:
			print("Unable to save the excel file ", self.workbook_path + TESTPLAN_FILENAME)
			fname,fext = os.path.splitext(TESTPLAN_FILENAME)
			renameFile = fname+str(datetime.datetime.now())+fext
			workb.save(self.workbook_path + renameFile)
			print("File saved as ", self.workbook_path + renameFile)

	def send_email(self, changeset, name, emailID, report):

		if len(report) > 0 :
			print("---- Email ----")
			print('Email ID : ', emailID)
			print('Name : ', name)
			print('File list : ')
			for eachItem in report:
				print(eachItem)
		else:
			print(changeset, " is fine")

	def parse_job_files(self, regression_files):

		file_notOk_report = []
		file_ok_report = []
		file_err_report = []
		for eachfile in regression_files:
			# print(self.repo_path+eachfile)
			validity = self.checkJobFile(self.repo_path+eachfile)
			if validity == 7 :
				# print(self.repo_path + eachfile + " - File Valid ")
				file_ok_report.append(self.repo_path + eachfile + " - File Valid ")
			elif validity == -1:
				# print(self.repo_path + eachfile + " - File not found/error ")
				file_err_report.append(self.repo_path + eachfile + " - File not found/error ")
			else:
				# print(self.repo_path + eachfile + " - File Invalid ")
				file_notOk_report.append(self.repo_path + eachfile + " - File Invalid ")

		return file_notOk_report

	def parse_repository(self, changeset):

		files_changed, committer, emailID = repo_lib.get_repo_log(self.repo_path, changeset)
		# for eachfile in files_changed:
		# 	print(eachfile)
		# print(committer, ' ', emailID)
		reg_files = jrt_repo.get_regression_suite_files(files_changed)
		# for eachfile in reg_files:
		# 	print(eachfile)
		return committer, emailID, reg_files


	def parse_repo_change_log(self, baseChangeset, recentChangeset):

		id_list = repo_lib.get_changeset_list(self.repo_path, baseChangeset, recentChangeset)

		# print(id_list)
		# for eachID in id_list:
		# 	if len(eachID) > 0 :
		# 		print(eachID)
		# 		files_changed, committer, emailID = repo_lib.get_repo_log(self.repo_path, eachID)
		# 		print(committer, ' ', emailID)
		# 		reg_files = jrt_repo.get_regression_suite_files(files_changed)
		# 		print(reg_files)

		# print(committer, ' ', emailID)
		# reg_files = jrt_repo.get_regression_suite_files(files_changed)
		# return committer, emailID, reg_files
		return id_list

class utils_jrt():
	def getAllFileNames(self, path):
		listfilename = []
		for dirpaths, dirnames, filenames in os.walk(path):
			for filename in filenames:
			 	listfilename.append(filename)
		return listfilename

	def logAllJobFileNames(self, path, logfilename):
		listfilename = []
		if os.path.exists(logfilename):
			os.remove(logfilename)
		logfile = open(logfilename, 'a')

		for dirpaths, dirnames, filenames in os.walk(path):
			for filename in filenames:
				# print(filename)
				fname,fext = os.path.splitext(filename)
				if fext == '.job':
					listfilename.append(filename)
					logfile.write(filename + '\n')
				else:
					print('Unknown job file type', filename)

		logfile.close()
		return listfilename

	def logAllFileNamesAndPath(self, path, logfilename):
		listFileNamePath = []
		if os.path.exists(logfilename):
			os.remove(logfilename)
		logfile = open(logfilename, 'a')

		for dirpaths, dirnames, filenames in os.walk(path):
				for filename in filenames:		  	
					fname,fext = os.path.splitext(filename)
					if fext == '.job':
						strfileAndpath = os.path.join(dirpaths,filename)
						logfile.write(strfileAndpath + '\n')
						#print(strfileAndpath)
						listFileNamePath.append(strfileAndpath)
					elif filename == '.empty':
						strfileAndpath = os.path.join(dirpaths,filename)
						logfile.write(strfileAndpath + '\n')
						# print('Unknown job file ', filename)
					else:
						print('Unknown file type', filename)

		logfile.close()

		return listFileNamePath

