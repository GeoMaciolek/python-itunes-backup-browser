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
debug_restore_file_count = 15 # Set to 0 or Null if not debugging!

############ BEGIN PROGRAM #############

### Constants

database_filename = 'manifest.db' # SQLite DB filename

#example_query = '''SELECT "_rowid_",fileID,domain,relativePath FROM "main"."Files" WHERE "domain" LIKE '%CameraRollDomain%' AND "relativePath" LIKE '%Media/DCIM/100APPLE/%' LIMIT 0, 15;'''

base_query = '''SELECT "_rowid_",fileID,domain,relativePath FROM "main"."Files" WHERE "domain" LIKE ? AND "relativePath" LIKE ? LIMIT 0, 15;'''

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


### Script Start

# Imports (and related functions as needed
from pathlib import Path # So we can use sane paths
import os, sqlite3

"""
if restore_timestamps_via_exif:
    from PIL import Image
    def get_date_taken(path): # A quick function to get the date
        return Image.open(path).getexif()[36867]
"""

db_path = Path(backup_base_path,database_filename)

# Just a little diagnostic info
file_info = os.stat(db_path)
print(f'DB Size: {file_info.st_size/1024/1024:.1f}MB')

# 'Connect' to SQLite DB
con = sqlite3.connect(db_path)

con.row_factory = sqlite3.Row
cur = con.cursor()
# Tuple for the query - to fill in to limit SQL injection. The "domain" and the path match ("relativePath")
query_fill_tuple=(archive_domain,archive_path_match_sql)
cur.execute(base_query, query_fill_tuple)

one_row = cur.fetchone()
cur_file_id = one_row['fileID']
cur_file_source_subdir = cur_file_id[0:2] # The two-character directory that the backup file is stored in. e.g. 'ef/ef0313281238123'
cur_file_relpath = one_row['relativePath']
cur_file_basename = cur_file_relpath.replace(archive_path_match_base,'')

print("\nFilename: " + one_row['relativePath'] + " - Hash/ID: " + one_row['fileID'])

source_file = Path(backup_base_path,cur_file_source_subdir,cur_file_id)
file_info = os.stat(source_file)
print(f'Target Name: {cur_file_basename} - File size: {file_info.st_size/1024/1024:.1f}MB')

print("lol debug")