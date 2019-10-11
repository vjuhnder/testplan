#!/usr/bin/python3
import glob
import xlwt
import os
from xlwt import Workbook
import datetime

HEADER_STRING = 	"#TEST_DESCR_START\n\
#NAME_single_ln()\n\
#VERSION_single_ln()\n\
#MODULE_NAME_single_ln()\n\
#PLATFORM_single_ln()\n\
#SUMMARY_single_ln()\n\
#DESCRIPTION_multi_ln()\n\
#PASS-CRITERIA_single_ln(Pass: )\n\
#TEST_DESCR_END"

WORKSPACE = '/mnt/c/code/jenkins-regression-tests/regression-suites/'
WORKBOOKPATH = '/mnt/c/code/jrt-testplan/'
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

	def clearProperties(self):
		self.name_str = ""
		self.ver_str = ""
		self.mod_str = ""
		self.plat_str = ""
		self.summ_str = ""
		self.desc_str = ""
		self.pf_str = ""
		self.own_str = ""

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
				dir1.replace(WORKSPACE, '')
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
						dir2.replace(WORKSPACE, '')
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
							dir3.replace(WORKSPACE, '')
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
			# print("Unable to open the file")
			return -1

	def createTestPlanSheet(self, folderName, workbook):
		sheetName = folderName
		#excel can accept sheet name upto 30 characters
		if len(sheetName) > 30:
			sheetName = sheetName[:29]

		excelSheet = workbook.add_sheet(sheetName)
		jobFiles = self.getJobFileNames(WORKSPACE + folderName)

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
			excelSheet.write(rowIndex, self.getIDExcelColumn('Module Name'), eachjob.replace((WORKSPACE + folderName + '/'), ''))
			excelSheet.write(rowIndex, self.getIDExcelColumn('Test Name'), self.name_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Test Summary'), self.summ_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Pass-Criteria'), self.pf_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Version'), self.ver_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Platform'), self.plat_str)
			excelSheet.write(rowIndex, self.getIDExcelColumn('Owner'), self.own_str)

	def createTestPlanWorkbook(self):
		#create and populate test plan
		print("Folder to process ", WORKSPACE)

		workb = Workbook()
		#parse job folder
		for eachdir in (os.listdir(WORKSPACE)):
			if os.path.isdir(os.path.join(WORKSPACE,eachdir)) == True:
				if self.enable_print:
					print("Dir...", eachdir)
				
				self.createTestPlanSheet(eachdir, workb)

		try:
			workb.save(WORKBOOKPATH + TESTPLAN_FILENAME)
			print("File saved as ", WORKBOOKPATH + TESTPLAN_FILENAME)
		except:
			print("Unable to save the excel file ", WORKBOOKPATH + TESTPLAN_FILENAME)
			fname,fext = os.path.splitext(TESTPLAN_FILENAME)
			renameFile = fname+str(datetime.datetime.now())+fext
			workb.save(WORKBOOKPATH + renameFile)
			print("File saved as ", WORKBOOKPATH + renameFile)

class utlis_jrt():
	def getAllFileNames(path):
		listfilename = []
		for dirpaths, dirnames, filenames in os.walk(mp.WORKSPACE):
			for filename in filenames:
			 	listfilename.append(filename)
		return listfilename

	def getAllFileNames(path, logfilename):
		listfilename = []
		if os.path.exists(logfilename):
			os.remove(logfilename)
		logfile = open(logfilename, 'a')

		for dirpaths, dirnames, filenames in os.walk(path):
			for filename in filenames:
				print(filename)
				
				fname,fext = os.path.splitext(filename)
				if fext == '.job':
					listfilename.append(filename)
					logfile.write(filename + '\n')
				else:
					print('Unknown job file ', filename)

		logfile.close()
		return listfilename

	def getAllFileNamesAndPath(path, logfilename):
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
					else:
						print('Unknown job file ', filename)
		logfile.close()

		return listFileNamePath

