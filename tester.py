import sys
import os
import shutil
from glob import glob
import time
import subprocess
import filecmp as cmp

# define this first to enable easy timing of RunInstances()
def timeme(method):
	def wrapper(*args, **kw):
		startTime = int(round(time.time() * 1000))
		result = method(*args, **kw)
		endTime = int(round(time.time() * 1000))
		# print("{}: {}ms".format(method.__name__,endTime - startTime))
		return (result,endTime-startTime)
	return wrapper

# Should compile java. No idea how java code is compiled as I don't use java and I have no intention to learn how to use its messed up toolchain.
def compile(file):
	# compile java
	raise Exception("Fuck java")
	javac = "javac"
	cmd = "{} {}".format(javac,file)
	proc = subprocess.Popen(cmd, shell=True) #, env = {'PATH': '/path/to/javac'})

# Here the compiled stuff should be run. Again, no idea how this is done. 
@timeme
def RunInstances():
	raise Exception("Fuck java")


## Starting from here things should be correct - though possibly ugly
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
	for i in range(4):
		file = glob(fw_path + "*/"*(3-i) + targetname +".java")
		if len(file) == 1:
			return file[0]
	raise Exception("File not found")

# Copies src to target
def moveFile(src,target):
	shutil.copyfile(src, target)


# Used to clean student solution files (&compilation stuff maybe, no idea)
def cleanFolder(path):
	files = glob(path + '/*')
	for f in files:
		os.remove(f)
	
def TestSolution(solutionPath,targetDestination, compilation_target):
	moveFile(solutionPath,targetDestination) # copy file to framework folder
	compile(compilation_target) # compile fw/src folder 
	(_,time) = RunInstances() # run all instances
	return time


def testing():
	# 0: get exercise number (for some filenames)
	if len(sys.argv) > 1:
		ex = sys.argv[1]
	else:
		ex = input("Enter exercise name (e.g. E1 or E2): ")
	# 1: get folders and compilation target
	(fw,sub,sol_target) = [GetFolder(n,ex) for n in ["framework","submission","solution"]]
	sol_student = glob(fw + "solutions")[0] # Results from the computation should be here
	compilation_target = GetJavaFile(fw,"AlgoDat_"+ex) # This is the compilation target. I think
	targetDestination = GetJavaFile(fw, ex) # The student submissions should be placed at this location

	# 2: Run with the E[0-9].java file provided in ./ that produces correct results
	solution = GetJavaFile("./",ex) #! EXPECTS E1.java/E2.java/... in the root folder. Should be the solution that generates correct outputs
	TestSolution(solution,targetDestination,compilation_target) # compile as usual, run instances as usual
	for f in glob(sol_student + "*"): # solutions are in folder where student-solutions are expected later, thus the name
		moveFile(f,sol_target) # move to correct folder (solution-target)
	
	# 3: Preparations are done at this point. Now get all submissions from students
	#		compile and compare their solutions to target solution.
	subs = glob(sub + "*.java")
	print("Found {} solutions".format(len(subs)))
	# 4: move to folder, compile, run stuff
	print(">>Testing student submissions")
	badStudents = []
	for s in subs:
		cleanFolder(sol_student)
		(time,_) = TestSolution(s,targetDestination,compilation_target)
		(i,m,e) = CompareDirectories(sol_student,sol_target) # identical, mismatch, not found etc
		string = "Identical: {}, Mismatch: {}, Not found: {}".format(i,m,e)
		if len(m) + len(e) > 0:
			badStudents.append((os.path.basename(s), len(m),len(e)))
		print("{} ({}ms): {}".format(os.path.basename(s),time,string))
	print("Mistakes found in the following solutions:")
	for bs in badStudents:
		print("  {}".format(bs))

# If not called as import run the testing function
if __name__ == "__main__":
	testing()