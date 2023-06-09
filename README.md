# Acids-SportTorrent-Renamer
Python script to rename SportTorrents files to TSDB naming convention to appease SportScanner Plex agent for proper metadata parsing

```diff
                                    **D i s c l a i m e r :**
- This script is not perfect. Im still working on the logic to get the matching more presice. But overall, it does a good job.
- Please double check your results and report back specific files that do not get named.
```


**Requirments:**

_Python 3.0+_


**SETUP ENV:**

_pip install csv_
 
 _pip install os_
 
 _pip install re_

**HOW TO:**
1. Download: https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/archive/refs/heads/main.zip
2. Extract somewhere
3. Update Renamer.py with your actual Paths
![set_dir](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/4b972359-9d80-4c68-b102-59630348db4a)
3. Open Command Prompt (or equal..)
4. Type: "cd {Location of Acids-SportTorrent-Renamer}"
5. Type: "python Renamer.py"
  
  --Script should now be trying to match & rename your files in video_dir to the data in csv_dir



TheSportDB offers 3 styles of naming conventions to work along Plex and Kodi.
![TSDB-naming-convention](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/3fbff5ed-fbe5-4dda-992a-6f0eca64a34c)

The script can extract either of the 3 naming conventions. 
Simply edit the Renamer.py code and select your desired column to pull the new name from.
![4  Plex_  5  Kodi_  6  Kodi 2](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/979b3945-76a3-4418-9dc1-c8abc52c0ce1)


**Request Data:**
To request .csv data for your specific desired league, please visit "https://thesportsdb.com/" and find your League, and send me a Pull Request with the League ID associated with the League. 
_(i.e, https://thesportsdb.com/league/4380 - "4380" is the League ID for the NHL)_

I will refresh the Data folder every few days.

For Sport Torrents, the most consistent naming convention to follow was provided by this [twitter account @SportTorrents](https://twitter.com/SportTorrents); this made the job of making a Renamer much "easier". 
