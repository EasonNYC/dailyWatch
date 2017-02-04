# DailyWatch
**DailyWatch** is a Python script to watch your TV show folders and remove older episodes as new ones come in, much like a DVR would.

DailyWatch manages regularly downloaded TV Show folders (or podcasts etc.) by automaticly removing
old episodes for certain shows just like a DVR "season pass" might. The maximum number of episodes to keep on hand
at anytime for each show is configurable in the script settings, and DailyWatch is meant to be run scheduled in a crontab
according to the user's preference (ex. weekly, daily, hourly etc). DailyWatch is perfect for a HTPC or media server
because it allows the user to receive a large amount of "fresh" content on a nightly basis while quietly removing "stale"
content before it can fill up a hard drive.

++How it works:++ DailyWatch will search each directory specified in the watchDirs list. If it notices there are more shows
than the max specified, it will remove the "oldest modified file" in that directory and recursively
run until the directory and any sub directory contains an amount of eposodes equal to the max set for that show. It will
continue to run untill it has processed each directory listed.

**Configuration Options:**

++WatchDirs++ - list of directories to watch. Requires the full path of each show's main folder, along with the max number of episodes to keep, in parethesis and seperated by a comma. Searches
all subdirectories in this path as well (if their are folders inside for each season, for instance).

Ex:
watchDirs = [("/home/USERNAME/Media/Series/TheTVShowDirName", 5),

The above setting will watch the directory of the show "TheTVShowDirName" and remove the oldest modified file if it discovers there are more than 5 files above a specified threshold in bytes.(default threshold is 100000000 bytes)

++Safemode ++- when True(default) will move old files to the Safedir folder, when false it will delete old files permanently
++Safedir++ - an absolute path to a directory to move "old" files to (used when Safemode is True)
++threshold++ - only consider files above this number (in bytes) as episodes. 100000000 is the default
++log file++ - by defualt can be found in the dailyWatch directory.