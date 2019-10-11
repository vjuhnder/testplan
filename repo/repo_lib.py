#!/usr/bin/python3
import sys, os, subprocess

REPO_PATH = '/mnt/c/code/jenkins-regression-tests/'

class ChDir(object):
    def __init__(self, new_dir):
        self._new_dir = new_dir
        self._old_dir = os.getcwd()

    def __enter__(self):
        os.chdir(self._new_dir)

    def __exit__(self, *args):
        os.chdir(self._old_dir)

def extractEmail(strval):
	return strval[strval.find("<")+1:strval.find(">")]

def extractAuthor(strval):
	return strval[0:strval.find("<")]

#Get files added of a revision
def get_repo_log(repo, changeset):

	with ChDir(repo):	    
	    run_cmd = subprocess.Popen(['hg','log','-r', changeset, '--template', b'{file_adds}'], stdout=subprocess.PIPE)
	    run_cmd.wait()
	    files_adds, _ = run_cmd.communicate()
	    files_added_list = str(files_adds, 'utf-8').split(' ')
	    # print("Files Added: ")
	    # for eachfile in files_added_list:
	    # 	print(eachfile)

	    run_cmd = subprocess.Popen(['hg','log','-r', changeset, '--template', b'{file_mods}'], stdout=subprocess.PIPE)
	    run_cmd.wait()
	    files_mods, _ = run_cmd.communicate()
	    files_modified_list = str(files_mods, 'utf-8').split(' ')
	    # print("Files Modified: ")
	    # for eachfile in files_modified_list:
	    # 	print(eachfile)
	    run_cmd = subprocess.Popen(['hg','log','-r', changeset, '--template', b'{author}'], stdout=subprocess.PIPE)
	    run_cmd.wait()
	    committer, _ = run_cmd.communicate()
	    commit_author = str(committer, 'utf-8')

	    author_email = extractEmail(commit_author)
	    author_name = extractAuthor(commit_author)

	return files_added_list + files_modified_list, author_name, author_email



if __name__ == "__main__":
	get_repo_log(REPO_PATH, 'a83913d5b585')

