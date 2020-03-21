import time
from datetime import datetime, timedelta
import temp_variables

def generateGuideData(myTvDirectory, myBackup, myShowDurations):
    showCounter = 0
    print("Generating Guide Data...This will take a few seconds")

    # Replace time in xmltv files
    ## Need to do this after execution b/c script takes long to execute
    f1 = open(myTvDirectory + 'temp_xmltv.xml', 'r')
    if not myBackup:
        f2 = open(myTvDirectory + 'xmltv.xml', 'w')
    else:
        f2 = open(myTvDirectory + 'xmltv1.xml', 'w')

    # Wait for script to run on the minute (0 seconds)
    timeObject = datetime.now()
    myCurrentTime = int(timeObject.strftime("%S"))
    while (myCurrentTime / 60) != 0:
        timeObject = datetime.now()
        myCurrentTime = int(timeObject.strftime("%S"))
        continue

    for line in f1:
        # Replace & with correct escape
        line = line.replace('&', '&amp;')
        
        if '{tempStartTime}' in line:
            showLength = myShowDurations[showCounter]
            print ("Show length: " + str(showLength))
            currentTime = timeObject.strftime("%Y%m%d%H%M%S")
            line = line.replace('{tempStartTime}', str(currentTime))
            timeObject += timedelta(seconds=showLength)
            currentTime = timeObject.strftime("%Y%m%d%H%M%S")
            line = line.replace('{tempEndTime}', str(currentTime))

            # Increase show counter
            showCounter += 1
            
        f2.write(line)
        
    # Close xmltv
    f1.close()
    f2.close()

# Call the function
generateGuideData(temp_variables.tvDirectory, temp_variables.backup, list(temp_variables.showDurations))
