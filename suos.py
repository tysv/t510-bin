#!/usr/bin/env python3
#                 SUOS
# the latin word 'suos' means 'their own'
#
# use .suos to change settings
# place .suos in the same directory as this script.

#boolean flags
debugging_mode = False
reset_mode     = False
verbose_mode   = False

logfile = "/home/ty/automation/reports/suos.log"
movedfiles = 0

import os, sys, time, glob, logging

logging.basicConfig(filename=f'{logfile}', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.NOTSET)

## Go through each label's settings
## and move files
## from source/old_name -> destination/new_name
def standard(setting):
    if verbose_mode == True: print("entering standard() function")
    label, destination, count, movarr = setting
    fileprocess(label, destination, count, movarr)    

def reset(setting):
	
    if verbose_mode == True: print("entering reset() function")
    label, destination, count, ignored_setting = setting
    movarr=glob.glob(f'{destination}{sep}*')
    llength=len(label)
    for name in movarr:
        basename=name.split(sep)[-1]
        if not label in basename[0:llength-1]:
            name=f'{destination}{sep}{label}{basename}'
    count=-1
    fileprocess(label, destination, count, movarr)

def fileprocess(label, destination, count, movarr):
    if verbose_mode == True:
        print("settings look like this:")
        print("label: " + label)
        print("destination: " + destination)
        print("count: " + str(count))
        print("movarr: " + str(movarr))
    for file in movarr:
        try:
            suffix= "." + file.split(".")[1]
        except: suffix = ""
        count+=1
        cstring = str(count).rjust(4,"0")
        tag=''
        optional_under='_'
        basename=file.split(sep)[-1]
        for c in basename.lower().strip(label).strip("_"):
            if c == '.': break
            if c.isalpha() or c in '_-':  tag+=c
        try:
            if tag == '' or tag[-1] == "_": optional_under=''
        except: optional_under = ''
        newfilepath = f'{destination}{sep}{label}_{tag}{optional_under}{cstring}{suffix}'
        if debugging_mode: print(f'Would do: {file} ---> {newfilepath}')
        else:
            os.rename(file, newfilepath)
            movedfiles+=1
        
    
############################## END OF FUNCTIONS ##############################
############################## START OF SCRIPT  ##############################


# necessary when calling from mu, which has
# its own "home directory" or whatever
#os.chdir('/home/ty/bin/mu_code/')
args = sys.argv
for arg in args[1:]:
    if verbose_mode == True: print(f"argument: {arg}")
    if "dry" in arg or "dryrun" in arg or "--dry" in arg or "-d" in arg: 
        debugging_mode = True
    elif "reset" in arg or "resetrun" in arg or "--reset" in arg or "-r" in arg:
        reset_mode = True
    elif "verbose" in arg or "verboserun" in arg or "--verbose" in arg or "-v" in arg:
        verbose_mode = True
    else:
        print("Command line usage: --dry and --reset modes.")
        print("Call again with no arguments and it'll just do the standard stuff")
        exit(0)

sep= os.path.sep
newline= f'\n'
user_name= os.environ.get('USER') #didn't fix, just hardcoded 'Ty'


#must point to where script is saved
scr_dir = os.path.join(sep, 'home', user_name, 'bin')
#for windows, change to TOP LEVEL of whatever directory structure.
#for instance might be /programfiles/uninstallinformation/
home_dir= os.path.join(sep, 'home', user_name) #NOT USED??


settings_file= open(f'{scr_dir}{sep}.suos', 'r')
lines = settings_file.readlines()
settings = []
sources = []

## Scans .suos file to build up script settings
for l in lines:
    newline=f'\n'
    l = l.rstrip(newline)
    words= l.split(";")
    #skippable lines (comments and blank lines)
    if ("#" in words[0]) or (newline in words[0]) or (len(l) <= 3): continue

    if (l[0:5] == "source" or words[0] == "source"): # SOURCE
        sources.append(words[1])
        if verbose_mode == True: print(f"source: {words[1]}")
        continue
    else: #label - destination pairs
        label = words[0]
        destination = words[1].rstrip(newline)
        count = len(glob.glob(f'{destination}{sep}{label}*'))
        entry = [label, destination, count, []]
        settings.append(entry)

settings_file.close()

##  BUILD THE MATCHED FILES LIST
##  FOR EACH OF THE LABELS and
##  FOR EACH OF THE SOURCES
for source in sources:
    try:
        os.chdir(os.path.normpath(source))
    except: continue
    cwd= str(os.path.abspath(os.getcwd()))
    for check in settings:
        matched_files=[]
        label, count = (check[0], check[1])
        #destination = check[2] # an array of destinations... ??? wat? Idk man
        for found in glob.glob(f'{label}*'):
            fullpath=f'{cwd}{sep}{found}'
            matched_files.append(fullpath)
        check[3].extend(matched_files)

if debugging_mode == True:
    print("settings: ")
    for s in settings:
        print(str(s))
    print()

if reset_mode == True:
    for s in settings:
        reset(s)
else:
    for s in settings:
        standard(s)
        
if (movedfiles > 0):
	logging.info(f'{time.strftime("%c")}: Moved {movedfiles} files')
#else: logging.info('TEST') #just for testing when no files to move
