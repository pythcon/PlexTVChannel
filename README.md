# DIY TV Channel for Plex

**Brief Description:** generatePlaylist.py will output blocks of episodes ranging from 40mins-1hr (blocks do not exceed 1hr) when provided a list of tv show directories. generateXMLTV.py will output guide data to import into plex. The two other bash script included are for linux users who want to setup total automation. These are run as a cron job and will take care of everything for you.

---

**Software Needed**:

- Plex (Plex Pass Required)

- [xTeVe] (https://xteve.de)

- VLC

- Python3 (if you want to generate a playlist and guide)

  - moviepy (pip3 install moviepy)
  - tvdb_api (pip3 install tvdb_api)

- FFmpeg [linux guide] (https://linoxide.com/linux-how-to/install-ffmpeg-centos-7/)

---

**A few notes:** I am using a *Linux* Server. You may need to adjust steps to make this work for your individual setup. This works by using vlc to start an http stream and then have xTeVe start capturing it. Then you add xTeVe into the Plex DVR section as a new device. It is pretty straight forward. To get VLC working, you need to generate a M3U playlist so it plays your list of videos in order, continuously. I wrote my Python script to generate this M3U file and generate a XMLTV guide to import into Plex.

**Before you run the python script, locate the following variables inside the script:**

```
cartoons = ["show1", "show2", "show3"]

dir = "" # Directory to grab shows from (make sure there is a "/" at the end!)
tvDirectory = "" # Directory where files will be generated (make sure there is a "/" at the end!)
commercialsDirectory = "" # Directory where commercials will be pulled from (make sure there is a "/" at the end!)
timezone = "" # Enter Timezone
showPoster = ""
channelName = ""
```

It is imperative that you populate the variables before you run the script!

---

*Step 1:* Generating your M3U playlist for VLC and XMLTV for Plex. Run the Python script by executing **python3 generatePlaylist.py <backup? (yes | no)> <commercials? (yes | no)>**. To generate the XMLTV Guide, run **python3 generateXMLTV.py**. The script will recognize if you selected backup or not.

---

*Step 2:* Launch VLC and test stream.
Launch VLC by using the command making sure to input the ip address of your machine and any port you would like to broadcast your http stream on:

```
vlc -vvv /path/to/tv/playlist.m3u --sout-keep --sout '#transcode{vcodec=h264, acodec=aac, vb=800, ab=128} :standard{access=http, mux=ts, dst=<ip:port>}’ --sout-mux-caching=5000
```
**Note**: If you have a **headless** install of a server, you need to use **cvlc** instead of vlc.

```
cvlc -vvv /path/to/tv/playlist.m3u --sout-keep --sout '#transcode{vcodec=h264, acodec=aac, vb=800, ab=128} :standard{access=http, mux=ts, dst=<ip:port>}’ --sout-mux-caching=5000
```
**Second Note**: If you copy and paste this command, it may not work. If you are not immediately getting lots of output, **manually type the command**.

---

*Step 3:* Open VLC on another computer/device and verify that your stream is working by using the ip address and port that you specified in the previous command.

---

*Step 4: If you’ve made it to this step, your VLC http stream is successfully working and you are ready to install xTeVe. xTeVe is going to some configuration so let's start with that.
    
Start xTeVe by navigating to the directory that you installed it and using the command **./xTeVe**. Take note of the url that is generated. Open up that webpage in your browser. Setup xTeVe to use XEPG. (You can setup xTeVe to run with systemd later)
    
---

*Step 5:* Generate a M3U file for xTeVe. We need a file for xTeVe to know where to grab our http stream from vlc. Create a new file called **vlc_stream.m3u** and open it. Put the following inside of it (replacing the name of your channel and ip:port):

```
#EXTM3U 
#EXTINF:-1,<Name of your channel> 
http://<ip:port>
```

---

*Step 6:* Setup xTeve Channel

Import that into xTeVe by navigating to the Playlist tab and clicking “new”. Input a name and the path to your **vlc_stream.m3u**. (This is NOT the Python generated m3u playlist!) 

Go to the XMLTV tab, click new and input the path to your xmltv.xml (whether it was generated from the Python script or you have your own).

Go to the mapping tab, click your channel and input the channel description, select the XMLTV file we created and the XMLTV channel.

---

*Step 7:* xTeVe Settings
This step is the most important of the tutorial. This took me countless hours to figure out. Navigate to the settings tab and scroll down to the streaming section. Change the stream buffer from no buffer to **VLC**. Scroll down a little bit more to the option labeled: *VLC / CVLC Options:*. Change your command to this:

```
-I dummy [URL] --sout #std{mux=ts,access=file,dst=-} --loop
```
    
All that was added was a --loop to keep the stream from replaying the same video over and over again.

---

*Step 8:* Open Plex and go to setting and click Live TV & DVR. Add a new device and type in the IP address of your xTeVe client. It should only be the IP address and the port. Click through the settings and when you get to the guide page, do not enter your zip code. Click the orange text at the top and input the path to your xmltv.xml file. Finish the setup and navigate to the Live TV section to see your TV station in action!

---

**Extras:**
Since I am a perfectionist, I setup my tvchannel to be completely automated. I have created a cron job with scripts so I never have to touch it. In an ideal situation, you would want to setup your tv station on a VM so it is contained in its own instance. This makes it very easy to test without having to reboot your whole setup. Make sure you update the scripts with the correct details listed below!

My cron job looks like this:

```
@reboot /path/to/tv/tvStart.sh
* * * * * /path/to/tv/tvContinue.sh
```
*tvStart.sh & tvContinue.sh instructions:*

*Editing the Path:* There is some editing needed in both **tvStart.sh** and **tvContinue.sh**. Open up both files and change all of the paths to your current setup. Just do a replace and search for **/path/to/tv/**.

*Editing the VLC IP:* Locate the **ip:port** phrase in the VLC command and change it with your current setup. Note: This is not always the same ip address if you are running VLC on a different machine.

*Editing the cURL statement (automatically refreshes the guide in Plex):* Start off by locating the **cURL** command in both scripts. 
- Get your **API token.** Instructions can be found [here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/).
- Replace the **PlexServerIP** with your server IP.
- Replace the **DVR ID** with your DVR ID. Go to https://PlexServerIP:32400/livetv/dvrs/?X-Plex-Token=api-token and locate the ID of your DVR.
- Populate the full statement.

---

This guide took me countless hours and critical thinking to put together. My ultimate goal was to make this work with Plex. I had an initial version working with VLC but I was not satisfied with it just working on the VLC client. It had to be Plex.

If you want to consider **donating** to me that would be great, but certainly not required!

[Donation Link](https://paypal.me/tmurphy605)

Feel free to message me with any questions you might have.

-**Todd**

[My Website](http://toddamurphy.me/)