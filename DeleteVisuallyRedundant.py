#!/usr/bin/env python3

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
	remainingFilepaths = []

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
		elif (size == maxSize):
			maxFilepaths.append(filepath)

	if (len(maxFilepaths) > 1):
		oldestModifiedTime = float("inf")

		for maxFilepath in maxFilepaths:
			modifiedTime = os.stat(maxFilepath).st_mtime

			if (modifiedTime < oldestModifiedTime):
				oldestModifiedTime = modifiedTime

		for maxFilepath in maxFilepaths:
			modifiedTime = os.stat(maxFilepath).st_mtime

			if(modifiedTime > oldestModifiedTime):
				print("D:", maxFilepath)
				if toDryRun == False:
					os.remove(maxFilepath)
			elif (modifiedTime == oldestModifiedTime):
				remainingFilepaths.append(maxFilepath)

	# Remove all but one duplicate if any still exist
	for remainingFilepath in remainingFilepaths[1:]:
		if toDryRun == False:
			os.remove(remainingFilepath)

filename_regex = re.compile("(.+?\.(?:jpe?g|png|gif))(?:\s+|$)", flags=re.IGNORECASE)
with open(dupsFile, 'r') as fp:
	for cnt, line in enumerate(fp):
		matches = filename_regex.findall(line)

		deleteAllButLargestAndOldest(matches)

if toRemoveDupFile:
	os.remove(dupsFile)

