import os
import sys
import random
import moviepy.editor as mp
import time
import math
from datetime import datetime, timedelta
import tvdb_api

# Display help
# Check if it is a backup file
backup = False
commercials = True
if not len(sys.argv) > 1:
    print ("Incorrect Usage: python3 generateShowList.py <backup? (yes | no)>")
    exit()
else:
    if sys.argv[1] == "yes":
        backup = True
        print ("BACKUP FLAG WAS SET TO TRUE")
        time.sleep(3)
if dir == "":
    print ("Please populate your 'dir' variable! It cannot be null. Open up the script")
    exit()


########################################################
########################################################
#        Edit these variable to your system!           #
########################################################
########################################################

cartoons = ["show1", "show2", "show3"]

dir = "" # Directory to grab shows from (make sure there is a "/" at the end!)
tvDirectory = "" # Directory where files will be generated (make sure there is a "/" at the end!)
commercialsDirectory = "" # Directory where commercials will be pulled from (make sure there is a "/" at the end!)
timezone = "" # Enter Timezone
showPoster = ""
channelName = ""

########################################################
########################################################
#                       END                            #
########################################################
########################################################

cartoonsLeft = cartoons.copy()
showDirectory = []
commercialList = []
commercialSpecific = {}
previousRandomShow = 999
playlistDuration = 0
showDurations = []
showName = ""
showDesc = ""
showCounter = 0
showLength = 0
blockCounter = 0
t = tvdb_api.Tvdb()


extensions = ['.264', '.3g2', '.3gp', '.3gp2', '.3gpp', '.3gpp2', '.3mm', '.3p2', '.60d', '.787', '.89', '.aaf', '.aec', '.aep', '.aepx',
              '.aet', '.aetx', '.ajp', '.ale', '.am', '.amc', '.amv', '.amx', '.anim', '.aqt', '.arcut', '.arf', '.asf', '.asx', '.avb',
              '.avc', '.avd', '.avi', '.avp', '.avs', '.avs', '.avv', '.axm', '.bdm', '.bdmv', '.bdt2', '.bdt3', '.bik', '.bin', '.bix',
              '.bmk', '.bnp', '.box', '.bs4', '.bsf', '.bvr', '.byu', '.camproj', '.camrec', '.camv', '.ced', '.cel', '.cine', '.cip',
              '.clpi', '.cmmp', '.cmmtpl', '.cmproj', '.cmrec', '.cpi', '.cst', '.cvc', '.cx3', '.d2v', '.d3v', '.dat', '.dav', '.dce',
              '.dck', '.dcr', '.dcr', '.ddat', '.dif', '.dir', '.divx', '.dlx', '.dmb', '.dmsd', '.dmsd3d', '.dmsm', '.dmsm3d', '.dmss',
              '.dmx', '.dnc', '.dpa', '.dpg', '.dream', '.dsy', '.dv', '.dv-avi', '.dv4', '.dvdmedia', '.dvr', '.dvr-ms', '.dvx', '.dxr',
              '.dzm', '.dzp', '.dzt', '.edl', '.evo', '.eye', '.ezt', '.f4p', '.f4v', '.fbr', '.fbr', '.fbz', '.fcp', '.fcproject', '.ffd',
              '.flc', '.flh', '.fli', '.flv', '.flx', '.gfp', '.gl', '.gom', '.grasp', '.gts', '.gvi', '.gvp', '.h264', '.hdmov', '.hkm',
              '.ifo', '.imovieproj', '.imovieproject', '.ircp', '.irf', '.ism', '.ismc', '.ismv', '.iva', '.ivf', '.ivr', '.ivs', '.izz',
              '.izzy', '.jss', '.jts', '.jtv', '.k3g', '.kmv', '.ktn', '.lrec', '.lsf', '.lsx', '.m15', '.m1pg', '.m1v', '.m21', '.m21',
              '.m2a', '.m2p', '.m2t', '.m2ts', '.m2v', '.m4e', '.m4u', '.m4v', '.m75', '.mani', '.meta', '.mgv', '.mj2', '.mjp', '.mjpg',
              '.mk3d', '.mkv', '.mmv', '.mnv', '.mob', '.mod', '.modd', '.moff', '.moi', '.moov', '.mov', '.movie', '.mp21', '.mp21',
              '.mp2v', '.mp4', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg4', '.mpf', '.mpg', '.mpg2', '.mpgindex', '.mpl', '.mpl',
              '.mpls', '.mpsub', '.mpv', '.mpv2', '.mqv', '.msdvd', '.mse', '.msh', '.mswmm', '.mts', '.mtv', '.mvb', '.mvc', '.mvd',
              '.mve', '.mvex', '.mvp', '.mvp', '.mvy', '.mxf', '.mxv', '.mys', '.ncor', '.nsv', '.nut', '.nuv', '.nvc', '.ogm', '.ogv', '.ogx',
              '.osp', '.otrkey', '.pac', '.par', '.pds', '.pgi', '.photoshow', '.piv', '.pjs', '.playlist', '.plproj', '.pmf', '.pmv', '.pns',
              '.ppj', '.prel', '.pro', '.prproj', '.prtl', '.psb', '.psh', '.pssd', '.pva', '.pvr', '.pxv', '.qt', '.qtch', '.qtindex', '.qtl',
              '.qtm', '.qtz', '.r3d', '.rcd', '.rcproject', '.rdb', '.rec', '.rm', '.rmd', '.rmd', '.rmp', '.rms', '.rmv', '.rmvb', '.roq', '.rp',
              '.rsx', '.rts', '.rts', '.rum', '.rv', '.rvid', '.rvl', '.sbk', '.sbt', '.scc', '.scm', '.scm', '.scn', '.screenflow', '.sec',
              '.sedprj', '.seq', '.sfd', '.sfvidcap', '.siv', '.smi', '.smi', '.smil', '.smk', '.sml', '.smv', '.spl', '.sqz', '.srt', '.ssf',
              '.ssm', '.stl', '.str', '.stx', '.svi', '.swf', '.swi', '.swt', '.tda3mt', '.tdx', '.thp', '.tivo', '.tix', '.tod', '.tp', '.tp0',
              '.tpd', '.tpr', '.trp', '.ts', '.tsp', '.ttxt', '.tvs', '.usf', '.usm', '.vc1', '.vcpf', '.vcr', '.vcv', '.vdo', '.vdr', '.vdx',
              '.veg', '.vem', '.vep', '.vf', '.vft', '.vfw', '.vfz', '.vgz', '.vid', '.video', '.viewlet', '.viv', '.vivo', '.vlab', '.vob',
              '.vp3', '.vp6', '.vp7', '.vpj', '.vro', '.vs4', '.vse', '.vsp', '.w32', '.wcp', '.webm', '.wlmp', '.wm', '.wmd', '.wmmp', '.wmv',
              '.wmx', '.wot', '.wp3', '.wpl', '.wtv', '.wve', '.wvx', '.xej', '.xel', '.xesc', '.xfl', '.xlmv', '.xmv', '.xvid', '.y4m', '.yog',
              '.yuv', '.zeg', '.zm1', '.zm2', '.zm3', '.zmv']


print("#####GENERATING SHOW LIST#####")


########################################################
# Writes to the show list
########################################################
def writeToArray(path):
    global tempShowList
    global extensions

    ext = os.path.splitext(path)[-1].lower()

    if ext in extensions:
        tempShowList.append(path)
        #print("Added: " + path)
########################################################
        

########################################################
# Check duration of file
########################################################
def checkDuration(file):
    try:
        return mp.VideoFileClip(file).duration
    except OSError:
        print("Could not get duration for: " + file)
        return 1799  # default value if it fails
########################################################


########################################################
# Generate episdoe list that fit into 40min -1hr block
########################################################
def generateBlock(episodes):
    global playlistDuration
    returnList = []
    durationCheck = False
    totalDuration = 0

    while not durationCheck:
        randomChoice = random.choice(episodes)
        currentDuration = checkDuration(randomChoice)
        totalDuration += currentDuration
        playlistDuration += currentDuration

        if totalDuration < 3600:
            returnList.append(randomChoice)
        else:
            durationCheck = True
    return returnList
########################################################


########################################################
# Generate a random commercial
########################################################
def getRandomCommercial(listOfCommercials):
    randomNumber = random.randint(0, len(listOfCommercials)-1)
    return listOfCommercials[randomNumber]
    
########################################################


########################################################
# Get Poster for show
########################################################
def getShowPoster(show_name):
    global showPoster
    global t
    
    try:
        show = t[show_name] # Get Show
        poster = show.data['poster'] # Get poster for show
        return poster
    except: #If not found return channel poster
        return showPoster
    
########################################################


########################################################
# Get Description for show
########################################################
def getShowDescription(show_name):
    global t
    
    try:
        show = t[show_name] # Get Show
        desc = show.data['overview'] # Get description for show
        return desc
    except: #If not found return channel poster
        return ""
    
########################################################

    
# Loops into individual directories to get directly to files
while len(cartoonsLeft) != 0:
    tempShowList = []
    randomNumber = random.randint(0, len(cartoonsLeft)-1)
    currentShow = cartoonsLeft[randomNumber]
    cartoonsLeft.remove(currentShow)

    for file in os.listdir(dir + currentShow):
        if "Specials" in file or "Subs" in file: #omit specials, extras, subtitles and deleted scenes
            continue
        if os.path.isfile(dir + currentShow + "/" + file):
            writeToArray(dir + currentShow + "/" + file)
        else:
            for seasonFile in os.listdir(dir + currentShow + "/" + file):
                writeToArray(dir + currentShow + "/" + file + "/" + seasonFile)
    showDirectory.append(tempShowList.copy())

# Clear Temp Show List
tempShowList = []

# Loops into commercials directory
if (commercials):
    for file in os.listdir(commercialsDirectory):
        if "ignore" in file: #omit commercials you dont want
            continue
        if os.path.isfile(commercialsDirectory + file):
            writeToArray(commercialsDirectory + file)
        else:
            for subFile in os.listdir(commercialsDirectory + file):
                if os.path.isfile(commercialsDirectory + file + "/" + subFile):
                    writeToArray(commercialsDirectory + file + "/" + subFile)
                else:
                    tempSpecificList = []
                    tempSpecificShow = ""
                    for specificCommercial in os.listdir(commercialsDirectory + file + "/" + subFile):
                        tempSpecificList.append(commercialsDirectory + file + "/" + subFile + "/" + specificCommercial)
                        tempSpecificShow = specificCommercial

                    # After Specific Show list is generated, insert into dictionary
                    commercialSpecific[tempSpecificShow] = tempSpecificList.copy()
                        
    commercialList = tempShowList.copy()
    
# Open Files
if not backup:
    tvList = open(tvDirectory + "showList.txt", "w")
    m3u = open(tvDirectory + "playlist.m3u", "w")
else:
    tvList = open(tvDirectory + "showList1.txt", "w")
    m3u = open(tvDirectory + "playlist1.m3u", "w")
xmltv = open(tvDirectory + "temp_xmltv.xml", "w")

# Initial line in M3U file
m3u.write("#EXTM3U\n")

# Initial line for xmltv
xmltv.write("<tv generator-info-name='Todd' source-info-name='Todds Generator'>\n")
xmltv.write("<channel id='1'>\n")
xmltv.write("<display-name>" + channelName + "</display-name>\n")
xmltv.write("<icon src='" + showPoster + "'/>\n")
xmltv.write("</channel>\n")

# Generate Blocks of Episodes & puts back into directory
while blockCounter < len(showDirectory):
    print ("Generating Blocks..." + str(len(showDirectory) - blockCounter) + " left.")
    showDirectory[blockCounter] = generateBlock(showDirectory[blockCounter])
    blockCounter += 1

# Loops through show directory and generate random schedule
while len(showDirectory) > 0:
    randomShow = random.randint(0, len(showDirectory)-1) # already a random show because populated in random order
    specificCommercialFound = False # Initial Specific Commercial
    initialRunThrough = True

    while len(showDirectory[randomShow]) > 0:
        randomEpisode = random.choice(showDirectory[randomShow])
        randomEpisodeWrite = randomEpisode.encode('utf-8').strip().decode()

        # Get Name of Show
        showName = randomEpisode.split(dir)[1].split('/')[0]
        
        # Get Description of Show (Episode Name)
        showDesc = os.path.basename(randomEpisode)
        showDesc = os.path.splitext(showDesc)[0]
        
        if (commercials):
            # Only check for specific commercial on initial run-through
            if initialRunThrough:
                initialRunThrough = False # No longer initial run-through
                
                # Check to see if there is specific commercial
                for show in commercialSpecific.keys():
                    if show.lower() in showName.lower():
                        randomCommercial = random.choice(commercialSpecific[show])
                        specificCommercialFound = True # Found a specific commercial

        print("Writing: " + showName)
        
        # Write episode to txt file
        tvList.write(randomEpisodeWrite)
        tvList.write("\n")

        #Need to get duration for XML and array
        cur_duration = checkDuration(randomEpisode)

        # Write episode to m3u file
        m3u.write("#EXTINF: " + str(cur_duration) + ", " + showDesc + "\n")
        m3u.write("file://" + randomEpisodeWrite + "\n")

        # Add extra guide information
        showDesc += " ||\n\n "
        showDesc += getShowDescription(showName)

        # Write episode to xmltv file
        xmltv.write("<programme channel='1' start='{tempStartTime} " + timezone + "' stop='{tempEndTime} " + timezone + "'>\n")
        xmltv.write("<title lang='en'>" + showName + "</title>\n")
        xmltv.write("<desc lang='en'>" + showDesc + "</desc>\n")
        xmltv.write("<icon height='' src='" + getShowPoster(showName) + "' width=''/>\n")
        xmltv.write("<video/>\n<date/>\n<new/>\n</programme>\n")

        # If commercials
        if (commercials):

            # If there is no specific commercial
            if not specificCommercialFound:
                randomCommercial = getRandomCommercial(commercialList).encode('utf-8').strip().decode()

            commercial_duration = checkDuration(randomCommercial)
                
            m3u.write("#EXTINF: " + str(commercial_duration) + ", Commercial\n")
            m3u.write("file://" + randomCommercial + "\n")

        # Round duration to the nearest second
        cur_duration = math.ceil(cur_duration)        # Add Episode and Duration to dictionary
        showDurations.append(cur_duration)

        # Remove the episode
        #print ("Removing: " + randomEpisode)
        showDirectory[randomShow].remove(randomEpisode)

        specificCommercialFound = False

    # Remove show
    del showDirectory[randomShow]

# Close xmltv
xmltv.write("</tv>")

# Close files
tvList.close()
m3u.close()
xmltv.close()

# store variables to file for later xmltv generation
temp_variables = open(tvDirectory + "temp_variables.py", "w")
temp_variables.write("tvDirectory='" + tvDirectory +"'")
temp_variables.write("\n")
if backup:
    temp_variables.write("backup=True")
else:
    temp_variables.write("backup=False")
temp_variables.write("\n")
temp_variables.write("showDurations=" + str(showDurations))
temp_variables.close()

print ("Playlist Duration in seconds: " + str(playlistDuration))
print("Finished! Happy Streaming!")
