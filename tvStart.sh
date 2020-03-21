#!/bin/bash
echo "Generating playlist for Todderang"

python3 /path/to/tv/generatePlaylist.py no

sleep 5

python3 /path/to/tv/generateXMLTV.py

sleep 2

curl -X POST "https://<PlexServerIP>:32400/livetv/dvrs/<dvrID>/reloadGuide?X-Plex-Token=<api token>"

sleep 2

/usr/bin/cvlc /path/to/tv/playlist.m3u --sout-keep --sout '#transcode{vcodec=h264, acodec=aac, vb=800, ab=128} :standard{access=http, mux=ts, dst=<ip:port>}' --sout-mux-caching=5000 &

sleep 5

echo -ne '\n'

sleep 2

python3 /path/to/tv/generatePlaylist.py yes
