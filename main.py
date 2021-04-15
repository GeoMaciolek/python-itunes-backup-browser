##### Settings ############

# Local system paths. Use forward slashes, e.g. '/home/myuser/itunesbackup 'or 'c:/users/me/documents/SomeBackup' 
backup_base_path = 'F:/3f01edfbff9f017dc2eb6ff5782333ad9d7278fe' # The path to your backup folder. 
restore_path = 'F:/ipad_restore' # Where you want to restore the data.

# Source archive (backup) details - as from the archive database. (Note: % is a SQL wildcard
archive_path_match = 'Media/DCIM/100APPLE/%' # The beginning part ofthe archive path as defined in the backup, e.g. Media/DCIM/100APPLE/%
archive_domain = 'CameraRollDomain' # The archive domain - the application in question.

# Other settings
restore_timestamps_via_exif = False # Try to use exif tags to restore file timestamps?
exif_filetypes = ['jpg','jpeg','tif','tiff']
debug_restore_file_count = 4 # Set to 0 or Null if not debugging!
verbose = True # Print extra diagnostics (True / False)
testmode = True # Only print, don't actually copy files

############ BEGIN PROGRAM #############

## Constants

database_filename = 'manifest.db' # SQLite DB filename

#example_query = '''SELECT "_rowid_",fileID,domain,relativePath FROM "main"."Files" WHERE "domain" LIKE '%CameraRollDomain%' AND "relativePath" LIKE '%Media/DCIM/100APPLE/%' LIMIT 0, 15;'''

base_query = '''SELECT "_rowid_",fileID,domain,relativePath FROM "main"."Files" WHERE "domain" LIKE ? AND "relativePath" LIKE ? LIMIT 0,?;'''


## Imports (and related functions as needed)
import os, sqlite3

from pathlib import Path # So we can use sane, cross-patform paths
from shutil import copyfile # So we can copy files, of course.

"""
if restore_timestamps_via_exif:
    from PIL import Image
    def get_date_taken(path): # A quick function to get the date
        return Image.open(path).getexif()[36867]
"""

## Functions
verboseprint = print if (verbose or testmode) else lambda *a, **k: None # Prints if the "verbose" flag is true, otherwise nothing.


## Variable Initalization

# Split off the archive_path_match string into two - one for cleaning up file names, one for the SQL query
if not archive_path_match[-1] == '%':
    # No wildcard specified by user - add our own
    archive_path_match_sql = archive_path_match + '%'
    archive_path_match_base = archive_path_match # already correct
else:
    # wildcard specified by user - clean up
    archive_path_match_sql = archive_path_match # Already correct
    # we're going to remove the last character from this to clean it up
    archive_path_match_base = archive_path_match[:-1]


## Begin

db_path = Path(backup_base_path,database_filename)

# Just a little diagnostic info
file_info = os.stat(db_path)
verboseprint(f'DB Size: {file_info.st_size/1024/1024:.1f}MB')

# 'Connect' to SQLite DB
con = sqlite3.connect(db_path)

con.row_factory = sqlite3.Row
cur = con.cursor()
# Tuple for the query - to fill in to limit SQL injection.
# The "domain", the path match ("relativePath"), and the limit statement - if any
if (not debug_restore_file_count) or debug_restore_file_count == 0 or debug_restore_file_count == -1:
    limit_count = "-1"
else:
    limit_count = str(debug_restore_file_count)

query_fill_tuple=(archive_domain,archive_path_match_sql,limit_count)

file_count=0
for row in cur.execute(base_query, query_fill_tuple):
    file_count+=1
    cur_file_id = row['fileID']
    cur_file_source_subdir = cur_file_id[0:2] # The two-character directory that the backup file is stored in. e.g. 'ef/ef0313281238123'
    cur_file_relpath = row['relativePath']
    cur_file_basename = cur_file_relpath.replace(archive_path_match_base,'')
    
    verboseprint("\nFilename & Path: " + cur_file_relpath + " - Hash/ID: " + cur_file_id) # Print the info from the database as desired
    
    source_file = Path(backup_base_path,cur_file_source_subdir,cur_file_id)
    file_info = os.stat(source_file)
    verboseprint(f'Target Name: {cur_file_basename} - File size: {file_info.st_size/1024/1024:.1f}MB')

    full_source_file = Path(backup_base_path,cur_file_source_subdir,cur_file_id) # Essentially, /thebackup/a1b2b3b4-a134-eaa/3f/3fab37cd83e
    full_target_file = Path(restore_path,cur_file_basename)
    verboseprint("Copying " + str(full_source_file) + " to " + str(full_target_file))
    if not testmode:
        copyfile(full_source_file, full_target_file) # Do the actual file copy

verboseprint("File count: " + str(file_count))

verboseprint("lol debug")