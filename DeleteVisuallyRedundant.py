import getopt
import os
import re
import sys

dupsFile = "dups.txt"
filepath = None
toRemoveDupFile = True
toDryRun = False
opts, args = getopt.getopt(sys.argv[1:], "p:rd")

for o, a in opts:
	if o == "-p":
		filepath = a
	elif o == "-r":
		toRemoveDupFile = False
	elif o == "-d":
		toDryRun = True
		
if filepath == None:
	print("Error: Please provide path using the -p option")
	exit()

os.system("findimagedupes -R \"{}\" > \"{}\"".format(filepath, dupsFile))

def deleteAllButLargestAndOldest(filepaths):
	maxSize = 0
	maxFilepaths = []

	for filepath in filepaths:
		size = os.stat(filepath).st_size
		if (size > maxSize):
			maxSize = size
		
	for filepath in filepaths:
		size = os.stat(filepath).st_size
		
		if(size < maxSize):
			print("D:", filepath)
			if toDryRun == False:
				os.remove(filepath)
		
		if (size == maxSize):
			maxFilepaths.append(filepath)
			
	if (len(maxFilepaths) > 1):
		oldestModifiedTime = 0
		
		for maxFilepath in maxFilepaths:
			modifiedTime = os.stat(filepath).st_mtime
			
			if (modifiedTime < oldestModifiedTime):
				oldestModifiedTime = modifiedTime
		
		for maxFilepath in maxFilepaths:
			modifiedTime = os.stat(filepath).st_mtime
			
			if(modifiedTime > oldestModifiedTime):
				print("D:", maxFilepath)
				if toDryRun == False:
					os.remove(maxFilepath)


with open(dupsFile, 'r') as fp:
	for cnt, line in enumerate(fp):
		matches = re.findall("(?:(.*?(?:jpg|png|gif))[\s]{0,1})+?", line)
		
		deleteAllButLargestAndOldest(matches)

if toRemoveDupFile:
	os.remove(dupsFile)

