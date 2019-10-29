from time import clock # Time a function
import os
import hashlib

def get_hashes(directory=None):
	'''
	Populate a dictionary with filename:hash of binary, given a directory and file list.
	'''	
	hashDict = {}		
	BLOCKSIZE = 65536 # In case any file is bigger than 65536 bytes				
	for fileName in os.listdir(directory):
		fullPath = os.path.join(directory, fileName)
		with open(fullPath, 'rb+') as inFile:
			h = hashlib.new('md5')
			buf = inFile.read(BLOCKSIZE)
			while len(buf) > 0:
				h.update(buf)
				buf = inFile.read(BLOCKSIZE)
		hashDict[str(fileName)] = h.hexdigest()	
	return hashDict

def check_hashes(left_hash_dict=None, right_hash_dict=None):
	'''
	Check that every hash from the left folder is in the right folder.
	Returns True if they are all there.
	Returns a list of the file names that are not, if they are not.
	'''
	missing_files = []
	for filename, _hash in left_hash_dict.iteritems():
		if _hash in right_hash_dict.values():
			pass
		else:
			missing_files.append(filename)
	if len(missing_files) == 0:
		return True
	else:
		return missing_files

if __name__ == '__main__':
	left_folder = ''
	right_folder = ''
	
	print "Beginning hashing files..."
	start_time = clock()
	print "Hashing files on left folder..."
	left_start_time = clock()
	left_hash_dict = get_hashes(directory=left_folder)
	left_finish_time = clock() - left_start_time
	print "Hashing left files took " + str(left_finish_time) + " seconds.\n"

	print "Hashing files on right folder..."
	right_start_time = clock()
	right_hash_dict = get_hashes(directory=right_folder)	
	right_finish_time = clock() - right_start_time
	print "Hashing right files took " + str(right_finish_time) + " seconds.\n"
	finish_time = clock() - start_time
	print "Hashing took a total of " + str(finish_time) + " seconds.\n"

	print "Starting to check hashes..."
	start_time = clock()
	results = check_hashes(left_hash_dict=left_hash_dict, right_hash_dict=right_hash_dict)
	finish_time = clock() - start_time
	print "Checking hashes took " + str(finish_time) + " seconds."

	if results == True:
		print "RESULTS: All files present in right folder!"
	else:
		print "RESULTS: The following files were not present in the right folder:"
		print results