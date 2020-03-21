#!/bin/bash
LOCKFILE=/tmp/tvLockFile.lock

#Do not run script if characters less than 10 (if uptime is less than 10 minutes)
uptime=`uptime -p | cut -d " " -f2-`
if [ "${#uptime}" -lt 10 ]
then
    echo "Uptime has not reached 10 minutes!"
    exit 1
fi

if pgrep -x "tvStart.sh" > /dev/null
then
    echo "tvStart.sh running...exiting"
else
    # If lockfile exists
    if [ -f "$LOCKFILE" ]
    then
        echo "tvContinue.sh running...exiting"
        exit 1
    else
        if pgrep -x "vlc" > /dev/null
        then
            echo "VLC running...exiting"
        else
            # Create Lock File
            touch "$LOCKFILE"

            #Generate Guide Data
            python3 /path/to/tv/generateXMLTV.py

            sleep 2

            #Move backup files to current files
            mv -f /path/to/tv/showList1.txt /path/to/tv/showList.txt
            mv -f /path/to/tv/playlist1.m3u /path/to/tv/playlist.m3u
            mv -f /path/to/tv/xmltv1.xml /path/to/tv/xmltv.xml

            sleep 2

            echo "VLC stopped...starting it"
            /usr/bin/cvlc /path/to/tv/playlist.m3u --sout-keep --sout '#transcode{vcodec=h264, acodec=aac, vb=800, ab=128} :standard{access=http, mux=ts, dst=<ip:port>}' --sout-mux-caching=5000 &

            sleep 5

            echo -ne '\n'

            sleep 2

            #Generate a new playlist
            python3 /path/to/tv/generatePlaylist.py yes

            sleep 2

            # Remove Lock File
            rm -f "$LOCKFILE"

            curl -X POST "https://<PlexServerIP>:32400/livetv/dvrs/<dvrID>/reloadGuide?X-Plex-Token=<api token>"

        fi
    fi
fi
