'''
Name: filename_in_folder.py
Date: 2015-10-06
Author: Blair Gemmer
Description: Check if the file from the left folder is in the right folder.

The left folder contains files with the format "IMG_YYYYMMDD_HHMMSS.jpg", where HH is in 24 hour format, as well
as files with the format "Screenshot_YYYY-MM-DD-HH-MM-SS.png", where HH is in 24 hour format,
while the right folder contains files with the format "YYYY-MM-DD HH.MM.SS.extension", where HH is in 24 hour format
and "extension" is the original file extension.

The first pass involves creating a list of the files in the format of the right folder.
The second pass checks each filename in the list to see if it exists in the right folder.
If the second pass succeeds, it returns a True. Otherwise, it returns a list of the filenames that where
not present in the right folder.

Version: 2015.10.06
'''

import os

def sanitize_filenames(filename_list=None, debug=False):
	'''
	Sanitize the given filename into the format YYYY-MM-DD HH.MM.SS.extension
	'''
	def split_png(filename=None):
		'''
		Split a file with the format Screenshot_YYYY-MM-DD-HH-MM-SS.png
		'''
		filename_split = filename.split('_')	# example: ['Screenshot', '2015-01-01-24-30-00']
		date_time = filename_split[1]			# example: 2015-01-01-24-30-00
		date_time_split = date_time.split('-')	# example: ['2015', '01', '01', '24', '30', '00']
		date = ''
		for element in date_time_split[0:3]:	# example: 20150101
			date += element
		time = ''
		for element in date_time_split[3:6]:	# example: 243000
			time += element
		return date, time

	def split_other(filename=None):
		'''
		Split a file with the format IMG_YYYYMMDD_HHMMSS.jpg
		'''		
		filename_split = filename.split('_')			# example: ['VID', '20150101', '153038.mp4']
		date = filename_split[1]						# example: 20150101
		time = filename_split[2]						# example: 153038
		return date, time

	def split_date(date=None):
		'''
		Splits the given date from YYYYMMDD to YYYY, MM, DD and returns them.
		'''
		return date[0:4], date[4:6], date[6:8] # YYYY, MM, DD
	def split_time(time=None):
		'''
		Splits the given time from HHMMSS to HH, MM, SS and returns them.
		'''
		return time[0:2], time[2:4], time[4:6] # HH, MM, SS

	if filename_list != None:
		for filename in filename_list:
			filename_index = filename_list.index(filename)
			filename, extension = os.path.splitext(filename) # Get the filename and extension

			# Sanitize the filename to the appropriate format:
			if extension == '.png':
				date, time = split_png(filename=filename) # Treat pngs differently				
			else:
				date, time = split_other(filename=filename) # For jpg or mp4

			# Further split up the date and time into their separate elements:
			year, month, day = split_date(date=date)
			hour, minute, second = split_time(time=time)
			
			# Finally, modify the original list of filenames with the updated filename:
			updated_filename = year + '-' + month + '-' + day + ' ' + hour + '.' + minute + '.' + second + extension # YYYY-MM-DD HH.MM.SS.extension
			
			if debug:
				print filename+extension, updated_filename
			filename_list[filename_index] = updated_filename


## Just in case it failed to check the first time.			
def double_check_folder(filename_list=None, folder_name=None):
	check_folder(filename_list, folder_name)
	check_folder(filename_list, folder_name)
	
def check_folder(filename_list=None, folder_name=None):
	'''
	Checks the right folder for the existence of every filename in the list.
	Returns True if they all exist. 
	Returns a list of the missing filenames if they do not all exist.
	'''
	if filename_list != None:
		if folder_name != None:
			for filename in filename_list:
				if filename not in os.listdir(folder_name):
					print filename
				# if filename in os.listdir(folder_name):
				# 	print filename
		else:
			print '[ERROR] FOLDER NAME REQUIRED!'
	else:
		print '[ERROR] LIST OF FILENAMES REQUIRED!'

if __name__ == '__main__':
	left_folder = ''
	right_folder = ''

	# First, create a list of the filenames from the left folder:
	filename_list = []
	for filename in os.listdir(left_folder):
		filename_list.append(filename)
	# Then, sanitize them:
	sanitize_filenames(filename_list=filename_list)

	# Finally, check if they exist in the right folder:
	check_folder(filename_list=filename_list, folder_name=right_folder)
