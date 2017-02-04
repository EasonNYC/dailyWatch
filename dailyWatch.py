# dailyWatch.Py
# Author:Eason Smith
# Email:eason@easonrobotics.com
#
# dailyWatch.py will watch TV show folders you specify for new episodes and delete older ones. It does this by looking
# for an overage in the number of large files # it finds(eg. the number of TV episodes in a TV show's episode folder).
#
# When the total number of episodes is above a pre-specified max, it removes the oldest file in that directory.
# Searches all subdirecties as well.
#
# To use this script:
# Add/change absolute paths in watchDirs to your shows, along with the max number of episodes to keep,
# change safemode to False if you want to delete old files instead of moving them to another directory
# change safeDir to the folder you wish to store files the script marks for removal when safemode is True
# change the min threshold (in bytes) of the files the script should search (default value seems to work fine for me)
# run the script in your OS as a chronological job every night (I run it at 4:30am).
#################################################################################
import os
import datetime
import shutil

###OPTIONS
SAFEMODE = True # change safemode to False to enable auto-deletion of episodes (default = True)
safeDir = "/home/USERNAME/deleteme" # directory to move files to if safemode is True

# Each tv show's absolute path/dir to watch, plus max number of episodes to retain.
watchDirs = [("/home/USERNAME/Media/Series/The Graham Norton Show", 5),
             ("/home/USERNAME/Media/Series/The Tonight Show Starring Jimmy Fallon", 3),
             ("/home/USERNAME/Media/Series/Last Week Tonight With Jon Oliver", 5),
             ]
threshold = 100000000 #bytes. Will only look for files above this size (in bytes)
#threshold = 0


# Function: log
# Arguments: (string) message, (optional) path to log.txt
# Description: logger function prints to a standard text file as well also prints to the console.
# Prints to the same dir by default if path to logfile is omitted.
def log(msg, logfile=os.path.dirname(os.path.realpath(__file__)) + '/log.txt'):
    curtime = datetime.datetime.now()
    with open(logfile, 'a+') as logfile:
        logfile.writelines('[' +str(curtime)+'] ' + msg+'\n')
        logfile.close()


# Function: removeOldEp
# Arguments: (string) path to the show folder, (int) max number of files/episodes to keep
# Description: If more than the max number of files exist in a folder, this function will
# recursively find and remove or delete the oldest file till the threshold is met. Search includes subdirectories.
def removeOldEp(d, maxEpisodes):
    # init oldest file
    oldest_modified = datetime.datetime.now()
    path_to_oldest_file = ""
    num_episodes_found = 0

    for dirpath, dirnames, filenames in os.walk(d):
        # print(dirpath)
        for file in filenames:
            # save the current path
            curpath = os.path.join(dirpath, file)

            # get the size and the date file was modified.
            filesize = os.stat(curpath).st_size  # in bytes
            time_last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))

            if (filesize > threshold):

                # track the oldest episode
                num_episodes_found = num_episodes_found + 1
                if (time_last_modified < oldest_modified):
                    oldest_modified = time_last_modified
                    path_to_oldest_file = curpath

                    # old stuff based on time
                    # if (datetime.datetime.now() - time_last_modified) > datetime.timedelta(days=14) and size > 100000000:
                    # print(str(curpath) + " " + str(size))
                    # os.remove(curpath)

    print("Processing: " + d)
    print("Number of episodes found: " + str(num_episodes_found) + " (max:" + str(maxEpisodes) + ")")
    # remove the oldest episode(s) of the current show recursively, or finish processing current show and continue.
    if (num_episodes_found > maxEpisodes):
        if SAFEMODE:
            print("removing " + str(path_to_oldest_file) + " " + str(oldest_modified))
            shutil.move(path_to_oldest_file, safeDir) #move but don't delete
        else:
            print("deleting " + str(path_to_oldest_file) + " " + str(oldest_modified))
            # os.remove(path_to_oldest)

        #recursively process each show, exit when show is below max num of episodes to keep
        removeOldEp(d, maxEpisodes)

    else:
        print("ok")
        print("Finished Processing: " + d)


######main
log("dailyWatch starting...")
for dirs, limit in watchDirs:
    removeOldEp(dirs, limit)
log("dailyWatch done. \n")