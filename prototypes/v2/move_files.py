# -*- coding: utf-8 -*-
'''
Name: move_files.py
Author: Blair Gemmer
Version: 20160719

Description: 

Given a CSV with a list of missing files, will import the files

from the left folder to the right folder. Performs a copy operation,

rather than a move operation.


'''

import pandas as pd
import os
import shutil

def get_file_list(csv_filepath=None, filename_column='filename'):
	file_dataframe = pd.read_csv(csv_filepath)
	return file_dataframe[filename_column].tolist()

def move_files(left_folder=None, right_folder=None, file_list=None):	
	for filename in file_list:
		left_filepath = os.path.join(left_folder, filename)
		if os.path.exists(left_filepath):			
			right_filepath = os.path.join(right_folder, filename)
			if not os.path.exists(right_filepath):
				shutil.copy2(left_filepath, right_filepath)
				print '[ACTION] {left_filepath} -> {right_filepath} successfully.'.format(
																							left_filepath=left_filepath, 
																							right_filepath=right_filepath
																						)	
		else:
			print '[ERROR] {left_filepath} does not exist.'.format(left_filepath=left_filepath)
	print '[ACTION] Copied all files successfully.'
	


if __name__ == '__main__':
	left_folder = ''
	right_folder = ''
	csv_filepath = ''
	file_list = get_file_list(csv_filepath=csv_filepath)
	move_files(left_folder=left_folder, right_folder=right_folder, file_list=file_list)