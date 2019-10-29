#-*- coding: utf-8 -*-
'''
Name: FilesInFolder
Author: Blair Gemmer <blairg23@gmail.com>
Version: 20150131

Description: Checks existence of files from one given folder in the other given folder.

- If the left folder is larger than the right folder, it will return the filenames and hashes of the remaining files.
- If the right folder is larger than the left folder, it will return a True if all files from the left folder
exist in the right folder and a False with the filenames and hashes of the non-existence files.

'''
from time import clock # Time a function

import os  # Operating System functions
import sys # System Functions

# Hashing algorithms:
import hashlib
import base64

class FilesInFolder:
	def __init__(self, left_folder=None, right_folder=None, verbose=False):
		# Create the directory divider:	
		if os.name=='nt': # Windows environments
			self.divider = '\\'
		elif os.name=='posix': # Unix environments 
			self.divider = '/'
		self.verbose = verbose # Verbosity
		self.actionCounter = 0
		# If the directories have been provided:
		if left_folder != None and right_folder != None:
			self.CheckExistence(left_folder, right_folder)
		else:
			print '[ERROR] Please provide both a right and left folder directory.'


	def updateDirectory(self, directory):
		'''
		Updates the current working directory.
		'''
		if self.verbose:
			print '\n[{counter}] Updating the Current Working Directory.'.format(counter=self.actionCounter)
		cwd = os.getcwd() # The current working directory
		self.actionCounter +=1
		if self.verbose:
			print '[Previous working directory] {path}'.format(path=cwd)	
		os.chdir(directory) # Change the working directory to the specified directory	
		self.cwd = os.getcwd() # Grab the new current working directory
		if self.verbose:
			print '[Current working directory] {path}'.format(path=self.cwd)	


	def findSingleFiles(self, directory):
		'''
		Finds all the files without a folder within a given directory.
		'''	
		self.updateDirectory(directory=directory) # Update the current working directory
		# And find all the single files:
		if self.verbose:
			print '\n[{counter}] Finding files in {path}.'.format(counter=self.actionCounter, path=self.cwd)
		singleFiles = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]
		self.actionCounter += 1
		return singleFiles


	def get_hashes(self, directory, fileList):
		'''
		Populate a dictionary with filename:hash of binary, given a directory and file list.
		'''
		if self.verbose:
			print '\n[{counter}] Hashing files.'.format(counter=self.actionCounter)
		hashDict = {}		
		BLOCKSIZE = 65536 # In case any file is bigger than 65536 bytes				
		for fileName in fileList:
			fullPath = os.path.join(directory, fileName)
			with open(fullPath, 'rb+') as inFile:
				h = hashlib.new('md5')
				buf = inFile.read(BLOCKSIZE)
				while len(buf) > 0:
					h.update(buf)
					buf = inFile.read(BLOCKSIZE)
			hashDict[str(fileName)] = h.hexdigest()
		self.actionCounter += 1
		return hashDict

	def checkHashes(self, leftHashes, rightHashes, cwd):
		'''
		Checks the files that exist in the left and the right, as well as which exist in the left, but not the right.
		Writes the results to files in the root directory.
		'''
		hashCounter = 0 # Counter to keep track of how many hashes were written

		if self.verbose:
			print '\n[{counter}] Checking hashed files and writing results to files.'.format(counter=self.actionCounter)
		for k1, v1 in leftHashes.iteritems():
			inFolder = False # Whether or not the file is in the folder
			for k2,v2 in rightHashes.iteritems():
				if v1 == v2: # If the file is in the folder:
					inFolder = True
					with open(cwd+self.divider+'InRight_folder.txt', 'a+') as outFile:
						obj = str(k1) + ', ' + str(v1) + ' : ' + str(k2) + ', ' + str(v2) + '\n'
						outFile.write(obj)
					hashCounter += 1
			if not inFolder: # If the file was never found in the folder:
				with open(cwd+self.divider+'NotInRight_folder.txt', 'a+') as outFile:
						obj = str(k1) + ', ' + str(v1) + '\n'
						outFile.write(obj)		
		self.actionCounter += 1
		if hashCounter == len(leftHashes): # If we found as many matches as there are hashes:
			return True # Then we know all the files from the left folder are in the right folder
		else: # otherwise,
			print 'hashCounter=', hashCounter
			print 'leftHashes=', len(leftHashes)
			return False # there were files in the left folder that were NOT in the right folder.

	def CheckExistence(self, left_folder, right_folder):
		'''
		Checks existence of files from left folder in the right folder.
		'''
		# Print out the path of the left and right folders:
		if self.verbose:
			print '[Left Folder Path] {path}'.format(path=left_folder)			
			print '[Right Folder Path] {path}'.format(path=right_folder)

		originalCwd = os.getcwd()
		
		print "Beginning hashing files..."
		start_time = clock()

		# Grab the files from the left side first:		
		print "Hashing files on left folder..."
		left_start_time = clock()
		leftFiles = self.findSingleFiles(left_folder)
		leftHashes = self.get_hashes(directory=left_folder, fileList=leftFiles)		
		left_finish_time = clock() - left_start_time
		print "Hashing left files took " + str(left_finish_time) + " seconds.\n"

		# Then grab the files from the right side:		
		print "Hashing files on right folder..."
		right_start_time = clock()
		rightFiles = self.findSingleFiles(right_folder)		
		rightHashes = self.get_hashes(directory=right_folder, fileList=rightFiles)
		right_finish_time = clock() - right_start_time
		print "Hashing right files took " + str(right_finish_time) + " seconds.\n"
		finish_time = clock() - start_time
		print "Hashing took a total of " + str(finish_time) + " seconds.\n"

		# Print out the number of files in the left and right folders:
		if self.verbose:
			print '[Left Folder Size] {size}'.format(size=len(leftHashes))
			print '[Right Folder Size] {size}'.format(size=len(rightHashes))		

		# Finally, check those hashes:
		print "Starting to check hashes..."
		start_time = clock()
		result = self.checkHashes(leftHashes=leftHashes, rightHashes=rightHashes, cwd=originalCwd)
		finish_time = clock() - start_time
		print "Checking hashes took " + str(finish_time) + " seconds."
		
		if result:
			print '[Result] All files from the left folder are in the right folder.'
		else:
			print '[Result] Not all files from the left folder are in the right folder.'

if __name__ == '__main__':
	left_folder = ''
	right_folder = ''

	inFolder = FilesInFolder(left_folder=left_folder, right_folder=right_folder, verbose=True)
	