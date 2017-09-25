# DailyWatch
**DailyWatch** is a Python script which watches your Plex TV show folders and removes old episodes as new ones come in, just like a DVR.

DailyWatch manages TV show folders (or folders which contain podcasts etc.) by automaticly removing
old episodes for certain shows like a DVR "season pass". The user specifies the folders and maximum number of episodes to keep on hand
in an easy to configure txt file, and DailyWatch script can be scheduled in a chrontab to check for "stale" episodes however often you'd like. DailyWatch is perfect for a HTPC or media server because it allows the user to receive a large amount of "fresh" content on a daily basis while quietly removing older "stale" content before it can fill up a hard drive.

How it works: DailyWatch will (recursively) search each directory specified in the watchdirs.txt file. If it notices there are more shows
than the listed entry in the watchdirs.txt file specified, it will remove the "oldest modified file" in that directory and recursively
run until the directory and any sub directory contains an amount of eposodes equal to the number in the watchdirs.txt file specified for that show/podcast. Thge script will continue to run untill it has processed each directory listed in the watchdirs.txt folder.

**Configuration Options:**

For a full list of CLI options:

    python dailyWatch.py -h

**watchdirs.txt** - A file with the list of directories to watch. Requires the full path of each show's main folder, along with the max number of episodes to keep, on the same line seperated by a comma. Example:

    /home/USERNAME/Media/Series/TheTVShowDirName, 5

The above line specifies a folder to watch for the show "TheTVShowDirName" and a number of episodes to always keep on hand (5). DailyWatch will remove the oldest modified file if it discovers there are more than 5 files which are above a specified threshold in bytes. Note: If there are Season folders inside this folder, it will process all seasons (default threshold is 100000000 bytes, but this can be configured with the -t option).

Once your watchdirs.txt is configured correctly, edit your crontab to run dailyWatch on a periodic basis:

    sudo crontab -e

Next add this line to the end of the file (the below line tells crontab to run at 4:00 AM every day.

    0 4 * * * /usr/bin/python /home/USERNAME/dailyWatch/dailyWatch.py 

Other options:

Safemode- when True(default) will move old files to the Safedir folder, when false it will delete old files permanently  
Safedir - an absolute path to a directory to move "old" files to (used when Safemode is True)  
threshold - only consider files above this number (in bytes) as episodes. 100000000 is the default  
log file - by defualt can be found in the dailyWatch directory.
