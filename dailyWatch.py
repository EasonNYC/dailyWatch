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
import argparse


###OPTIONS
SAFEMODE = True # change safemode to False to enable auto-deletion of episodes (default = True)
safeDir = "/home/epiczero/deleteme" # directory to move files to if safemode is True
threshold = 100000000 #bytes.  Will only process files above this size
logfile = os.path.dirname(os.path.realpath(__file__)) + '/log.txt'
watchDirs = []
watchfile = "watchdirs.txt"


#PARSE ARGUMENTS
    
parser = argparse.ArgumentParser(description='dailyWatch will watch your TV show directories and keep only the latest episodes.')
parser.add_argument("-d", action="store", help='filename of watch file. Must use full path and be properly formatted (see example watchfile.)')
parser.add_argument("-l", action="store", help='file to store log info')
parser.add_argument("-t", action="store", type=int, help='ignore all files below NUM bytes. Default=100000000')
parser.add_argument("-s", action="store", help='True = script will move your files to the designated directory instead of deleting them. is always TRUE for now. Default=True [FUTURE IMPLIMENTATION].')
args = parser.parse_args()
    
#log incoming arguments
argstr = "args:"
for a in str(args):
    argstr+= a

#handle arguments
if args.d != None:
    watchfile = args.d
if args.l != None:
    logfile = args.l
if args.s != None:
    pass #TODO
if args.t != None:
    if args.t < 1:
        print(" ERROR command line argument (-t threshold in [bytes]) can not be less than 1. Exiting....")
        exit()
    threshold = args.t
    #todo add --dryrun  print result only
    #todo add -m specify safemode folder
    #todo add -v turn on verbose output    


# Function: log
# Arguments: (string) message, (optional) path to log.txt
# Description: logger function prints to a standard text file as well also prints to the console.
# Prints to the same dir by default if path to logfile is omitted.
def log(msg, logfile=logfile):
    curtime = datetime.datetime.now()
    print('[' +str(curtime)+'] ' + msg+'\n')
    with open(logfile, 'a+') as logfile:
        logfile.writelines('[' +str(curtime)+'] ' + msg+'\n')
        logfile.close()


# Function: loadWatchDirs
# Arguments: (string) path+filename of watchfile
# Description: opens a the file of directories to watch and parses its contents.
def loadWatchdirs(watchfile):
    try:
        fileobj = open(watchfile, "r")
        for line in fileobj:
            if line[0] == '#' or line[0] == '\n':
                continue

            #prepare
            line = line.rstrip()
            tmp = [x for x in line.split(', ')] 
            tmp[1] = int(tmp[1])

            #append
            watchDirs.append((tmp[0],tmp[1]))
    except IOError as e:
        log(str(e.errno) + str(e))
        log(e)


# Function: removeOldEp
# Arguments: (string) path to the show folder, (int) max number of files/episodes to keep
# Description: If more than the max number of files exist in a folder, this function will
# recursively find and remove or delete the oldest file till the threshold is met. Search includes subdirectories.
def removeOldEp(d, maxEpisodes):
    # init oldest file
    oldest_modified = datetime.datetime.now()
    path_to_oldest_file = ""
    oldest_filename = ""
    num_episodes_found = 0

    for dirpath, dirnames, filenames in os.walk(d):
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
                    oldest_filename = file

                    # old stuff based on time
                    # if (datetime.datetime.now() - time_last_modified) > datetime.timedelta(days=14) and size > 100000000:
                    # print(str(curpath) + " " + str(size))
                    # os.remove(curpath)

    log("Processing: " + d)
    log("Number of episodes found: " + str(num_episodes_found) + " (max:" + str(maxEpisodes) + ")")
    
    # remove the oldest episode(s) of the current show recursively, or finish processing current show and continue.
    if (num_episodes_found > maxEpisodes):
        if SAFEMODE:
            #todo: --dryrun here
            log("removing " + str(path_to_oldest_file) + " " + str(oldest_modified))
            shutil.move(path_to_oldest_file, os.path.join(safeDir,oldest_filename)) #move but don't delete
        else:
            log("deleting " + str(path_to_oldest_file) + " " + str(oldest_modified))
            # os.remove(path_to_oldest)

        #recursively process show directory, exit when show is below max num of episodes to keep
        removeOldEp(d, maxEpisodes)

    else:
        log("ok")
        log("Finished Processing: " + d)


# MAIN #########
log("DailyWatch starting...")

log("handling arguments")


log("Loading watchfile " + watchfile + "...")
loadWatchdirs(watchfile)

log("processing directories...")
for dirs, limit in watchDirs:
    removeOldEp(dirs, limit)
log("DailyWatch done. \n\n")
