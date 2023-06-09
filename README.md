# Acids-SportTorrent-Renamer
Python script to rename SportTorrents files to TSDB naming convention to appease SportScanner Plex agent for proper metadata parsing

```diff
                                    **D i s c l a i m e r :**
- This script is not perfect. Im still working on the logic to get the matching more presice. But overall, it does a good job.
- Please double check your results and report back specific files that do not get named.
```
<br>

**Requirments:**

_Python 3.0+_
<br>

**SETUP ENV:**

_pip install csv_
 
 _pip install os_
 
 _pip install re_
<br>

**HOW TO:**
1. Download: https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/archive/refs/heads/main.zip
2. Extract somewhere
3. Update Renamer.py with your actual Paths
![set_dir](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/4b972359-9d80-4c68-b102-59630348db4a)
3. Open Command Prompt (or equal..)
4. Type: "cd {Location of Acids-SportTorrent-Renamer}"
5. Type: "python Renamer.py"
  
  --Script should now be trying to match & rename your files in video_dir to the data in csv_dir
<br>


TheSportDB offers 3 styles of naming conventions to work along Plex and Kodi.
![TSDB-naming-convention](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/3fbff5ed-fbe5-4dda-992a-6f0eca64a34c)

The script can extract either of the 3 naming conventions. 
Simply edit the Renamer.py code and select your desired column to pull the new name from.
![4  Plex_  5  Kodi_  6  Kodi 2](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/979b3945-76a3-4418-9dc1-c8abc52c0ce1)
<br>

**Request Data:**
To request .csv data for your specific desired league, please visit "https://thesportsdb.com/" and find your League, and send me a Pull Request with the League ID associated with the League. 
_(i.e, https://thesportsdb.com/league/4380 - "4380" is the League ID for the NHL)_

I will refresh the Data folder every few days.

<br>

**Tools:**

```Organizer.py``` - I made this script with the aim of automatically moving/Organizing files that were freshly renamed.
currently this script **creates a folder for every league that TSDB covers...which...is 989 leagues or something**...
Please be prepared for that! OR edit the code in Organizer.py to only handle the Leagues you like.

   **Instructions**
 Edit the code in Organizer.py and highlight `'J:`
 
![Highlight_J](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/4915b5ff-41a8-419f-a3ff-bece2164a561)

Toggle Ctrl + H to "Replace"

![Ctrl_H_to_Replace](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/94419ea8-c6ae-4cfc-9ac6-3013c4dca379)

Write new desired Drive letter/location.

Toggle Ctrl + Alt + Enter to Confirm replacement.

![Ctrl_Alt_Enter_to_Confirm_Replace](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/886c3773-9437-45f7-a590-7a807bd0628a)

Your Code should be updated:

![Your_new_File_location](https://github.com/AcidAlchamy/Acids-SportTorrent-Renamer/assets/111721042/be9cd534-384e-4b7e-a5a0-cccef584039e)
                   
                   
                   






For Sport Torrents, the most consistent naming convention to follow was provided by this [twitter account @SportTorrents](https://twitter.com/SportTorrents); this made the job of making a Renamer much "easier". 
