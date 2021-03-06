#-*- coding: utf-8 -*-
'''
Description: Checks existence of files from one given folder in the other given folder.

- If the left folder is larger than the right folder, it will return the filenames and hashes of the remaining files.
- If the right folder is larger than the left folder, it will return a True if all files from the left folder
exist in the right folder and a False with the filenames and hashes of the non-existence files.

'''

import os  # Operating System functions
import sys # System Functions
import shutil # File copy operations

import hashlib # Hashing functions
import json # JSON stuff


from time import localtime as clock # Time a function

# Filenames we don't want to check:
PROTECTED_FILENAMES = ['contents.csv', 'missing.txt']

class FilesInFolder:
    def __init__(
                    self,
                    left_folder=None,
                    right_folder=None,
                    write_mode=None,
                    hash_algorithm='md5',
                    hash_type='contents',
                    contents_filename='contents.json',
                    missing_files_filename='missing.txt',
                    fix_missing_files=False,
                    verbose=False
                ):

        self.verbose = verbose
        self.action_counter = 0
        self.write_mode = write_mode
        self.hash_algorithm = hash_algorithm
        self.hash_type = hash_type
        self.left_folder = left_folder
        self.right_folder = right_folder
        self.contents_filename = contents_filename
        self.missing_files_filename = missing_files_filename
        self.fix_missing_files = fix_missing_files

        try:
            # If valid directories have not been provided:
            if self.left_folder == None or self.right_folder == None or not os.path.exists(self.left_folder) or not os.path.exists(self.right_folder):
                raise IOError('[ERROR] Please provide valid right and left directories.')
            else:               
                print('[{action_counter}] Left Directory: {left_folder}'.format(action_counter=self.action_counter, left_folder=self.left_folder))
                print('[{action_counter}] Right Directory: {right_folder}'.format(action_counter=self.action_counter, right_folder=self.right_folder))
                print('\n')

        except Exception as e:
            print(e)        



    def find_filenames(self, directory=None):
        '''
        Finds all the filenames in a given directory.
        '''
        filenames = []
        try:
            if directory == None or not os.path.exists(directory):
                raise IOError('[ERROR] Please provide a valid directory to search.')    
            else:                               
                if self.verbose:
                    print('[{action_counter}] Finding files in {directory}.\n'.format(action_counter=self.action_counter, directory=directory))

                filenames = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory,f))]

                self.action_counter += 1

        except Exception as e:
            print(e)

        return filenames


    def hash_file_contents(self, filepath=None, hash_algorithm='md5'):
        '''
        Uses given hashing algorithm to hash the binary file, given a full filepath.
        '''
        BLOCKSIZE = 65536 # In case any file is bigger than 65536 bytes             
        hash_value = 0x666
        try:
            if self.verbose:
                print('[{action_counter}] Hashing file contents of {filepath}.\n'.format(action_counter=self.action_counter, filepath=filepath))
            
            if filepath == None or not os.path.exists(filepath):
                raise IOError('[ERROR] Please provide a valid filepath to hash.')
            with open(filepath, 'rb+') as inFile:
                h = hashlib.new(hash_algorithm)
                buf = inFile.read(BLOCKSIZE)
                while len(buf) > 0:
                    h.update(buf)
                    buf = inFile.read(BLOCKSIZE)
            hash_value = h.hexdigest()
        except Exception as e:
            print(e)

        return hash_value

    def hash_filename(self, filename=None, hash_algorithm='md5'):
        '''
        Uses given hashing algorithm to hash the given filename.
        '''
        hash_value = 0x666
        try:            
            if self.verbose:
                print('[{action_counter}] Hashing filename {filename}.\n'.format(action_counter=self.action_counter, filename=filename))
            if filename == None:
                raise IOError('[ERROR] Please provide a filename to hash.')
            else:
                h = hashlib.new(hash_algorithm)
                h.update(filename)
                hash_value = h.hexdigest()
        except Exception as e:
            print(e)
        return hash_value

    def get_hashes(self, directory=None, hash_algorithm='md5', hash_type='contents'):
        '''
        Populate a dictionary with filename:hash_value pairs, given a directory and list of filenames.
        '''
        hashlist = {}
        hashlist['headers'] = ['hash_value', 'filepath']
        try:
            if directory == None or not os.path.exists(directory):
                raise IOError('[ERROR] Please provide a valid directory to hash.')  
            else:                               
                filenames = self.find_filenames(directory=directory)
                for filename in filenames:
                    if filename not in PROTECTED_FILENAMES:
                        filepath = os.path.join(directory, filename)
                        if hash_type == 'contents':
                            hash_value = self.hash_file_contents(filepath=filepath, hash_algorithm=hash_algorithm)
                        elif hash_type == 'filenames':
                            hash_value = self.hash_filename(filename=filename, hash_algorithm=hash_algorithm)
                        hashlist[str(hash_value)] = str(filepath)
                        self.action_counter += 1
        except Exception as e:
            print(e)

        return hashlist


    def write_dictionary_contents(self, dictionary_contents={}, write_mode=None, contents_filepath=None):
        '''
        Writes contents of a given dictionary, using the specified write mode (JSON or CSV).
        '''
        valid_write_modes = ['json', 'csv']
        try:
            if dictionary_contents == {}:
                raise Exception('[ERROR] Need to provide a valid dictionary with contents.')
            elif write_mode == None or not write_mode.lower() in valid_write_modes:
                raise Exception('[ERROR] Need to provide a write mode from: {valid_write_modes}'.format(valid_write_modes=valid_write_modes))
            elif contents_filepath == None:
                raise Exception('[ERROR] Need to provide a valid file to write contents.')
            else:               
                with open(contents_filepath, 'a+') as outfile:
                    if write_mode.lower() == 'json':
                        json.dump(dictionary_contents, outfile)                 
                    elif write_mode.lower() == 'csv':
                        headers = ','.join(dictionary_contents['headers'])
                        outfile.write(headers + '\n')
                        for key,value in dictionary_contents.items():
                            if key != 'headers':
                                output_line = key + ',' + value + '\n'
                                outfile.write(output_line)
                    else:
                        raise Exception('[ERROR] Need to provide a write mode from: {valid_write_modes}'.format(valid_write_modes=valid_write_modes))
        except Exception as e:
            print(e)

    def compare_hash_lists(self, left_hash_dict=None, right_hash_dict=None):
        '''
        Given two hash lists, will compare them to ensure all hashes 
        from left list exist in right list, then will return the list of
        all hashes that are missing.
        '''
        missing_hash_value_filepaths = []
        for hash_value, filepath in left_hash_dict.items():
            if not hash_value in right_hash_dict.keys():
                missing_hash_value_filepaths.append(filepath)
        return missing_hash_value_filepaths

    def write_list_contents(self, list_contents=[], missing_files_filepath=None):
        '''
        Writes contents of a given list to a file.
        '''
        try:
            if list_contents == []:
                raise Exception('[ERROR] Need to provide a valid list with contents.')
            else:
                with open(missing_files_filepath, 'a+') as outfile:
                    for value in list_contents:
                        outfile.write(value + '\n')
        except Exception as e:
            print(e)


    def write_missing_files(self, missing_filepaths=[], destination_directory=None):
        '''
        Writes missing files to the destination filepath.
        '''
        try:
            if missing_filepaths == []:
                raise Exception('[ERROR] Need to provide a valid list of missing files.')
            else:
                for missing_filepath in missing_filepaths:
                    missing_filename = os.path.basename(missing_filepath)
                    # Use copy2 to retain metadata such as creation and modification times of the file
                    destination_filepath = os.path.join(destination_directory, missing_filename)
                    shutil.copy2(missing_filepath, destination_filepath)
        except Exception as e:
            print(e)


    def cleanup(self):
        '''
        Cleans up metadata files like contents.csv and missing.txt
        '''
        self.action_counter += 1
        for filename in PROTECTED_FILENAMES:
            left_file_to_delete = os.path.join(self.left_folder, filename)
            right_file_to_delete = os.path.join(self.right_folder, filename)

            if os.path.exists(left_file_to_delete):
                if self.verbose:
                    print(f'[{self.action_counter}] Deleting {left_file_to_delete}.\n')
                os.remove(left_file_to_delete)
                self.action_counter += 1

            if os.path.exists(right_file_to_delete):
                if self.verbose:
                    print(f'[{self.action_counter}] Deleting {right_file_to_delete}.\n')
                os.remove(right_file_to_delete)
                self.action_counter += 1
                

    def run(self):
        '''
        Runs all the required functions to check whether two folders have identical content.
        '''
        left_hash_dict = self.get_hashes(directory=self.left_folder, hash_algorithm=self.hash_algorithm, hash_type=self.hash_type)
        right_hash_dict = self.get_hashes(directory=self.right_folder, hash_algorithm=self.hash_algorithm, hash_type=self.hash_type)
        
        missing_hash_value_filepaths = self.compare_hash_lists(left_hash_dict=left_hash_dict, right_hash_dict=right_hash_dict)

        if self.write_mode != None:
            # Missing files:
            if len(missing_hash_value_filepaths) == 0:
                print('All files from left folder exist in right folder.')
                print('Left Folder:' ,self.left_folder)
                print('Right Folder:', self.right_folder)
                print('\n')

                # Left side:            
                left_outfilepath = os.path.join(self.left_folder, self.contents_filename)
                self.write_dictionary_contents(dictionary_contents=left_hash_dict, write_mode=self.write_mode, contents_filepath=left_outfilepath)
                if self.verbose:
                    print('[{action_counter}] Writing contents to {contents_filepath}.\n'.format(action_counter=self.action_counter, contents_filepath=left_outfilepath))

                self.action_counter += 1

                # Right side:
                right_outfilepath = os.path.join(self.right_folder, self.contents_filename) 
                self.write_dictionary_contents(dictionary_contents=right_hash_dict, write_mode=self.write_mode, contents_filepath=right_outfilepath)
                if self.verbose:
                    print('[{action_counter}] Writing contents to {contents_filepath}.\n'.format(action_counter=self.action_counter, contents_filepath=right_outfilepath))

                self.action_counter += 1 
            else:   
                missing_files_filepath = os.path.join(self.left_folder, missing_files_filename)
                if self.verbose:
                    print('[{action_counter}] Writing missing file info to {missing_files_filepath}.\n'.format(action_counter=self.action_counter, missing_files_filepath=missing_files_filepath))
                self.write_list_contents(list_contents=missing_hash_value_filepaths, missing_files_filepath=missing_files_filepath)
                self.action_counter += 1

                if self.fix_missing_files:
                    if self.verbose:
                        print(f'[{self.action_counter}] Writing missing files to {self.right_folder}.\n')
                    self.write_missing_files(missing_filepaths=missing_hash_value_filepaths, destination_directory=self.right_folder)
                    self.action_counter += 1


                    if self.verbose:
                        print(f'[{self.action_counter}] Cleaning up metadata files.\n')
                    self.cleanup()
                    
                    if self.verbose:
                        print(f'[{self.action_counter}] Rerunning file checker.\n')
                    self.action_counter += 1
                    self.run()


                       
        else:
            print('Files missing from left folder that exist in right folder:')
            print(missing_hash_value_filepaths)


if __name__ == '__main__':
    # Until I use arg parse:
    left_folder = ''
    right_folder = ''

    hash_algorithm = 'md5'
    hash_type = 'contents' # Other option is "filenames"
    write_mode = 'csv'
    contents_filename = 'contents.csv'
    missing_files_filename = 'missing.txt'
    fix_missing_files = True

    file_checker = FilesInFolder(
                                    left_folder=left_folder,
                                    right_folder=right_folder,
                                    write_mode=write_mode,
                                    hash_algorithm=hash_algorithm,
                                    hash_type=hash_type,
                                    contents_filename=contents_filename,
                                    missing_files_filename=missing_files_filename,
                                    fix_missing_files=fix_missing_files,
                                    verbose=True
                                )

    
    # Some calls you can use to test (until I write good unit tests):

    # filenames = file_checker.find_filenames(directory=left_folder)

    #hashlist = file_checker.get_hashes(directory=left_folder, hash_algorithm=hash_algorithm, hash_type=hash_type)

    #contents_filepath = os.path.join(left_folder, contents_filename)
    #file_checker.write_dictionary_contents(dictionary_contents=hashlist, write_mode=write_mode, contents_filepath=contents_filepath)
    file_checker.run()