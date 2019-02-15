import sys
import os
import string
from subprocess import Popen, PIPE

def preview(packagePath, bundlePath):

	def getUserName():
		getUserName = '''
    			set usernamePath to POSIX path of (path to home folder)
 			set stringLength to length of usernamePath as string
    			set username to (text items 8 thru stringLength of usernamePath) as string
    			set stringLength_2 to (length of username) - 1
    			set username_2 to (text items 1 thru stringLength_2 of username) as string
    			'''
		p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
		stdout, stderr = p.communicate(getUserName)
		username = stdout.rstrip('\n')
		return username

	username = getUserName()
	
	# This set of code finds the most recent version of the simulator based on the folder names contained in 
	# the "/Users/userName/Library/Application Support/iPhone Simulator/" directory.

	simDir = "/Users/" + username + "/Library/Application Support/iPhone Simulator"

	simDirList = os.listdir(simDir)
	versions = []
	versionsNum = []

	for dir in simDirList:
    		versions.append(dir)
    		if dir.rfind(".") == 1: # Tests if the version number has two numbers only
        		dir = dir + "0"
    		dir = dir.replace(".","")
    		versionsNum.append(dir)

	versions2 = []
	versionsNum2 = []

	i = 0
	for x in versionsNum:
    		if x.isdigit():
        		versionsNum2.append(x)
        		versions2.append(versions[i])
    		i = i + 1

	maxVersion = max(versionsNum2)
	maxVersionIndex = versionsNum2.index(maxVersion)
	myVersion = versions2[maxVersionIndex]
	
	# Create the applications folder if it does not exist
	versionDirList = os.listdir(simDir + "/" + myVersion)
	
	flag = 0;
	for item in versionDirList:
		if item.upper() == "APPLICATIONS":
			flag = 1
	
	applicationsPath = simDir + "/" + myVersion + "/Applications"
	command = "mkdir %s" %("\"" + applicationsPath + "\"")
	
	if flag == 0:
		os.system(command)
		
	# Create a symlink pointing from the simulator directory to the build folder
	buildFolder = packagePath + "/Build_Folder"
	buildFolderList = os.listdir(buildFolder)
	for element in buildFolderList:
		if element != '.DS_Store':
			buildName = element

	buildPath = buildFolder + "/" + buildName
	
	# Create the symbolic link
	link2SimDir = "ln -s %s %s" %("\"" + buildPath + "\"", "\"" + applicationsPath + "\"")
	os.system(link2SimDir)
	
	contentBundleFolder = applicationsPath + "/" + buildName + "/Library/Content"
	
	# Remove existing symbolic links
	removeLink = "rm -r %s" %("\"" + contentBundleFolder + "/SimBundle\"")
	os.system(removeLink)
	
	# Create a symbolic link from the bundle to the build folder
	link2Build = "ln -s %s %s" %("\"" + bundlePath + "\"", "\"" + contentBundleFolder + "/SimBundle\"")
	os.system(link2Build)
        
	# Launch the simulator
	if bundlePath != '':	
		cmd = """osascript<<END
			tell application "iPhone Simulator" to activate
			END"""
		os.system(cmd)

