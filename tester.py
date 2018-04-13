import sys
import os
import shutil
from glob import glob
import time
import subprocess
import filecmp as cmp

## Starting from here things should be fine
def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        # print("{}: {}ms".format(method.__name__,endTime - startTime))
        return (result,endTime-startTime)
    return wrapper

##! IF SOMETHING IS NOT WORKING, ERROR IS MOST LIKELY IN THESE FUNCTIONS
# Compiles java
def compile(file):
	# compile java
	javac = "javac"
	cmd = "{} {}".format(javac,file)
	proc = subprocess.Popen(cmd, shell=True) #, env = {'PATH': '/path/to/javac'})

@timeme
def RunInstances():
	return "result"

def CompareDirectories(a,b):
	af = {os.path.basename(f) for f in glob(a + "/*")}
	bf = {os.path.basename(f) for f in glob(b + "/*")}
	common = af.union(bf)
	return cmp.cmpfiles(a,b,list(common), shallow=False)




# List folder[s] and return selection 
def GetFolder(name, filter = ""):
	if filter != "":
		filter += "*"
	folders = glob("./{}/*{}/".format(name,filter))
	if len(folders) == 1:
		return folders[0]
	# if more than one folder or zero
	folders = glob("{}*/".format(name)) # search without filter
	for i, f in enumerate(folders):
		print("{}: {}".format(i+1, f))
	while True:
		x = int(input("Select the {} folder: ".format(name))) - 1
		if x >= 0 and x < len(folders):
			print("{} folder: {}".format(name, folders[x]))
			return folders[x]

# Look in fw_path subfolders (depth<=3) for a file called <targetname>.java
def GetJavaFile(fw_path, targetname):
	for i in range(3):
		file = glob(fw_path + "*/"*(3-i) + targetname +".java")
		if len(file) == 1:
			return file[0]
	raise Exception("File not found")

# Copies src to target
def moveFile(src,target):
	shutil.copyfile(src, target)

# # Get instances
# def GetInstances(path):
# 	return glob(path)


# Used to clean student solution files (&compilation stuff maybe, no idea)
def cleanFolder(path):
	files = glob(path + '/*')
	for f in files:
		os.remove(f)
	
@timeme
def DoNothing():
	return 1

def testing():
	# 0: get exercise number (for some filenames)
	if len(sys.argv) > 1:
		ex = sys.argv[1]
	else:
		ex = input("Enter exercise name (e.g. E1 or E2): ")
	# 1: get folders and compilation target
	(fw,sub,sol_target) = [GetFolder(n,ex) for n in ["framework","submission","solution"]]
	sol_student = glob(fw + "solutions")[0] # solutions from student
	compilation_target = GetJavaFile(fw,"AlgoDat_"+ex) # i guess?
	# 2: get destination path of Solution files
	target = GetJavaFile(fw, ex)
	# 3: get all solutions
	subs = glob(sub + "*.java")
	print("Found {} solutions".format(len(subs)))
	# 4: move to folder, compile, run stuff
	print(">>Testing student submissions")
	badStudents = []
	for s in subs:
		moveFile(s,target)
		cleanFolder(sol_student)
		# cleanFolder(compilation files)
		#! compile(compilation_target)
		(result,time) = DoNothing() # assign values to result and time. remove if RunInstances is run instead
		#! (result,time) = RunInstances(no idea how this works)
		(i,m,e) = CompareDirectories(sol_student,sol_target)
		string = "Identical: {}, Mismatch: {}, Not found: {}".format(i,m,e)
		if len(m) + len(e) > 0:
			badStudents.append(os.path.basename(s))
		print("{} ({}ms): {}".format(os.path.basename(s),time,string))
	print("Bad students:")
	for bs in badStudents:
		print("  {}".format(bs))

if __name__ == "__main__":
	testing()