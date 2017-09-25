# DailyWatch
**DailyWatch** is a Python script which watches your Plex TV show folders and removes old episodes as new ones come in, just like a DVR.

Programmed by: Eason Smith (Eason@EasonRobotics.com)

DailyWatch is written for linux with support for Python 2.6/3.5 

- [Intro](#intro)
- [CLI Options](#options)
- [How to Configure](#configuration)

<a name='intro'></a>
DailyWatch manages TV show folders (or folders which contain podcasts etc.) by automaticly removing
old episodes for certain shows like a DVR "season pass". The user specifies the folders and maximum number of episodes to keep on hand in an easy to configure txt file, and DailyWatch script can be scheduled in a chrontab to check for "stale" episodes however often you'd like. DailyWatch is perfect for a HTPC or media server because it allows the user to receive a large amount of "fresh" content on a daily basis while quietly removing older "stale" content before it can fill up a hard drive.

<a name='options'></a>
Options
========  

For a list of CLI options:

    python dailyWatch.py -h  



<a name='configuration'></a>
How to Configure:
================

Clone this repo into your home directory and open watchdirs.txt using your favorite text editor: 

    nano watchdirs.txt

This file should be edited to contain a list of directories to watch with the number of episodes to keep on each line, seperated by a comma. Example:

    /home/USERNAME/Media/Series/TheTVShowDirName, 5

DailyWatch will recursively remove the oldest modified file found in this directory (above a specified threshold in bytes) untill it has exactly five files. It then moves on to the next entry to process. Note that if you have folder/s within the folder you listed in your watchdirs.txt file, dailywatch will process all of those folders as well.

Once your watchdirs.txt is configured correctly, edit your crontab to run dailyWatch.py on a periodic basis:

    sudo crontab -e

Next add this line to the end of the crontab file (the example below tells crontab to run at 4:00 AM every day.)

    0 4 * * * /usr/bin/python /home/USERNAME/dailyWatch/dailyWatch.py 

DailyWatch outputs to a log file, which may be helpful to the user when debugging the script. (log.txt)
