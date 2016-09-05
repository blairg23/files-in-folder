# files-in-folder
A class to check the files in two folders, given some parameters.

* Can do diff on two folders based on one of the following parameters:

1. Hash of filenames (for simply checking if two folders have files with identical names).
2. Hash of file contents (for checking the actual contents of two folders' files in the case that some files may have been renamed).

* Can write key:value pairs of filename to hash value to JSON or CSV and/or write that JSON or CSV to a file.
* Can output log of missing files and hash values from the left comparison folder.
* Can write key:value pairs of filename from left folder to filename of right folder to match up the missing files and write those to JSON or CSV and/or write that JSON or CSV to a file.
