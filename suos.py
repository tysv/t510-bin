#!/usr/bin/python3
#                 SUOS
# the latin word 'suos' means 'their own'
#
# use .suos to change settings
# place .suos in the same directory as this script.import os

debugging_mode = False
standard_mode  = True
verbose_mode   = True
manual_mode    = False
reset_mode     = False



import os, sys, time, glob, random
import shutil, string

def print_help_text():
	print("SUOS HELP TEXT BRO ITS RIGHT HERE")
	print("flags: --dry, --verbose, --reset, --manual")
	print("todo: put more information here")
	exit(0)

def search_replace(base_string, search_for, replacement_with):
    result=''
    if base_string == '' or search_for == '': return result
    for character in base_string:
        if character in search_for: result+=replacement_with
        else: result+=character
    return result

def manual(setting):
    if verbose_mode == True: print("----entering manual() function")
    def namegen():
        n=''
        for i in range(1,12):
            n+=str(random.randint(0, 9))
        #print(f'n: {n}')
        return n
    #this would be a good place to go through a special folder like
    #/pornstart/unsorted/sort-LABEL where EACH LABEL TYPE got a folder
    #for manual sorting. Anything in there gets moved to the proper
    #storage spot with a generic name ala uhm_0001 or joi_0121
    #copy paste sorting then run "suos.py --unsorted"
    #could even just rename them and move them to /downloads/ or something
    #to be later integrated?
    #expand movearr with the default-named-manually-sorted-fellas
    label, destination, count, ignore = setting
    try:
        manual_sort_spot=f"{destination}{sep}manual{sep}"
        print(f"manual_sort_spot: {manual_sort_spot}")
        #os.chdir(manual_sort_spot)
        movarr=glob.glob(f'{manual_sort_spot}*')
        count=0

        fileprocess(label, destination, count, movarr)
        newmov = []
        for file in movarr:
            if os.path.isdir(file): continue
            count+=1
            extension=file.split(sep)[-1] #Just the basename
            if len(extension.split(".")) > 1:
                extension=extension.split(".")[-1]
                extension=f".{prefix}"
            else:
                extension=''
            newname=f"{manual_sort_spot}" + namegen() + extension
            #print(f"name: {name}")
            if debugging_mode:
                print(f'Would do: [{file}] -> [{newname}]')
            else:
                if verbose_mode == True: print(f'DOING: [{file}] -> [{newname}]')
                os.rename(f"{file}", f"{newname}")
            newmov.append(newname)
        if verbose_mode == True: print("manual mode finished w/the movarr loop")
        fileprocess(label, destination, count, newmov)
        return 0
    except Exception as ex:
        print("caught errors:")
        print(ex)
    exit(11)

## Go through each label's settings
## and move files
## from source/old_name -> destination/new_name
def standard(setting):
    if verbose_mode == True: print("----entering standard() function")
    label, destination, count, movarr = setting
    fileprocess(label, destination, count, movarr)

def reset(setting):
    print("implementation dangerous and Idk man what was this for?")
    return 1
    exit(0)
"""
    if verbose_mode == True: print("----entering reset() function")
    label, destination, count, ignored_setting = setting
    movarr=glob.glob(f'{destination}{sep}*')
    llength=len(label)

    for name in movarr:
        basename=name.split(sep)[-1]
        if not label in basename[0:llength]:
            #print(f'basename: {basename}')
            name=f'{destination}{sep}{label}{basename}'
            #print(f'name: {name}')
    count=-1
    fileprocess(label, destination, count, movarr)
"""
def fileprocess(label, destination, count, movarr):
    if verbose_mode == True:
        print("----filepocess() received:")
        print("--label: " + label)
        print("--destination: " + destination)
        print("--count: " + str(count))
        print("--movarr: " + str(movarr))
    for file in movarr:
        if not os.path.isfile(file): continue
        basename=file.split(sep)[-1]
        try:
            suffix= "." + basename.split(".")[-1]
        except:
            suffix = ""
        count+=1
        count_string = str(count).rjust(4,"0")
        tag=''
        optional_under='_'
        optional_sub_folders=''
        #detect if tag is present in the basename,
        #               only allow certain characters into tag (A-z_-)
        #               and if it was terminated with '_' or needs it still
        for c in basename.lower().lstrip(label).lstrip("_"):
            if c == '.': break
            elif c.isalpha() or c in '-_':  tag+=c
            elif c == ' ': tag+='-'
        try:
            if tag == '' or tag[-1] == "_": optional_under=''
        except: optional_under = ''

        #CHECK FOR ALTERNATE DESTINATIONS NOW
        #w/in the destination (/joi/) look for a SUBFOLDER sharing name w/tag
        tags=tag.split('_')
        for t in tags:
            subfolder=f'{sep}{t}'
            if os.path.isdir(f'{destination}{optional_sub_folders}{subfolder}'):
                optional_sub_folders+=subfolder
            else: break

        newfilepath = \
        f'{destination}{optional_sub_folders}{sep}{label}_{tag}{optional_under}{count_string}{suffix}'

        if debugging_mode:
            print(f'Would do: {file} ---> {newfilepath}')
        else:
            if verbose_mode: print(f'trying: shutil.move({file},{newfilepath}')
            shutil.move(file,newfilepath)
            #os.renames(file, newfilepath)


############################## END OF FUNCTIONS ##############################
############################## START OF SCRIPT  ##############################

if verbose_mode: print("end functions/start script")

# necessary when calling from mu, which has
# its own "home directory" or whatever
#os.chdir('/home/ty/bin/mu_code/')
args = sys.argv
if len(args) > 1:
    if "help" in args or "--help" in args or "-h" in args:
        print_help_text()
    if "dry" in args or "dryrun" in args or "--dry" in args or "-d" in args:
        debugging_mode = True
    if "debug" in args or "--debug" in args:
        debugging_mode = True
    if "reset" in args or "resetrun" in args or "--reset" in args or "-r" in args:
        reset_mode = True
    if "verbose" in args or "verboserun" in args or "--verbose" in args or "-v" in args:
        verbose_mode = True
    if "manual" in args or "manualrun" in args or "--manual" in args or "-m" in args:
        manual_mode = True
    #print("Command line usage: --dry and --reset modes.")
    #print("Call again with no arguments and it'll just do the standard stuff")
    #exit(0)

sep = os.path.sep
newline = f'\n'
user_name = os.environ.get('USER') #didn't fix, just hardcoded 'Ty' ??? but now?

#must point to where script is saved
#"C:\Users\Ty\Documents\scripts"
#for windows, change to TOP LEVEL of whatever directory structure.
scr_file = os.path.realpath(__file__)
scr_dir =  os.path.dirname(scr_file)
#for instance might be /programfiles/uninstallinformation/
#doesn't seem to be needed? # home_dir= os.path.join(sep, 'home', user_name)


settings_file = open(f'{scr_dir}{sep}.suos', 'r')
lines = settings_file.readlines()
settings = []
sources = []
if verbose_mode: print("scanning .suos file")

## Scans .suos file to build up script settings
for l in lines:
    l = l.rstrip(newline)
    words= l.split(";")
    #skippable lines (comments and blank lines)
    if ("#" in words[0]) or (newline in words[0]) or (len(l) <= 3): continue

    if (l[0:5] == "source" or words[0] == "source"): # SOURCE
        sources.append(words[1])
        #print(words[1])
        continue
    else: #label - destination pairs
        label = words[0]
        destination = words[1].rstrip(newline)
        if os.path.isdir(destination) == True: print(f'{destination} exists bro')
        else:
            print("it don't exist")
            os.mkdir(destination)
            if os.path.isdir(destination) == True:
                print(f'{destination} exists NOW.')
            else: print(f"creation of {destination} FAILED")
        count = len(glob.glob(f'{destination}{sep}**', recursive=True))
        entry = [label, destination, count, []]
        settings.append(entry)

settings_file.close()
if verbose_mode: print("closed .suos file")

##  BUILD THE MATCHED FILES LIST
##  FOR EACH OF THE LABELS and
##  FOR EACH OF THE SOURCES
for source in sources:
    try:
        os.chdir(os.path.normpath(source))
    except: continue
    cwd= str(os.path.abspath(os.getcwd()))
    for set in settings:
        matched_files=[]
        label, count = (set[0], set[1])
        for found in glob.glob(f'{label}*'):
            fullpath=f'{cwd}{sep}{found}'
            matched_files.append(fullpath)
        set[3].extend(matched_files)

if verbose_mode: print("--done setting up--")

if debugging_mode == True:
    print("settings: ")
    for s in settings:
        print(str(s))
    print()

if reset_mode == True:
    for s in settings:
        reset(s)
if manual_mode == True:
    for s in settings:
        manual(s)
if standard_mode == True:
    for s in settings:
        standard(s)

