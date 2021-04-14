##### Settings ############

# Local system paths. Use forward slashes, e.g. '/home/myuser/itunesbackup 'or 'c:/users/me/documents/SomeBackup' 
backup_base_path = 'F:/3f01edfbff9f017dc2eb6ff5782333ad9d7278fe' # The path to your backup folder. 
restore_path = 'F:/ipad_restore' # Where you want to restore the data.

# Source archive (backup) details - as from the archive database
archive_path_match = 'Media/DCIM/100APPLE/' # The beginning part of the archive path as defined in the backup, e.g. Media/DCIM/100APPLE/
archive_domain = 'CameraRollDomain' # The archive domain - the application in question.

# Other settings
restore_timestamps_via_exif = False # Try to use exif tags to restore file timestamps?
exif_filetypes = ['jpg','jpeg','tif','tiff']
debug_restore_file_count = 15 # Set to 0 or Null if not debugging!

############ BEGIN PROGRAM #############

### Constants

database_filename = 'manifest.db' # SQLite DB filename

### Script Start

# Imports (and related functions as needed
from pathlib import Path # So we can use sane paths
import os, sqlite3
if restore_timestamps_via_exif:
    from PIL import Image
    def get_date_taken(path): # A quick function to get the date
        return Image.open(path).getexif()[36867]

db_path = Path(backup_base_path,database_filename)

# Just a little diagnostic info
file_info = os.stat(db_path)
print(f'DB Size: {file_info.st_size/1024/1024:.1f}MB')



# SELECT "_rowid_",* FROM "main"."Files" WHERE "domain" LIKE '%CameraRollDomain%' ESCAPE '\' LIMIT 0, 49999;